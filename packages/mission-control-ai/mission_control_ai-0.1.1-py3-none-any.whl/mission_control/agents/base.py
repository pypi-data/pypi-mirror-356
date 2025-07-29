"""Base agent class for all specialized agents"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncio
from loguru import logger
from pydantic import BaseModel, Field

from ..memory.service import MemoryService
from ..core.config import AgentConfig


class Task(BaseModel):
    """Task model for agents"""
    id: str
    type: str
    description: str
    dependencies: List[str] = Field(default_factory=list)
    priority: int = 1
    status: str = "pending"  # pending, in_progress, completed, failed
    assigned_agent: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentContext(BaseModel):
    """Context information for agent execution"""
    task: Task
    shared_memory: Dict[str, Any] = Field(default_factory=dict)
    previous_results: Dict[str, Any] = Field(default_factory=dict)
    environment: Dict[str, str] = Field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(
        self,
        config: AgentConfig,
        memory_service: Optional[MemoryService] = None
    ):
        self.config = config
        self.name = config.name
        self.type = config.type
        self.capabilities = config.capabilities
        self.memory_service = memory_service
        self.agent_id = f"{self.type}_{self.name.lower().replace(' ', '_')}"
        
        logger.info(f"Initialized {self.name} agent with capabilities: {self.capabilities}")
    
    @abstractmethod
    async def execute(self, context: AgentContext) -> Tuple[bool, Any]:
        """
        Execute the agent's task
        
        Returns:
            Tuple of (success: bool, result: Any)
        """
        pass
    
    @abstractmethod
    def can_handle(self, task: Task) -> bool:
        """Check if this agent can handle the given task"""
        pass
    
    async def pre_execute(self, context: AgentContext) -> None:
        """Pre-execution hook for setup"""
        logger.info(f"{self.name} starting task: {context.task.description}")
        
        # Load relevant memories
        if self.memory_service:
            memories = self.memory_service.search_memory(
                query=context.task.description,
                agent_id=self.agent_id,
                limit=5
            )
            if memories:
                logger.debug(f"Found {len(memories)} relevant memories")
                context.shared_memory["relevant_memories"] = memories
    
    async def post_execute(
        self,
        context: AgentContext,
        success: bool,
        result: Any
    ) -> None:
        """Post-execution hook for cleanup and memory storage"""
        logger.info(f"{self.name} completed task with status: {'success' if success else 'failed'}")
        
        # Store execution memory
        if self.memory_service:
            memory_content = {
                "task": context.task.description,
                "success": success,
                "result_summary": str(result)[:500] if success else None,
                "error": context.task.error,
                "timestamp": datetime.now().isoformat()
            }
            
            self.memory_service.add_memory(
                messages=[
                    {"role": "system", "content": f"Task: {context.task.description}"},
                    {"role": "assistant", "content": f"Result: {memory_content}"}
                ],
                agent_id=self.agent_id,
                metadata={"task_id": context.task.id}
            )
    
    async def run(self, context: AgentContext) -> Tuple[bool, Any]:
        """Main execution method with pre/post hooks"""
        try:
            # Pre-execution
            await self.pre_execute(context)
            
            # Main execution
            success, result = await self.execute(context)
            
            # Update task status
            context.task.status = "completed" if success else "failed"
            context.task.result = result
            context.task.completed_at = datetime.now()
            
            # Post-execution
            await self.post_execute(context, success, result)
            
            return success, result
            
        except Exception as e:
            logger.error(f"{self.name} encountered error: {str(e)}")
            context.task.status = "failed"
            context.task.error = str(e)
            context.task.completed_at = datetime.now()
            
            await self.post_execute(context, False, None)
            return False, str(e)
    
    def get_memory_context(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve relevant memories for the agent"""
        if not self.memory_service:
            return []
        
        return self.memory_service.search_memory(
            query=query,
            agent_id=self.agent_id,
            limit=limit
        )
    
    def share_knowledge(
        self,
        knowledge: str,
        target_agent: Optional[str] = None
    ) -> bool:
        """Share knowledge with another agent or collective memory"""
        if not self.memory_service:
            return False
        
        self.memory_service.add_memory(
            messages=[
                {"role": "system", "content": "Shared knowledge"},
                {"role": "assistant", "content": knowledge}
            ],
            agent_id=target_agent,
            metadata={"shared_by": self.agent_id}
        )
        return True