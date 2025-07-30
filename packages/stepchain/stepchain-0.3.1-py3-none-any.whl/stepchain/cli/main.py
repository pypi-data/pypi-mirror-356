"""Command-line interface for StepChain.

This module provides the stepchain command for running and resuming plans.
"""

import asyncio
import logging
import sys
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.tree import Tree

from stepchain import __version__
from stepchain.core.decomposer import TaskDecomposer
from stepchain.core.executor import AsyncExecutor, Executor
from stepchain.core.models import Plan, Step, StepStatus
from stepchain.storage import JSONLStore

console = Console()


def setup_logging(verbose: bool) -> None:
    """Configure logging with Rich handler."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def cli(verbose: bool) -> None:
    """StepChain - Reliability layer for LLM orchestration."""
    setup_logging(verbose)


@cli.command()
@click.argument("input_source")
@click.option("--run-id", "-r", help="Run ID (defaults to plan ID + timestamp)")
@click.option("--async", "use_async", is_flag=True, help="Use async executor")
@click.option("--max-concurrent", "-c", default=5, help="Max concurrent steps (async only)")
@click.option("--tools", "-t", multiple=True, help="Available tools (for task descriptions)")
@click.option("--dry-run", is_flag=True, help="Show execution plan without running")
def run(input_source: str, run_id: str | None, use_async: bool, max_concurrent: int, 
        tools: tuple[str, ...], dry_run: bool) -> None:
    """Execute a plan from YAML file or decompose and run a task description.

    Examples:
        crewctl run plan.yaml
        crewctl run "Analyze sales data and create a report"
        crewctl run "Build a web scraper" --tools python_code web_search
    """
    # Check if input is a file or task description
    if Path(input_source).exists() and input_source.endswith(('.yaml', '.yml')):
        # Load plan from file
        with open(input_source) as f:
            data = yaml.safe_load(f)
        plan = Plan(**data)
    else:
        # Treat as task description and decompose
        console.print(f"[bold blue]Decomposing task: {input_source}[/bold blue]")
        decomposer = TaskDecomposer()
        
        tools_list = list(tools) if tools else None
        plan = decomposer.decompose(input_source, tools=tools_list)
        
        # Show the generated plan
        console.print("\n[bold green]Generated Plan:[/bold green]")
        _display_plan_tree(plan)
    
    # Generate run ID if not provided
    if not run_id:
        from datetime import datetime
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        run_id = f"{plan.id}_{timestamp}"
    
    console.print(f"[bold green]Starting run: {run_id}[/bold green]")
    console.print(f"Plan: {plan.id} with {len(plan.steps)} steps")
    
    # If dry run, just show the plan and exit
    if dry_run:
        console.print("\n[bold yellow]DRY RUN MODE - No execution will occur[/bold yellow]")
        console.print("\n[bold]Execution order:[/bold]")
        
        # Calculate execution order
        from stepchain.core.scheduler import Scheduler
        scheduler = Scheduler()
        try:
            order = scheduler.get_execution_order(plan)
            for i, step_id in enumerate(order, 1):
                step = next(s for s in plan.steps if s.id == step_id)
                deps = f" (after: {', '.join(step.dependencies)})" if step.dependencies else ""
                console.print(f"{i}. {step.id}{deps}")
                console.print(f"   Tools: {', '.join(step.tools)}")
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)
        
        console.print("\n[green]✓[/green] Plan is valid and ready to execute")
        console.print("To execute, run without --dry-run flag")
        return
    
    # Execute plan
    if use_async:
        asyncio.run(_run_async(plan, run_id, max_concurrent))
    else:
        _run_sync(plan, run_id)


def _run_sync(plan: Plan, run_id: str) -> None:
    """Run plan synchronously with progress display."""
    executor = Executor()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Executing plan...", total=len(plan.steps))
        
        # Execute the entire plan once
        results = executor.execute_plan(plan, run_id)
        
        # Count completed steps
        completed = sum(1 for r in results if r.status == StepStatus.COMPLETED)
        progress.advance(task, completed)
    
    _display_results(results)


async def _run_async(plan: Plan, run_id: str, max_concurrent: int) -> None:
    """Run plan asynchronously with progress display."""
    executor = AsyncExecutor(max_concurrent=max_concurrent)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Executing plan...", total=len(plan.steps))
        
        results = await executor.execute_plan(plan, run_id)
        
        # Update progress
        completed = sum(1 for r in results if r.status == StepStatus.COMPLETED)
        progress.advance(task, completed)
    
    _display_results(results)


@cli.command()
@click.argument("run_id")
@click.option("--async", "use_async", is_flag=True, help="Use async executor")
@click.option("--max-concurrent", "-c", default=5, help="Max concurrent steps (async only)")
def resume(run_id: str, use_async: bool, max_concurrent: int) -> None:
    """Resume an interrupted run.

    Example:
        crewctl resume my-run-123
        crewctl resume my-run-123 --async
    """
    store = JSONLStore()
    
    # Get previous results
    results = store.get_results(run_id)
    if not results:
        console.print(f"[red]No results found for run: {run_id}[/red]")
        sys.exit(1)
    
    # Get the saved plan
    plan = store.get_plan(run_id)
    if not plan:
        console.print(f"[red]No plan found for run: {run_id}[/red]")
        console.print("[yellow]Note: Plans are only saved for runs started with v0.2.0+[/yellow]")
        sys.exit(1)
    
    console.print(f"[bold green]Resuming run: {run_id}[/bold green]")
    console.print(f"Plan: {plan.id} with {len(plan.steps)} steps")
    console.print(f"Found {len(results)} previous results")
    
    # Display current status
    completed = sum(1 for r in results if r.status == StepStatus.COMPLETED)
    failed = sum(1 for r in results if r.status == StepStatus.FAILED)
    
    if failed > 0:
        console.print(f"[yellow]Warning: {failed} steps failed in previous run[/yellow]")
    
    console.print(f"Progress: {completed}/{len(plan.steps)} steps completed")
    
    # Resume execution
    if use_async:
        asyncio.run(_resume_async(plan, run_id, max_concurrent))
    else:
        _resume_sync(plan, run_id)


@cli.command()
@click.argument("plan_file", type=click.Path(exists=True))
@click.option("--tools", "-t", multiple=True, help="Available tools to validate against")
def validate(plan_file: str, tools: tuple[str, ...]) -> None:
    """Validate a plan file for correctness.
    
    Example:
        crewctl validate plan.yaml
        crewctl validate plan.yaml --tools python_code web_search
    """
    console.print(f"[bold]Validating plan: {plan_file}[/bold]")
    
    try:
        # Load plan
        with open(plan_file) as f:
            plan_data = yaml.safe_load(f)
        
        # Create plan object
        plan = Plan(**plan_data)
        
        # Validate dependencies
        plan.validate_dependencies()
        console.print("[green]✓[/green] Dependencies are valid")
        
        # Check for circular dependencies
        from stepchain.core.scheduler import Scheduler
        scheduler = Scheduler()
        try:
            order = scheduler.get_execution_order(plan)
            console.print("[green]✓[/green] No circular dependencies")
            console.print(f"[green]✓[/green] Execution order determined ({len(order)} steps)")
        except ValueError as e:
            console.print(f"[red]✗[/red] Circular dependencies detected: {e}")
            sys.exit(1)
        
        # Validate tools if provided
        if tools:
            available_tools = set(tools)
            console.print(f"\nValidating against available tools: {', '.join(available_tools)}")
            
            invalid_tools = []
            for step in plan.steps:
                for tool in step.tools:
                    if tool not in available_tools:
                        invalid_tools.append((step.id, tool))
            
            if invalid_tools:
                console.print("[red]✗[/red] Invalid tool usage found:")
                for step_id, tool in invalid_tools:
                    console.print(f"  - Step '{step_id}' uses unavailable tool '{tool}'")
                sys.exit(1)
            else:
                console.print("[green]✓[/green] All tools are available")
        
        # Show plan summary
        console.print("\n[bold]Plan Summary:[/bold]")
        console.print(f"  ID: {plan.id}")
        console.print(f"  Steps: {len(plan.steps)}")
        
        # Count tools usage
        from collections import Counter
        tool_usage = Counter()
        for step in plan.steps:
            tool_usage.update(step.tools)
        
        if tool_usage:
            console.print("\n[bold]Tool Usage:[/bold]")
            for tool, count in tool_usage.most_common():
                console.print(f"  {tool}: {count} steps")
        
        # Analyze parallelization potential
        depth_map: dict[str, int] = {}
        for step in plan.steps:
            depth = _get_step_depth(step.id, plan.steps)
            depth_map.setdefault(depth, []).append(step.id)
        
        max_parallel = max(len(steps) for steps in depth_map.values())
        console.print("\n[bold]Parallelization Potential:[/bold]")
        console.print(f"  Maximum parallel steps: {max_parallel}")
        console.print(f"  Dependency depth: {len(depth_map)}")
        
        console.print("\n[green]✓[/green] Plan validation successful!")
        
    except FileNotFoundError:
        console.print(f"[red]Error: File '{plan_file}' not found[/red]")
        sys.exit(1)
    except yaml.YAMLError as e:
        console.print(f"[red]Error: Invalid YAML format: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: Plan validation failed: {e}[/red]")
        sys.exit(1)


def _get_step_depth(step_id: str, all_steps: list) -> int:
    """Calculate the dependency depth of a step."""
    step_map = {s.id: s for s in all_steps}
    step = step_map.get(step_id)
    
    if not step or not step.dependencies:
        return 0
    
    max_depth = 0
    for dep_id in step.dependencies:
        if dep_id in step_map:
            depth = 1 + _get_step_depth(dep_id, all_steps)
            max_depth = max(max_depth, depth)
    
    return max_depth


@cli.command()
def list_runs() -> None:
    """List all runs."""
    store = JSONLStore()
    runs = store.list_runs()
    
    if not runs:
        console.print("[yellow]No runs found[/yellow]")
        return
    
    table = Table(title="StepChain Runs")
    table.add_column("Run ID", style="cyan")
    table.add_column("Steps", justify="right")
    table.add_column("Status")
    
    for run_id in runs:
        results = store.get_results(run_id)
        total = len(results)
        completed = sum(1 for r in results if r.status == StepStatus.COMPLETED)
        failed = sum(1 for r in results if r.status == StepStatus.FAILED)
        
        if failed > 0:
            status = f"[red]Failed ({failed})[/red]"
        elif completed == total:
            status = "[green]Completed[/green]"
        else:
            status = f"[yellow]Partial ({completed}/{total})[/yellow]"
        
        table.add_row(run_id, str(total), status)
    
    console.print(table)


def _resume_sync(plan: Plan, run_id: str) -> None:
    """Resume plan execution synchronously."""
    executor = Executor()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        # Get already completed steps
        existing_results = executor.store.get_results(run_id)
        completed_count = sum(1 for r in existing_results if r.status == StepStatus.COMPLETED)
        
        task = progress.add_task("Resuming execution...", total=len(plan.steps))
        progress.advance(task, completed_count)
        
        # Execute remaining steps
        results = executor.execute_plan(plan, run_id, resume=True)
        
        # Update progress for newly completed steps
        new_completed = sum(1 for r in results if r.status == StepStatus.COMPLETED)
        if new_completed > 0:
            progress.advance(task, new_completed)
    
    # Display all results
    all_results = executor.store.get_results(run_id)
    _display_results(all_results)


async def _resume_async(plan: Plan, run_id: str, max_concurrent: int) -> None:
    """Resume plan execution asynchronously."""
    executor = AsyncExecutor(max_concurrent=max_concurrent)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        # Get already completed steps
        existing_results = executor.executor.store.get_results(run_id)
        completed_count = sum(1 for r in existing_results if r.status == StepStatus.COMPLETED)
        
        task = progress.add_task("Resuming execution...", total=len(plan.steps))
        progress.advance(task, completed_count)
        
        # Execute remaining steps
        results = await executor.execute_plan(plan, run_id, resume=True)
        
        # Update progress
        new_completed = sum(1 for r in results if r.status == StepStatus.COMPLETED)
        if new_completed > 0:
            progress.advance(task, new_completed)
    
    # Display all results
    all_results = executor.executor.store.get_results(run_id)
    _display_results(all_results)


def _display_results(results: list) -> None:
    """Display results in a table."""
    if not results:
        return
    
    table = Table(title="Execution Results")
    table.add_column("Step", style="cyan")
    table.add_column("Status")
    table.add_column("Duration", justify="right")
    table.add_column("Attempts", justify="right")
    
    for result in results:
        status_color = {
            StepStatus.COMPLETED: "green",
            StepStatus.FAILED: "red",
            StepStatus.RUNNING: "yellow",
            StepStatus.PENDING: "white",
        }.get(result.status, "white")
        
        duration = f"{result.duration_seconds:.1f}s" if result.duration_seconds else "-"
        
        table.add_row(
            result.step_id,
            f"[{status_color}]{result.status.value}[/{status_color}]",
            duration,
            str(result.attempt_count),
        )
    
    console.print(table)


@cli.command()
@click.argument("task_description")
@click.option("--tools", "-t", multiple=True, help="Available tools")
@click.option("--output", "-o", type=click.Path(), help="Output YAML file")
@click.option("--max-steps", default=20, help="Maximum number of steps")
def decompose(
    task_description: str,
    tools: tuple[str, ...],
    output: str | None,
    max_steps: int
) -> None:
    """Decompose a task into executable steps.

    Examples:
        crewctl decompose "Create a data analysis report"
        crewctl decompose "Build a web scraper" --tools python_code web_search
        crewctl decompose "Process customer feedback" --output feedback_plan.yaml
    """
    console.print(f"[bold blue]Decomposing task:[/bold blue] {task_description}")
    
    # Create decomposer
    decomposer = TaskDecomposer(
        max_steps=max_steps
    )
    
    # Decompose the task
    try:
        tools_list = list(tools) if tools else None
        plan = decomposer.decompose(task_description, tools=tools_list)
        
        # Display the plan as a tree
        console.print("\n[bold green]Generated Plan:[/bold green]")
        _display_plan_tree(plan)
        
        # Show dependency graph
        console.print("\n[bold cyan]Dependency Graph:[/bold cyan]")
        _display_dependency_graph(plan)
        
        # Save to file if requested
        if output:
            # Convert plan to dict for YAML serialization
            plan_dict = {
                "id": plan.id,
                "steps": [
                    {
                        "id": step.id,
                        "prompt": step.prompt,
                        "tools": step.tools,
                        "dependencies": step.dependencies,
                        "max_retries": step.max_retries,
                        "timeout": step.timeout,
                        "metadata": step.metadata
                    }
                    for step in plan.steps
                ],
                "metadata": plan.metadata
            }
            
            with open(output, 'w') as f:
                yaml.dump(plan_dict, f, default_flow_style=False, sort_keys=False)
            
            console.print(f"\n[green]✓[/green] Plan saved to: {output}")
        
        # Show summary
        console.print("\n[bold]Summary:[/bold]")
        console.print(f"  Total steps: {len(plan.steps)}")
        console.print(f"  Tools used: {len({t for s in plan.steps for t in s.tools})}")
        console.print(f"  Max parallel steps: {plan.metadata.get('max_parallel_steps', 'N/A')}")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def _display_plan_tree(plan: Plan) -> None:
    """Display plan as a tree structure."""
    tree = Tree(f"[bold]{plan.id}[/bold]")
    
    # Group steps by dependency level
    added_steps = set()
    
    def add_step_to_tree(step: Step, parent_node=None) -> None:
        if step.id in added_steps:
            return
        
        # Create node text
        tools_str = f" [{', '.join(step.tools)}]" if step.tools else ""
        node_text = f"[cyan]{step.id}[/cyan]{tools_str}\n  {step.prompt[:60]}..."
        
        # Add to tree
        node = tree.add(node_text) if parent_node is None else parent_node.add(node_text)
        
        added_steps.add(step.id)
        
        # Add dependent steps
        for other_step in plan.steps:
            if step.id in other_step.dependencies:
                add_step_to_tree(other_step, node)
    
    # Start with steps that have no dependencies
    root_steps = [step for step in plan.steps if not step.dependencies]
    for step in root_steps:
        add_step_to_tree(step)
    
    console.print(tree)


def _display_dependency_graph(plan: Plan) -> None:
    """Display a visual dependency graph."""
    # Create a simple ASCII representation
    step_dict = {step.id: step for step in plan.steps}
    
    # Calculate levels based on dependencies
    levels: dict[str, int] = {}
    
    def get_level(step_id: str) -> int:
        if step_id in levels:
            return levels[step_id]
        
        step = step_dict.get(step_id)
        if not step or not step.dependencies:
            levels[step_id] = 0
            return 0
        
        max_dep_level = max(get_level(dep) for dep in step.dependencies)
        levels[step_id] = max_dep_level + 1
        return levels[step_id]
    
    # Calculate levels for all steps
    for step in plan.steps:
        get_level(step.id)
    
    # Group by level
    level_groups: dict[int, list[str]] = {}
    for step_id, level in levels.items():
        if level not in level_groups:
            level_groups[level] = []
        level_groups[level].append(step_id)
    
    # Display
    max_level = max(level_groups.keys()) if level_groups else 0
    
    for level in range(max_level + 1):
        if level in level_groups:
            console.print(f"  Level {level}: {' | '.join(level_groups[level])}")
            if level < max_level:
                console.print("      ↓")


def main() -> None:
    """Entry point for crewctl command."""
    cli()


if __name__ == "__main__":
    main()
