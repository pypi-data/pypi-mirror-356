"""Terminal interface for Mission Control"""

import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.tree import Tree
import typer
from loguru import logger
import json

from ..core.orchestrator import MissionOrchestrator
from ..core.config import MissionConfig


class TerminalInterface:
    """Interactive terminal interface for Mission Control"""
    
    def __init__(self, config: MissionConfig):
        self.config = config
        self.console = Console()
        self.orchestrator = MissionOrchestrator(config)
        self.current_mission = None
        self.interactive_mode = True
        
    def run(self):
        """Run the terminal interface"""
        self.console.print(
            Panel.fit(
                "[bold blue]Mission Control Terminal[/bold blue]\n"
                "[dim]AI Development Workflow Orchestration System[/dim]",
                border_style="blue"
            )
        )
        
        # Run async event loop
        asyncio.run(self._async_run())
    
    async def _async_run(self):
        """Async main loop"""
        try:
            while True:
                command = await self._get_command()
                
                if command == "exit":
                    break
                elif command == "new":
                    await self._start_new_mission()
                elif command == "status":
                    await self._show_status()
                elif command == "history":
                    await self._show_history()
                elif command == "agents":
                    await self._show_agents()
                elif command == "memory":
                    await self._show_memory()
                elif command == "help":
                    self._show_help()
                else:
                    self.console.print(f"[red]Unknown command: {command}[/red]")
                    
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Mission Control shutting down...[/yellow]")
        finally:
            await self.orchestrator.shutdown()
    
    async def _get_command(self) -> str:
        """Get command from user"""
        commands = ["new", "status", "history", "agents", "memory", "help", "exit"]
        
        # Show current status
        if self.current_mission:
            status = await self.orchestrator.get_mission_status()
            self.console.print(f"\n[dim]Current mission: {status['mission_id']} ({status['status']})[/dim]")
        
        # Prompt for command
        command = Prompt.ask(
            "\n[bold green]mission-control[/bold green]",
            choices=commands,
            default="help"
        )
        
        return command.lower()
    
    async def _start_new_mission(self):
        """Start a new mission"""
        self.console.print("\n[bold]Starting New Mission[/bold]")
        
        # Get mission description
        description = Prompt.ask("Mission description")
        
        if not description:
            self.console.print("[red]Mission description required[/red]")
            return
        
        # Confirm mission parameters
        self.console.print("\n[bold]Mission Parameters:[/bold]")
        params_table = Table(show_header=False)
        params_table.add_column("Parameter", style="cyan")
        params_table.add_column("Value")
        
        params_table.add_row("Description", description)
        params_table.add_row("Max Concurrent Agents", str(self.config.orchestrator.max_concurrent_agents))
        params_table.add_row("Memory Service", self.config.memory.provider)
        params_table.add_row("Interactive Mode", "Yes" if self.interactive_mode else "No")
        
        self.console.print(params_table)
        
        if not Confirm.ask("\nProceed with mission?"):
            self.console.print("[yellow]Mission cancelled[/yellow]")
            return
        
        # Start mission with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console
        ) as progress:
            
            # Add progress tasks
            analysis_task = progress.add_task("[cyan]Analysis phase...", total=100)
            planning_task = progress.add_task("[cyan]Planning phase...", total=100)
            execution_task = progress.add_task("[cyan]Execution phase...", total=100)
            validation_task = progress.add_task("[cyan]Validation phase...", total=100)
            deployment_task = progress.add_task("[cyan]Deployment phase...", total=100)
            
            # Execute mission phases
            try:
                # Start mission
                self.current_mission = asyncio.create_task(
                    self.orchestrator.start_mission(description)
                )
                
                # Monitor progress
                phases = [
                    ("analysis", analysis_task),
                    ("planning", planning_task),
                    ("execution", execution_task),
                    ("validation", validation_task),
                    ("deployment", deployment_task)
                ]
                
                completed_phases = set()
                
                while not self.current_mission.done():
                    # Check mission status
                    status = await self.orchestrator.get_mission_status()
                    
                    # Update progress based on completed phases
                    if self.orchestrator.current_mission:
                        results = self.orchestrator.current_mission.get("results", {})
                        
                        for phase_name, task_id in phases:
                            if phase_name in results and phase_name not in completed_phases:
                                progress.update(task_id, completed=100)
                                completed_phases.add(phase_name)
                        
                        # Update execution progress based on task completion
                        if "execution" not in completed_phases:
                            total_tasks = status["progress"]["completed_tasks"] + \
                                        status["progress"]["pending_tasks"] + \
                                        status["progress"]["running_tasks"]
                            if total_tasks > 0:
                                completion = (status["progress"]["completed_tasks"] / total_tasks) * 100
                                progress.update(execution_task, completed=completion)
                    
                    await asyncio.sleep(0.5)
                
                # Get final result
                result = await self.current_mission
                
                # Mark all phases complete
                for _, task_id in phases:
                    progress.update(task_id, completed=100)
                
                # Show results
                self._display_mission_results(result)
                
            except Exception as e:
                self.console.print(f"\n[red]Mission failed: {str(e)}[/red]")
                logger.error(f"Mission execution failed: {str(e)}")
    
    async def _show_status(self):
        """Show current mission status"""
        status = await self.orchestrator.get_mission_status()
        
        if status["status"] == "no_active_mission":
            self.console.print("\n[yellow]No active mission[/yellow]")
            return
        
        # Create status layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(
            Panel(f"Mission Status: {status['mission_id']}", style="bold blue")
        )
        
        # Body - split into progress and agents
        layout["body"].split_row(
            Layout(name="progress"),
            Layout(name="agents")
        )
        
        # Progress table
        progress_table = Table(title="Task Progress", show_header=True)
        progress_table.add_column("Status", style="cyan")
        progress_table.add_column("Count", justify="right")
        
        for key, value in status["progress"].items():
            progress_table.add_row(key.replace("_", " ").title(), str(value))
        
        layout["body"]["progress"].update(progress_table)
        
        # Active agents table
        agents_table = Table(title="Active Agents", show_header=True)
        agents_table.add_column("Agent", style="green")
        
        for agent in status["active_agents"]:
            agents_table.add_row(agent)
        
        layout["body"]["agents"].update(agents_table)
        
        # Footer
        duration = status.get("duration", 0)
        layout["footer"].update(
            Panel(f"Duration: {duration:.1f} seconds", style="dim")
        )
        
        self.console.print(layout)
    
    async def _show_history(self):
        """Show mission history"""
        history = self.orchestrator.mission_history
        
        if not history:
            self.console.print("\n[yellow]No mission history[/yellow]")
            return
        
        # Create history table
        table = Table(title="Mission History", show_header=True)
        table.add_column("Mission ID", style="cyan")
        table.add_column("Description", max_width=40)
        table.add_column("Status", style="green")
        table.add_column("Duration")
        table.add_column("Completed At")
        
        for mission in history:
            duration = "N/A"
            if mission.get("started_at") and mission.get("completed_at"):
                delta = mission["completed_at"] - mission["started_at"]
                duration = f"{delta.total_seconds():.1f}s"
            
            completed_at = mission.get("completed_at", "N/A")
            if isinstance(completed_at, datetime):
                completed_at = completed_at.strftime("%Y-%m-%d %H:%M:%S")
            
            table.add_row(
                mission["id"],
                mission["description"][:40] + "..." if len(mission["description"]) > 40 else mission["description"],
                mission["status"],
                duration,
                completed_at
            )
        
        self.console.print(table)
    
    async def _show_agents(self):
        """Show agent information"""
        # Create agents tree
        tree = Tree("[bold]Agent Profiles[/bold]")
        
        for agent_type, config in self.config.agent_profiles.items():
            agent_branch = tree.add(f"[cyan]{agent_type}[/cyan] - {config.name}")
            
            # Add capabilities
            caps_branch = agent_branch.add("[yellow]Capabilities[/yellow]")
            for cap in config.capabilities:
                caps_branch.add(f"• {cap}")
            
            # Add configuration
            config_branch = agent_branch.add("[yellow]Configuration[/yellow]")
            config_branch.add(f"Model: {config.model}")
            config_branch.add(f"Temperature: {config.temperature}")
            config_branch.add(f"Max Tokens: {config.max_tokens}")
            
            # Add memory namespace
            if config.memory_namespace:
                agent_branch.add(f"[yellow]Memory:[/yellow] {config.memory_namespace}")
        
        self.console.print(tree)
    
    async def _show_memory(self):
        """Show memory statistics"""
        # Get memory service
        memory_service = self.orchestrator.memory_service
        
        # Create memory table
        table = Table(title="Memory Statistics", show_header=True)
        table.add_column("Namespace", style="cyan")
        table.add_column("Memory Count", justify="right")
        
        # Get memory counts for each agent
        for agent_type in self.config.agent_profiles.keys():
            agent_id = f"{agent_type}_{agent_type}"
            memories = memory_service.get_agent_memories(agent_id, page_size=1)
            
            # This is a simplified count - in reality we'd paginate through all
            table.add_row(f"agent_{agent_id}", str(len(memories)))
        
        # Add collective memory
        collective_memories = memory_service.get_agent_memories(None, page_size=1)
        table.add_row("collective", str(len(collective_memories)))
        
        self.console.print(table)
        
        # Show recent memories
        if Confirm.ask("\nShow recent memories?"):
            recent_memories = memory_service.search_memory("", limit=5)
            
            for idx, memory in enumerate(recent_memories):
                self.console.print(f"\n[bold]Memory {idx + 1}:[/bold]")
                self.console.print(f"[dim]{memory.get('memory', 'N/A')}[/dim]")
                self.console.print(f"[yellow]Score: {memory.get('score', 0):.2f}[/yellow]")
    
    def _show_help(self):
        """Show help information"""
        help_text = """
[bold]Mission Control Commands:[/bold]

  [cyan]new[/cyan]      Start a new mission
  [cyan]status[/cyan]   Show current mission status
  [cyan]history[/cyan]  Show mission history
  [cyan]agents[/cyan]   Show agent profiles
  [cyan]memory[/cyan]   Show memory statistics
  [cyan]help[/cyan]     Show this help message
  [cyan]exit[/cyan]     Exit Mission Control

[bold]Mission Workflow:[/bold]
  1. Analysis - Analyze project requirements
  2. Planning - Create detailed project plan
  3. Execution - Implement with specialized agents
  4. Validation - Test and security audit
  5. Deployment - Setup deployment environment

[bold]Agent Types:[/bold]
  • Architect - System design and architecture
  • Developer - Code implementation
  • Tester - Testing and quality assurance
  • Debugger - Error analysis and fixes
  • DevOps - Environment and deployment
  • Security - Security audits

[bold]Configuration:[/bold]
  Run [cyan]mission-control config[/cyan] to:
  • Set API keys (Anthropic, OpenAI, Mem0)
  • Configure local models (Ollama)
  • Set token limits and budgets
  • Customize agent profiles
  • Choose memory storage backend
"""
        self.console.print(help_text)
    
    def _display_mission_results(self, result: Dict[str, Any]):
        """Display mission results"""
        self.console.print("\n[bold green]Mission Completed![/bold green]")
        
        # Mission summary
        summary_table = Table(title="Mission Summary", show_header=False)
        summary_table.add_column("Field", style="cyan")
        summary_table.add_column("Value")
        
        summary_table.add_row("Mission ID", result["id"])
        summary_table.add_row("Status", result["status"])
        summary_table.add_row("Duration", f"{(result['completed_at'] - result['started_at']).total_seconds():.1f} seconds")
        
        self.console.print(summary_table)
        
        # Phase results
        if "results" in result:
            for phase, phase_result in result["results"].items():
                self.console.print(f"\n[bold]{phase.title()} Phase:[/bold]")
                
                if isinstance(phase_result, dict):
                    # Pretty print JSON
                    json_str = json.dumps(phase_result, indent=2)
                    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
                    self.console.print(syntax)
                else:
                    self.console.print(str(phase_result))
        
        # Save results option
        if Confirm.ask("\nSave mission results to file?"):
            filename = f"mission_{result['id']}.json"
            with open(filename, "w") as f:
                json.dump(result, f, indent=2, default=str)
            self.console.print(f"[green]Results saved to {filename}[/green]")