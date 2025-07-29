"""Root agent responsible for project planning and orchestration"""

from typing import List, Dict, Any, Optional, Tuple
import asyncio
from datetime import datetime
from loguru import logger
import json

from .base import BaseAgent, Task, AgentContext
from ..core.config import AgentConfig


class ProjectPlan:
    """Represents a complete project plan"""
    
    def __init__(self, description: str):
        self.description = description
        self.tasks: List[Task] = []
        self.task_graph: Dict[str, List[str]] = {}  # task_id -> dependencies
        self.agent_assignments: Dict[str, str] = {}  # task_id -> agent_type
        self.parallel_groups: List[List[str]] = []  # Groups of tasks that can run in parallel
        self.created_at = datetime.now()
    
    def add_task(
        self,
        task: Task,
        dependencies: Optional[List[str]] = None,
        suggested_agent: Optional[str] = None
    ):
        """Add a task to the plan"""
        self.tasks.append(task)
        self.task_graph[task.id] = dependencies or []
        if suggested_agent:
            self.agent_assignments[task.id] = suggested_agent
    
    def analyze_parallelism(self):
        """Analyze which tasks can be executed in parallel"""
        # Find tasks with no dependencies (can start immediately)
        ready_tasks = [
            task.id for task in self.tasks
            if not self.task_graph.get(task.id, [])
        ]
        
        self.parallel_groups = []
        processed = set()
        
        while len(processed) < len(self.tasks):
            current_group = []
            
            for task_id in ready_tasks:
                if task_id not in processed:
                    current_group.append(task_id)
                    processed.add(task_id)
            
            if current_group:
                self.parallel_groups.append(current_group)
            
            # Find next ready tasks
            ready_tasks = []
            for task in self.tasks:
                if task.id not in processed:
                    deps = self.task_graph.get(task.id, [])
                    if all(dep in processed for dep in deps):
                        ready_tasks.append(task.id)
        
        logger.info(f"Identified {len(self.parallel_groups)} parallel execution groups")


