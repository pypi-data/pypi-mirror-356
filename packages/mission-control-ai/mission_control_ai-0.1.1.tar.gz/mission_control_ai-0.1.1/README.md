# Mission Control

AI Development Workflow Orchestration System

Mission Control is a Python package that orchestrates AI agents to improve development workflows. It implements a human-in-the-loop terminal interface that acts as the communication point to a root agent, which builds detailed project plans, manages parallel and dependent tasks, and coordinates specialized agents.

## Features

- **Root Agent Orchestration**: Intelligent project planning and task allocation
- **Specialized Agent Profiles**: Architecture, Development, Testing, Debugging, DevOps, and Security agents
- **Memory Management**: Individual and collective knowledge bases using Mem0
- **Parallel Execution**: Smart dependency analysis and parallel task execution
- **Human-in-the-Loop**: Interactive terminal interface for mission control
- **Error Recovery**: Automatic bug detection and specialized debugging agents
- **Local Testing Environment**: Automated setup for human review
- **Flexible Model Support**: Use Anthropic, OpenAI, or local models via Ollama
- **Token Management**: Configure limits and budgets for API usage

## Architecture

Mission Control follows a staged execution model inspired by SPARC:

1. **Analysis Phase**: Analyze project requirements and identify components
2. **Planning Phase**: Create detailed project plan with task dependencies
3. **Execution Phase**: Deploy specialized agents in parallel groups
4. **Validation Phase**: Comprehensive testing and security audits
5. **Deployment Phase**: Setup local testing environment

## Installation

```bash
pip install mission-control-ai
```

Or install from source:

```bash
git clone https://github.com/bluearchio/mission-control.git
cd mission-control
pip install -e .
```

## Quick Start

### 1. Initial Setup

After installation, configure Mission Control with the interactive setup:

```bash
mission-control config
```

This will guide you through:
- Setting up API keys (Anthropic, OpenAI, Mem0)
- Configuring local models (Ollama)
- Setting token limits and budgets
- Customizing agent profiles
- Choosing memory storage options

### 2. Initialize a Project

```bash
mission-control init my-project
cd my-project
```

### 3. Start Mission Control

```bash
mission-control run
```

## Configuration

### Using the Configuration UI

Mission Control provides an interactive configuration interface:

```bash
mission-control config
```

Available configuration options:
1. **API Keys**: Configure Anthropic, OpenAI, and Mem0 API keys
2. **Local Models**: Set up Ollama for local inference
3. **Token Limits**: Set max tokens per request and total budgets
4. **Memory Service**: Choose between local storage, Mem0, or vector databases
5. **Agent Profiles**: Customize agent models, temperature, and capabilities
6. **Import/Export**: Save and share configurations

### Using Ollama for Local Models

To use local models instead of API-based services:

1. Install Ollama from https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Configure in Mission Control: `mission-control config`
4. Select "Configure Local Models"

### Environment Variables

You can also configure Mission Control using environment variables:

```bash
export ANTHROPIC_API_KEY=your-key
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama2
export MAX_TOKENS=8192
export TOKEN_BUDGET=1000000
```

## Usage

### CLI Commands

```bash
mission-control --help          # Show all commands
mission-control config          # Interactive configuration
mission-control init <project>  # Initialize new project
mission-control run             # Start Mission Control
mission-control agents          # List available agents
mission-control version         # Show version
```

### Terminal Commands

Once Mission Control is running:

- `new` - Start a new mission
- `status` - Show current mission status
- `history` - Show mission history
- `agents` - Show agent profiles
- `memory` - Show memory statistics
- `help` - Show help information
- `exit` - Exit Mission Control

### Example Mission

```
mission-control> new
Mission description: Build a REST API with authentication, database integration, and comprehensive tests

Mission Control will:
1. Analyze your requirements
2. Create a detailed project plan
3. Deploy specialized agents to implement
4. Run tests and security audits
5. Setup local testing environment
```

## Agent Types

### Root Agent
- Project analysis and planning
- Task dependency analysis
- Agent assignment and orchestration

### Architect Agent
- System design and architecture
- Technical specifications
- Design patterns and best practices

### Developer Agent
- Code implementation
- API development
- Database integration

### Tester Agent
- Unit test generation
- Integration testing
- Test coverage analysis

### Debugger Agent
- Error analysis
- Bug fixing
- Performance optimization

### DevOps Agent
- Environment setup
- Docker configuration
- CI/CD pipeline setup

### Security Agent
- Security audits
- Vulnerability scanning
- Best practices enforcement

## Memory System

Mission Control uses a dual-layer memory system:

### Individual Agent Memory
- Each agent maintains its own knowledge base
- Learns from past experiences
- Improves decision making over time

### Collective Memory
- Shared knowledge across all agents
- Best practices and patterns
- Cross-project learning

## Configuration

Create a `config/mission_config.json` file to customize:

```json
{
  "project_name": "my-project",
  "orchestrator": {
    "max_concurrent_agents": 10,
    "task_timeout": 3600
  },
  "agent_profiles": {
    "architect": {
      "name": "System Architect",
      "model": "claude-3-sonnet-20240229",
      "temperature": 0.7
    }
  }
}
```

## Development

### Project Structure

```
mission_control/
├── agents/          # Agent implementations
├── core/            # Core orchestration logic
├── memory/          # Memory service
├── terminal/        # Terminal interface
└── utils/           # Utilities and monitoring
```

### Running Tests

```bash
pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Inspired by the SPARC framework
- Memory system powered by Mem0
- Built with LangChain and LangGraph

## Support

- GitHub Issues: https://github.com/bluearchio/mission-control/issues
- Documentation: https://github.com/bluearchio/mission-control/wiki
