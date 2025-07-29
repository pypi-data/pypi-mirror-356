"""Main orchestrator for Mission Control"""

import asyncio
from typing import Dict, List, Optional, Any, Type
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

from ..agents.base import BaseAgent, Task, AgentContext
from ..agents.root_agent import RootAgent
from ..agents.specialized_agents import (
    ArchitectAgent,
    DeveloperAgent,
    TesterAgent,
    DebuggerAgent,
    DevOpsAgent,
    SecurityAgent
)
from ..memory.service import MemoryService
from ..core.config import MissionConfig, AgentConfig
from ..utils.monitoring import MissionMonitor


class AgentPool:
    """Manages a pool of agents"""
    
    def __init__(self, max_agents: int = 10):
        self.max_agents = max_agents
        self.active_agents: Dict[str, BaseAgent] = {}
        self.available_agents: Dict[str, Type[BaseAgent]] = {
            "root": RootAgent,
            "architect": ArchitectAgent,
            "developer": DeveloperAgent,
            "tester": TesterAgent,
            "debugger": DebuggerAgent,
            "devops": DevOpsAgent,
            "security": SecurityAgent
        }
        self.agent_locks: Dict[str, asyncio.Lock] = {}
    
    async def get_agent(
        self,
        agent_type: str,
        config: AgentConfig,
        memory_service: Optional[MemoryService] = None
    ) -> BaseAgent:
        """Get or create an agent of the specified type"""
        agent_key = f"{agent_type}_{config.name}"
        
        if agent_key not in self.agent_locks:
            self.agent_locks[agent_key] = asyncio.Lock()
        
        async with self.agent_locks[agent_key]:
            if agent_key in self.active_agents:
                return self.active_agents[agent_key]
            
            if len(self.active_agents) >= self.max_agents:
                raise RuntimeError(f"Agent pool limit reached ({self.max_agents})")
            
            # Create new agent
            agent_class = self.available_agents.get(agent_type)
            if not agent_class:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            agent = agent_class(config, memory_service)
            self.active_agents[agent_key] = agent
            
            return agent
    
    def release_agent(self, agent_key: str):
        """Release an agent back to the pool"""
        if agent_key in self.active_agents:
            del self.active_agents[agent_key]


class TaskQueue:
    """Manages task execution queue"""
    
    def __init__(self):
        self.pending_tasks: List[Task] = []
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
        self._lock = asyncio.Lock()
    
    async def add_task(self, task: Task):
        """Add a task to the queue"""
        async with self._lock:
            self.pending_tasks.append(task)
            logger.debug(f"Added task {task.id} to queue")
    
    async def get_ready_tasks(self, completed_ids: List[str]) -> List[Task]:
        """Get tasks that are ready to execute"""
        async with self._lock:
            ready_tasks = []
            
            for task in self.pending_tasks:
                # Check if all dependencies are completed
                if all(dep in completed_ids for dep in task.dependencies):
                    ready_tasks.append(task)
            
            # Remove ready tasks from pending
            for task in ready_tasks:
                self.pending_tasks.remove(task)
                self.running_tasks[task.id] = task
            
            return ready_tasks
    
    async def mark_completed(self, task_id: str, success: bool = True):
        """Mark a task as completed"""
        async with self._lock:
            if task_id in self.running_tasks:
                task = self.running_tasks.pop(task_id)
                
                if success:
                    self.completed_tasks.append(task)
                else:
                    self.failed_tasks.append(task)