class RootAgent(BaseAgent):
    """Root orchestration agent"""
    
    def __init__(self, config: AgentConfig, memory_service=None, llm_client=None):
        super().__init__(config, memory_service)
        self.llm_client = llm_client
        self.current_plan: Optional[ProjectPlan] = None
        self.execution_history: List[Dict[str, Any]] = []
    
    def can_handle(self, task: Task) -> bool:
        """Root agent handles planning and orchestration tasks"""
        return task.type in ["planning", "orchestration", "analysis"]
    
    async def execute(self, context: AgentContext) -> Tuple[bool, Any]:
        """Execute root agent tasks"""
        task_type = context.task.type
        
        if task_type == "planning":
            return await self._create_project_plan(context)
        elif task_type == "orchestration":
            return await self._orchestrate_execution(context)
        elif task_type == "analysis":
            return await self._analyze_requirements(context)
        else:
            return False, f"Unknown task type: {task_type}"
    
    async def _analyze_requirements(self, context: AgentContext) -> Tuple[bool, Any]:
        """Analyze project requirements and create initial understanding"""
        logger.info("Analyzing project requirements")
        
        requirements = context.task.description
        
        # Get relevant memories about similar projects
        memories = self.get_memory_context(requirements, limit=10)
        
        analysis = {
            "requirements": requirements,
            "identified_components": [],
            "suggested_architecture": {},
            "potential_challenges": [],
            "similar_projects": memories
        }
        
        # If we have an LLM client, use it for deeper analysis
        if self.llm_client:
            prompt = self._build_analysis_prompt(requirements, memories)
            # LLM analysis would go here
            pass
        else:
            # Basic analysis without LLM
            analysis["identified_components"] = self._extract_components(requirements)
            analysis["suggested_architecture"] = self._suggest_architecture(requirements)
        
        return True, analysis
    
    async def _create_project_plan(self, context: AgentContext) -> Tuple[bool, Any]:
        """Create a detailed project plan"""
        logger.info("Creating project plan")
        
        project_description = context.task.description
        analysis = context.shared_memory.get("analysis", {})
        
        # Create plan
        plan = ProjectPlan(project_description)
        
        # Define tasks based on analysis
        task_definitions = self._define_tasks(project_description, analysis)
        
        # Create task objects and add to plan
        for task_def in task_definitions:
            task = Task(
                id=task_def["id"],
                type=task_def["type"],
                description=task_def["description"],
                priority=task_def.get("priority", 1),
                metadata=task_def.get("metadata", {})
            )
            
            plan.add_task(
                task,
                dependencies=task_def.get("dependencies", []),
                suggested_agent=task_def.get("agent_type")
            )
        
        # Analyze parallelism
        plan.analyze_parallelism()
        
        self.current_plan = plan
        
        # Store plan in memory
        if self.memory_service:
            self.memory_service.add_memory(
                messages=[
                    {"role": "system", "content": "Project plan created"},
                    {"role": "assistant", "content": json.dumps({
                        "description": plan.description,
                        "task_count": len(plan.tasks),
                        "parallel_groups": len(plan.parallel_groups)
                    })}
                ],
                agent_id=self.agent_id
            )
        
        return True, {
            "plan": plan,
            "task_count": len(plan.tasks),
            "parallel_groups": plan.parallel_groups,
            "estimated_duration": self._estimate_duration(plan)
        }
    
    async def _orchestrate_execution(self, context: AgentContext) -> Tuple[bool, Any]:
        """Orchestrate the execution of the project plan"""
        if not self.current_plan:
            return False, "No project plan available"
        
        logger.info("Starting plan orchestration")
        
        execution_results = {
            "completed_tasks": [],
            "failed_tasks": [],
            "execution_time": 0,
            "parallel_executions": []
        }
        
        start_time = datetime.now()
        
        # Execute tasks in parallel groups
        for group_idx, task_group in enumerate(self.current_plan.parallel_groups):
            logger.info(f"Executing parallel group {group_idx + 1}/{len(self.current_plan.parallel_groups)}")
            
            # Get tasks for this group
            tasks = [
                task for task in self.current_plan.tasks
                if task.id in task_group
            ]
            
            # This is where we would dispatch to actual agents
            # For now, we'll simulate the execution
            group_results = await self._execute_task_group(tasks, context)
            
            execution_results["parallel_executions"].append({
                "group": group_idx + 1,
                "tasks": len(tasks),
                "results": group_results
            })
            
            # Check for failures
            for task_id, result in group_results.items():
                if result["success"]:
                    execution_results["completed_tasks"].append(task_id)
                else:
                    execution_results["failed_tasks"].append(task_id)
        
        execution_results["execution_time"] = (datetime.now() - start_time).total_seconds()
        
        # Store execution results
        self.execution_history.append(execution_results)
        
        return True, execution_results
    
    def _extract_components(self, requirements: str) -> List[str]:
        """Extract components from requirements (basic implementation)"""
        # This would be enhanced with NLP/LLM
        components = []
        
        # Look for common patterns
        if "api" in requirements.lower():
            components.append("API Layer")
        if "database" in requirements.lower():
            components.append("Database")
        if "frontend" in requirements.lower() or "ui" in requirements.lower():
            components.append("Frontend")
        if "auth" in requirements.lower():
            components.append("Authentication")
        if "test" in requirements.lower():
            components.append("Testing")
        
        return components
    
    def _suggest_architecture(self, requirements: str) -> Dict[str, Any]:
        """Suggest architecture based on requirements"""
        return {
            "pattern": "microservices" if "scale" in requirements.lower() else "monolithic",
            "layers": ["presentation", "business", "data"],
            "considerations": ["scalability", "maintainability", "security"]
        }
    
    def _define_tasks(
        self,
        description: str,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Define tasks based on project description and analysis"""
        tasks = []
        
        # Always start with architecture planning
        tasks.append({
            "id": "task_001",
            "type": "architecture",
            "description": "Design system architecture and create technical specifications",
            "priority": 1,
            "agent_type": "architect",
            "dependencies": []
        })
        
        # Setup development environment
        tasks.append({
            "id": "task_002",
            "type": "setup",
            "description": "Setup development environment and project structure",
            "priority": 1,
            "agent_type": "devops",
            "dependencies": ["task_001"]
        })
        
        # Core implementation tasks
        components = analysis.get("identified_components", [])
        for idx, component in enumerate(components):
            tasks.append({
                "id": f"task_{idx + 3:03d}",
                "type": "implementation",
                "description": f"Implement {component}",
                "priority": 2,
                "agent_type": "developer",
                "dependencies": ["task_002"]
            })
        
        # Testing
        tasks.append({
            "id": f"task_{len(components) + 3:03d}",
            "type": "testing",
            "description": "Create and run comprehensive test suite",
            "priority": 3,
            "agent_type": "tester",
            "dependencies": [f"task_{idx + 3:03d}" for idx in range(len(components))]
        })
        
        # Security audit
        tasks.append({
            "id": f"task_{len(components) + 4:03d}",
            "type": "security",
            "description": "Perform security audit and implement fixes",
            "priority": 3,
            "agent_type": "security",
            "dependencies": [f"task_{idx + 3:03d}" for idx in range(len(components))]
        })
        
        return tasks
    
    def _estimate_duration(self, plan: ProjectPlan) -> Dict[str, Any]:
        """Estimate project duration"""
        # Simple estimation based on task count and parallelism
        avg_task_duration = 30  # minutes
        parallel_factor = 0.6  # Efficiency factor for parallel execution
        
        total_sequential = len(plan.tasks) * avg_task_duration
        total_parallel = len(plan.parallel_groups) * avg_task_duration * parallel_factor
        
        return {
            "sequential_estimate": f"{total_sequential} minutes",
            "parallel_estimate": f"{total_parallel:.0f} minutes",
            "speedup": f"{total_sequential / total_parallel:.1f}x"
        }
    
    async def _execute_task_group(
        self,
        tasks: List[Task],
        context: AgentContext
    ) -> Dict[str, Dict[str, Any]]:
        """Execute a group of tasks (placeholder for actual agent dispatch)"""
        results = {}
        
        # In real implementation, this would dispatch to actual agents
        for task in tasks:
            # Simulate task execution
            await asyncio.sleep(0.1)  # Simulate work
            
            results[task.id] = {
                "success": True,
                "agent": self.current_plan.agent_assignments.get(task.id, "unknown"),
                "duration": 0.1,
                "result": f"Completed: {task.description}"
            }
        
        return results
    
    def _build_analysis_prompt(
        self,
        requirements: str,
        memories: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for LLM analysis"""
        memory_context = "\n".join([
            f"- {mem.get('memory', '')}" for mem in memories[:5]
        ])
        
        return f"""
        Analyze the following project requirements and provide:
        1. Identified components and modules
        2. Suggested architecture pattern
        3. Potential challenges and solutions
        4. Required agent types for implementation
        
        Requirements:
        {requirements}
        
        Similar projects context:
        {memory_context}
        
        Provide structured analysis in JSON format.
        """