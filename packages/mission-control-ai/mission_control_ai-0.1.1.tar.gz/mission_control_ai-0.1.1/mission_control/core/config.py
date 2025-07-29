"""Configuration management for Mission Control"""

from typing import Dict, List, Optional, Any
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os


class AgentConfig(BaseSettings):
    """Configuration for individual agents"""
    
    name: str
    type: str
    model: str = "claude-3-sonnet-20240229"
    temperature: float = 0.7
    max_tokens: int = 4096
    capabilities: List[str] = Field(default_factory=list)
    memory_namespace: Optional[str] = None
    
    class Config:
        env_prefix = "AGENT_"


class MemoryConfig(BaseSettings):
    """Memory service configuration"""
    
    provider: str = "mem0"
    api_key: Optional[str] = Field(default=None, env="MEM0_API_KEY")
    local_storage_path: Path = Path("./memory_storage")
    vector_db_type: str = "chromadb"
    enable_collective_memory: bool = True
    enable_agent_memory: bool = True
    
    class Config:
        env_prefix = "MEMORY_"


class OrchestratorConfig(BaseSettings):
    """Orchestrator configuration"""
    
    max_concurrent_agents: int = 10
    task_timeout: int = 3600  # 1 hour
    retry_attempts: int = 3
    enable_monitoring: bool = True
    monitoring_port: int = 8080
    
    class Config:
        env_prefix = "ORCHESTRATOR_"


class LLMConfig(BaseSettings):
    """LLM configuration"""
    
    provider: str = Field(default="anthropic", env="LLM_PROVIDER")
    max_tokens: int = Field(default=4096, env="MAX_TOKENS")
    token_budget: int = Field(default=0, env="TOKEN_BUDGET")  # 0 = unlimited
    token_warn_percentage: int = Field(default=80, env="TOKEN_WARN_PERCENTAGE")
    context_window: int = Field(default=0, env="CONTEXT_WINDOW")  # 0 = model default
    
    # Ollama settings
    ollama_model: str = Field(default="llama2", env="OLLAMA_MODEL")
    ollama_host: str = Field(default="http://localhost:11434", env="OLLAMA_HOST")
    
    class Config:
        env_prefix = "LLM_"


class MissionConfig(BaseSettings):
    """Main configuration for Mission Control"""
    
    project_name: str = "mission-control"
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Sub-configurations
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    
    # Agent profiles
    agent_profiles: Dict[str, AgentConfig] = Field(default_factory=dict)
    
    # API Keys
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_default_agent_profiles()
    
    def _load_default_agent_profiles(self):
        """Load default agent profiles"""
        default_profiles = {
            "architect": AgentConfig(
                name="Architect",
                type="planning",
                capabilities=["system_design", "architecture_planning", "dependency_analysis"],
                memory_namespace="architect_knowledge"
            ),
            "developer": AgentConfig(
                name="Developer",
                type="implementation",
                capabilities=["code_generation", "refactoring", "optimization"],
                memory_namespace="developer_knowledge"
            ),
            "tester": AgentConfig(
                name="Tester",
                type="testing",
                capabilities=["unit_testing", "integration_testing", "test_generation"],
                memory_namespace="tester_knowledge"
            ),
            "debugger": AgentConfig(
                name="Debugger",
                type="debugging",
                capabilities=["error_analysis", "bug_fixing", "performance_debugging"],
                memory_namespace="debugger_knowledge"
            ),
            "devops": AgentConfig(
                name="DevOps",
                type="deployment",
                capabilities=["environment_setup", "ci_cd", "monitoring_setup"],
                memory_namespace="devops_knowledge"
            ),
            "security": AgentConfig(
                name="Security",
                type="security",
                capabilities=["security_audit", "vulnerability_scanning", "secure_coding"],
                memory_namespace="security_knowledge"
            ),
        }
        
        # Merge with any provided profiles
        for key, profile in default_profiles.items():
            if key not in self.agent_profiles:
                self.agent_profiles[key] = profile