class MissionOrchestrator:
    """Main orchestrator for managing missions"""
    
    def __init__(self, config: MissionConfig):
        self.config = config
        self.memory_service = MemoryService(config.memory)
        self.agent_pool = AgentPool(config.orchestrator.max_concurrent_agents)
        self.task_queue = TaskQueue()
        self.monitor = MissionMonitor() if config.orchestrator.enable_monitoring else None
        self.executor = ThreadPoolExecutor(max_workers=config.orchestrator.max_concurrent_agents)
        
        # Mission state
        self.current_mission: Optional[Dict[str, Any]] = None
        self.mission_history: List[Dict[str, Any]] = []
        
        logger.info("Mission Orchestrator initialized")
    
    async def start_mission(self, mission_description: str) -> Dict[str, Any]:
        """Start a new mission"""
        logger.info(f"Starting new mission: {mission_description}")
        
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_mission = {
            "id": mission_id,
            "description": mission_description,
            "status": "planning",
            "started_at": datetime.now(),
            "completed_at": None,
            "results": {}
        }
        
        if self.monitor:
            self.monitor.start_mission(mission_id)
        
        try:
            # Phase 1: Analysis
            analysis_result = await self._execute_analysis_phase(mission_description)
            self.current_mission["results"]["analysis"] = analysis_result
            
            # Phase 2: Planning
            plan_result = await self._execute_planning_phase(mission_description, analysis_result)
            self.current_mission["results"]["plan"] = plan_result
            
            # Phase 3: Execution
            execution_result = await self._execute_implementation_phase(plan_result)
            self.current_mission["results"]["execution"] = execution_result
            
            # Phase 4: Testing & Validation
            validation_result = await self._execute_validation_phase(execution_result)
            self.current_mission["results"]["validation"] = validation_result
            
            # Phase 5: Deployment Setup
            deployment_result = await self._execute_deployment_phase()
            self.current_mission["results"]["deployment"] = deployment_result
            
            self.current_mission["status"] = "completed"
            self.current_mission["completed_at"] = datetime.now()
            
            # Store mission in history
            self.mission_history.append(self.current_mission)
            
            # Store in collective memory
            self.memory_service.add_memory(
                messages=[
                    {"role": "system", "content": f"Mission completed: {mission_description}"},
                    {"role": "assistant", "content": json.dumps(self.current_mission["results"])}
                ],
                metadata={"mission_id": mission_id}
            )
            
            return self.current_mission
            
        except Exception as e:
            logger.error(f"Mission failed: {str(e)}")
            self.current_mission["status"] = "failed"
            self.current_mission["error"] = str(e)
            self.current_mission["completed_at"] = datetime.now()
            
            if self.monitor:
                self.monitor.record_error(str(e))
            
            raise
    
    async def _execute_analysis_phase(self, description: str) -> Dict[str, Any]:
        """Execute the analysis phase"""
        logger.info("Executing analysis phase")
        
        # Get root agent for analysis
        root_config = self.config.agent_profiles.get("root", AgentConfig(
            name="RootAnalyzer",
            type="root"
        ))
        
        root_agent = await self.agent_pool.get_agent("root", root_config, self.memory_service)
        
        # Create analysis task
        analysis_task = Task(
            id="analysis_001",
            type="analysis",
            description=description,
            priority=1
        )
        
        context = AgentContext(task=analysis_task)
        
        # Execute analysis
        success, result = await root_agent.run(context)
        
        if not success:
            raise RuntimeError(f"Analysis phase failed: {result}")
        
        return result
    
    async def _execute_planning_phase(
        self,
        description: str,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the planning phase"""
        logger.info("Executing planning phase")
        
        # Get root agent for planning
        root_config = self.config.agent_profiles.get("root", AgentConfig(
            name="RootPlanner",
            type="root"
        ))
        
        root_agent = await self.agent_pool.get_agent("root", root_config, self.memory_service)
        
        # Create planning task
        planning_task = Task(
            id="planning_001",
            type="planning",
            description=description,
            priority=1
        )
        
        context = AgentContext(
            task=planning_task,
            shared_memory={"analysis": analysis}
        )
        
        # Execute planning
        success, result = await root_agent.run(context)
        
        if not success:
            raise RuntimeError(f"Planning phase failed: {result}")
        
        # Add tasks to queue
        plan = result.get("plan")
        if plan:
            for task in plan.tasks:
                await self.task_queue.add_task(task)
        
        return result
    
    async def _execute_implementation_phase(
        self,
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the implementation phase"""
        logger.info("Executing implementation phase")
        
        completed_task_ids = []
        execution_results = []
        
        # Get task groups from plan
        parallel_groups = plan.get("plan").parallel_groups if plan.get("plan") else []
        
        for group_idx, task_group in enumerate(parallel_groups):
            logger.info(f"Executing task group {group_idx + 1}/{len(parallel_groups)}")
            
            # Get ready tasks
            ready_tasks = await self.task_queue.get_ready_tasks(completed_task_ids)
            
            # Execute tasks in parallel
            group_results = await self._execute_task_group(ready_tasks)
            
            # Process results
            for task_id, result in group_results.items():
                if result["success"]:
                    completed_task_ids.append(task_id)
                    await self.task_queue.mark_completed(task_id, True)
                else:
                    await self.task_queue.mark_completed(task_id, False)
                    
                    # Handle failure - send to debugger
                    await self._handle_task_failure(task_id, result)
            
            execution_results.append({
                "group": group_idx + 1,
                "results": group_results
            })
        
        return {
            "total_tasks": len(plan.get("plan").tasks) if plan.get("plan") else 0,
            "completed_tasks": len(completed_task_ids),
            "failed_tasks": len(self.task_queue.failed_tasks),
            "execution_groups": execution_results
        }
    
    async def _execute_task_group(self, tasks: List[Task]) -> Dict[str, Dict[str, Any]]:
        """Execute a group of tasks in parallel"""
        results = {}
        
        # Create coroutines for each task
        coroutines = []
        for task in tasks:
            coroutines.append(self._execute_single_task(task))
        
        # Execute in parallel
        task_results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # Process results
        for task, result in zip(tasks, task_results):
            if isinstance(result, Exception):
                results[task.id] = {
                    "success": False,
                    "error": str(result),
                    "agent": task.assigned_agent
                }
            else:
                results[task.id] = result
        
        return results
    
    async def _execute_single_task(self, task: Task) -> Dict[str, Any]:
        """Execute a single task with the appropriate agent"""
        logger.debug(f"Executing task {task.id}: {task.description}")
        
        # Determine agent type
        agent_type = task.metadata.get("agent_type", task.type)
        
        # Map task type to agent type if needed
        type_mapping = {
            "architecture": "architect",
            "implementation": "developer",
            "coding": "developer",
            "testing": "tester",
            "debugging": "debugger",
            "setup": "devops",
            "deployment": "devops",
            "security": "security"
        }
        
        agent_type = type_mapping.get(task.type, agent_type)
        
        # Get agent configuration
        agent_config = self.config.agent_profiles.get(
            agent_type,
            AgentConfig(name=agent_type.title(), type=agent_type)
        )
        
        # Get agent from pool
        agent = await self.agent_pool.get_agent(agent_type, agent_config, self.memory_service)
        
        # Create context
        context = AgentContext(
            task=task,
            shared_memory=self._get_shared_memory()
        )
        
        # Execute task
        try:
            success, result = await agent.run(context)
            
            return {
                "success": success,
                "result": result,
                "agent": agent_type,
                "duration": (datetime.now() - task.created_at).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Task {task.id} failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": agent_type
            }
    
    async def _handle_task_failure(self, task_id: str, result: Dict[str, Any]):
        """Handle a failed task by sending to debugger"""
        logger.info(f"Handling failure for task {task_id}")
        
        # Create debugging task
        debug_task = Task(
            id=f"debug_{task_id}",
            type="debugging",
            description=f"Debug failure in task {task_id}",
            priority=0,  # High priority
            metadata={
                "original_task_id": task_id,
                "error": result.get("error", "Unknown error"),
                "agent_type": "debugger"
            }
        )
        
        # Get debugger agent
        debugger_config = self.config.agent_profiles.get(
            "debugger",
            AgentConfig(name="Debugger", type="debugger")
        )
        
        debugger = await self.agent_pool.get_agent("debugger", debugger_config, self.memory_service)
        
        # Execute debugging
        context = AgentContext(
            task=debug_task,
            shared_memory={"failed_task_result": result}
        )
        
        success, debug_result = await debugger.run(context)
        
        if success:
            logger.info(f"Debugging analysis complete for task {task_id}")
            # Store debugging results
            self.memory_service.add_memory(
                messages=[
                    {"role": "system", "content": f"Debug analysis for task {task_id}"},
                    {"role": "assistant", "content": json.dumps(debug_result)}
                ],
                agent_id="debugger"
            )
    
    async def _execute_validation_phase(
        self,
        execution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute validation and testing phase"""
        logger.info("Executing validation phase")
        
        # Create testing task
        test_task = Task(
            id="validation_001",
            type="testing",
            description="Run comprehensive test suite",
            priority=1
        )
        
        # Get tester agent
        tester_config = self.config.agent_profiles.get(
            "tester",
            AgentConfig(name="Tester", type="tester")
        )
        
        tester = await self.agent_pool.get_agent("tester", tester_config, self.memory_service)
        
        context = AgentContext(
            task=test_task,
            shared_memory={"execution_result": execution_result}
        )
        
        success, test_result = await tester.run(context)
        
        # Run security audit
        security_task = Task(
            id="security_001",
            type="security",
            description="Perform security audit",
            priority=1
        )
        
        security_config = self.config.agent_profiles.get(
            "security",
            AgentConfig(name="Security", type="security")
        )
        
        security_agent = await self.agent_pool.get_agent("security", security_config, self.memory_service)
        
        security_context = AgentContext(task=security_task)
        security_success, security_result = await security_agent.run(security_context)
        
        return {
            "testing": test_result if success else {"error": "Testing failed"},
            "security": security_result if security_success else {"error": "Security audit failed"},
            "overall_status": "passed" if success and security_success else "failed"
        }
    
    async def _execute_deployment_phase(self) -> Dict[str, Any]:
        """Execute deployment setup phase"""
        logger.info("Executing deployment phase")
        
        # Create deployment task
        deploy_task = Task(
            id="deployment_001",
            type="setup",
            description="Setup deployment environment",
            priority=1,
            metadata={"setup_type": "deployment"}
        )
        
        # Get DevOps agent
        devops_config = self.config.agent_profiles.get(
            "devops",
            AgentConfig(name="DevOps", type="devops")
        )
        
        devops = await self.agent_pool.get_agent("devops", devops_config, self.memory_service)
        
        context = AgentContext(task=deploy_task)
        
        success, result = await devops.run(context)
        
        return result if success else {"error": "Deployment setup failed"}
    
    def _get_shared_memory(self) -> Dict[str, Any]:
        """Get current shared memory state"""
        shared_memory = {}
        
        if self.current_mission:
            shared_memory["mission_id"] = self.current_mission["id"]
            shared_memory["results"] = self.current_mission.get("results", {})
        
        return shared_memory
    
    async def get_mission_status(self) -> Dict[str, Any]:
        """Get current mission status"""
        if not self.current_mission:
            return {"status": "no_active_mission"}
        
        return {
            "mission_id": self.current_mission["id"],
            "status": self.current_mission["status"],
            "progress": {
                "pending_tasks": len(self.task_queue.pending_tasks),
                "running_tasks": len(self.task_queue.running_tasks),
                "completed_tasks": len(self.task_queue.completed_tasks),
                "failed_tasks": len(self.task_queue.failed_tasks)
            },
            "active_agents": list(self.agent_pool.active_agents.keys()),
            "duration": (
                datetime.now() - self.current_mission["started_at"]
            ).total_seconds() if self.current_mission["started_at"] else 0
        }
    
    async def shutdown(self):
        """Shutdown the orchestrator"""
        logger.info("Shutting down Mission Orchestrator")
        
        # Wait for running tasks
        while self.task_queue.running_tasks:
            await asyncio.sleep(0.5)
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        # Close monitoring
        if self.monitor:
            self.monitor.stop()
        
        logger.info("Mission Orchestrator shutdown complete")