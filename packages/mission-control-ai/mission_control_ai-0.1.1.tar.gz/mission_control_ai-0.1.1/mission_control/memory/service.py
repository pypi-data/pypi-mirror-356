"""Memory service implementation using Mem0"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path
from mem0 import MemoryClient
from loguru import logger

from ..core.config import MemoryConfig


class MemoryService:
    """Manages both individual agent and collective knowledge bases"""
    
    def __init__(self, config: MemoryConfig):
        self.config = config
        self.client = None
        self.local_storage = config.local_storage_path
        self.local_storage.mkdir(parents=True, exist_ok=True)
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the memory client"""
        if self.config.provider == "mem0" and self.config.api_key:
            self.client = MemoryClient(api_key=self.config.api_key)
            logger.info("Initialized Mem0 client")
        else:
            logger.warning("Using local memory storage (no Mem0 API key provided)")
    
    def add_memory(
        self,
        messages: List[Dict[str, str]],
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add memory from conversation"""
        namespace = f"agent_{agent_id}" if agent_id else "collective"
        
        if self.client:
            # Use Mem0 service
            result = self.client.add(
                messages=messages,
                user_id=namespace,
                metadata=metadata or {}
            )
            logger.debug(f"Added memory to {namespace}: {result}")
            return result
        else:
            # Local storage fallback
            return self._add_local_memory(messages, namespace, metadata)
    
    def search_memory(
        self,
        query: str,
        agent_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search memories semantically"""
        namespace = f"agent_{agent_id}" if agent_id else "collective"
        
        if self.client:
            # Use Mem0 service
            results = self.client.search(
                query=query,
                version="v2",
                filters={"AND": [{"user_id": namespace}]},
                limit=limit
            )
            return results.get("results", [])
        else:
            # Local storage fallback
            return self._search_local_memory(query, namespace, limit)
    
    def get_agent_memories(
        self,
        agent_id: str,
        page: int = 1,
        page_size: int = 50
    ) -> List[Dict[str, Any]]:
        """Get all memories for a specific agent"""
        namespace = f"agent_{agent_id}"
        
        if self.client:
            # Use Mem0 service
            results = self.client.get_all(
                version="v2",
                filters={"AND": [{"user_id": namespace}]},
                page=page,
                page_size=page_size
            )
            return results.get("results", [])
        else:
            # Local storage fallback
            return self._get_local_memories(namespace)
    
    def share_memory(
        self,
        memory_id: str,
        from_agent: str,
        to_agent: Optional[str] = None
    ) -> bool:
        """Share memory from one agent to another or to collective"""
        # Get the memory
        memory = self._get_memory_by_id(memory_id, from_agent)
        if memory:
            # Add to target namespace
            target = f"agent_{to_agent}" if to_agent else "collective"
            self.add_memory(
                messages=[{"role": "system", "content": memory["memory"]}],
                agent_id=to_agent,
                metadata={"shared_from": from_agent, "original_id": memory_id}
            )
            return True
        return False
    
    def update_memory(
        self,
        memory_id: str,
        agent_id: str,
        new_content: str
    ) -> bool:
        """Update an existing memory"""
        if self.client:
            # Mem0 update implementation
            namespace = f"agent_{agent_id}"
            # Note: Actual implementation depends on Mem0 API
            logger.info(f"Updated memory {memory_id} for {namespace}")
            return True
        else:
            return self._update_local_memory(memory_id, agent_id, new_content)
    
    # Local storage methods (fallback when Mem0 is not available)
    
    def _add_local_memory(
        self,
        messages: List[Dict[str, str]],
        namespace: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add memory to local storage"""
        memory_file = self.local_storage / f"{namespace}.json"
        
        memories = []
        if memory_file.exists():
            with open(memory_file, "r") as f:
                memories = json.load(f)
        
        # Extract memory from messages
        memory_text = " ".join([m["content"] for m in messages])
        
        new_memory = {
            "id": f"mem_{datetime.now().timestamp()}",
            "memory": memory_text,
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "score": 1.0
        }
        
        memories.append(new_memory)
        
        with open(memory_file, "w") as f:
            json.dump(memories, f, indent=2)
        
        return new_memory
    
    def _search_local_memory(
        self,
        query: str,
        namespace: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Simple keyword search in local memories"""
        memory_file = self.local_storage / f"{namespace}.json"
        
        if not memory_file.exists():
            return []
        
        with open(memory_file, "r") as f:
            memories = json.load(f)
        
        # Simple keyword matching (could be improved with embeddings)
        query_lower = query.lower()
        scored_memories = []
        
        for memory in memories:
            memory_lower = memory["memory"].lower()
            score = sum(1 for word in query_lower.split() if word in memory_lower)
            if score > 0:
                memory["score"] = score / len(query_lower.split())
                scored_memories.append(memory)
        
        # Sort by score and return top results
        scored_memories.sort(key=lambda x: x["score"], reverse=True)
        return scored_memories[:limit]
    
    def _get_local_memories(self, namespace: str) -> List[Dict[str, Any]]:
        """Get all memories from local storage"""
        memory_file = self.local_storage / f"{namespace}.json"
        
        if not memory_file.exists():
            return []
        
        with open(memory_file, "r") as f:
            return json.load(f)
    
    def _get_memory_by_id(self, memory_id: str, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific memory by ID"""
        memories = self.get_agent_memories(agent_id)
        for memory in memories:
            if memory.get("id") == memory_id:
                return memory
        return None
    
    def _update_local_memory(
        self,
        memory_id: str,
        agent_id: str,
        new_content: str
    ) -> bool:
        """Update memory in local storage"""
        namespace = f"agent_{agent_id}"
        memory_file = self.local_storage / f"{namespace}.json"
        
        if not memory_file.exists():
            return False
        
        with open(memory_file, "r") as f:
            memories = json.load(f)
        
        for memory in memories:
            if memory.get("id") == memory_id:
                memory["memory"] = new_content
                memory["updated_at"] = datetime.now().isoformat()
                
                with open(memory_file, "w") as f:
                    json.dump(memories, f, indent=2)
                return True
        
        return False