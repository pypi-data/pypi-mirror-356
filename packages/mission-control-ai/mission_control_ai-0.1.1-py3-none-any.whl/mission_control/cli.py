"""Command-line interface for Mission Control"""

import typer
from typing import Optional
from pathlib import Path
import os
from loguru import logger
from rich.console import Console

from .core.config import MissionConfig
from .terminal.interface import TerminalInterface

app = typer.Typer(
    name="mission-control",
    help="AI Development Workflow Orchestration System",
    add_completion=False
)

console = Console()


@app.command()
def run(
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file"
    ),
    env_file: Optional[Path] = typer.Option(
        ".env",
        "--env",
        "-e",
        help="Path to environment file"
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        "-l",
        help="Logging level"
    ),
    interactive: bool = typer.Option(
        True,
        "--interactive/--no-interactive",
        "-i/-n",
        help="Run in interactive mode"
    )
):
    """Run Mission Control terminal interface"""
    
    # Setup logging
    logger.remove()  # Remove default handler
    logger.add(
        "mission_control.log",
        rotation="10 MB",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    logger.add(
        lambda msg: console.print(f"[dim]{msg}[/dim]"),
        level="ERROR"
    )
    
    # Load configuration
    if env_file and env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    config = MissionConfig()
    
    # Override with config file if provided
    if config_file and config_file.exists():
        import json
        with open(config_file) as f:
            config_data = json.load(f)
            config = MissionConfig(**config_data)
    
    # Create and run terminal interface
    interface = TerminalInterface(config)
    interface.interactive_mode = interactive
    
    try:
        interface.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Mission Control terminated by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        logger.exception("Unhandled exception in Mission Control")
        raise typer.Exit(1)


@app.command()
def init(
    project_dir: Path = typer.Argument(
        Path("."),
        help="Project directory to initialize"
    ),
    name: str = typer.Option(
        "my-project",
        "--name",
        "-n",
        help="Project name"
    )
):
    """Initialize a new Mission Control project"""
    
    console.print(f"[bold]Initializing Mission Control project: {name}[/bold]")
    
    # Create project structure
    project_dir = project_dir / name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create directories
    dirs = ["src", "tests", "docs", "config", ".mission_control"]
    for dir_name in dirs:
        (project_dir / dir_name).mkdir(exist_ok=True)
    
    # Create .env file
    env_content = """# Mission Control Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO

# API Keys
ANTHROPIC_API_KEY=your-api-key-here
OPENAI_API_KEY=your-api-key-here
MEM0_API_KEY=your-api-key-here

# Memory Configuration
MEMORY_PROVIDER=mem0
MEMORY_VECTOR_DB_TYPE=chromadb

# Orchestrator Configuration
ORCHESTRATOR_MAX_CONCURRENT_AGENTS=10
ORCHESTRATOR_ENABLE_MONITORING=true
"""
    
    with open(project_dir / ".env", "w") as f:
        f.write(env_content)
    
    # Create config file
    config_content = {
        "project_name": name,
        "agent_profiles": {
            "architect": {
                "name": "System Architect",
                "capabilities": ["system_design", "architecture_planning"]
            },
            "developer": {
                "name": "Senior Developer",
                "capabilities": ["code_generation", "refactoring"]
            }
        }
    }
    
    import json
    with open(project_dir / "config" / "mission_config.json", "w") as f:
        json.dump(config_content, f, indent=2)
    
    # Create .gitignore
    gitignore_content = """# Mission Control
.mission_control/
mission_control.log
.env

# Python
__pycache__/
*.py[cod]
venv/
.venv/

# IDE
.vscode/
.idea/
"""
    
    with open(project_dir / ".gitignore", "w") as f:
        f.write(gitignore_content)
    
    console.print(f"[green]✓[/green] Created project directory: {project_dir}")
    console.print(f"[green]✓[/green] Created configuration files")
    console.print(f"[green]✓[/green] Created project structure")
    
    console.print(f"\n[bold]Next steps:[/bold]")
    console.print(f"1. cd {project_dir}")
    console.print(f"2. Edit .env file with your API keys")
    console.print(f"3. Run: mission-control run")


@app.command()
def config():
    """Configure Mission Control settings interactively"""
    from .terminal.config_ui import run_config_ui
    run_config_ui()


@app.command()
def version():
    """Show Mission Control version"""
    from . import __version__
    console.print(f"Mission Control v{__version__}")


@app.command()
def agents():
    """List available agent types"""
    
    agents_info = {
        "architect": "System design and architecture planning",
        "developer": "Code implementation and refactoring",
        "tester": "Testing and quality assurance",
        "debugger": "Error analysis and bug fixing",
        "devops": "Environment setup and deployment",
        "security": "Security audits and vulnerability scanning"
    }
    
    console.print("[bold]Available Agent Types:[/bold]\n")
    
    for agent_type, description in agents_info.items():
        console.print(f"  [cyan]{agent_type:12}[/cyan] {description}")


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main()