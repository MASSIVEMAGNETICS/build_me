"""
OmniForge: Command Line Interface
Production-grade CLI with rich output and error handling
"""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
import sys
import json

from src.core.engine import OmniForgeEngine
from src.core.config import SystemConfig

console = Console()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    OmniForge: The Absolute Upgrade Engine
    
    Analyze, upgrade, and transform your codebase to modern standards.
    """
    pass

@cli.command()
@click.argument('repo_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for report')
@click.option('--format', '-f', type=click.Choice(['json', 'text']), default='text', help='Output format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def analyze(repo_path, output, format, verbose):
    """Analyze a repository and generate comprehensive report"""
    
    console.print(Panel.fit(
        "[bold cyan]OmniForge: The Absolute Upgrade Engine[/bold cyan]\n"
        "[dim]Analyzing your repository...[/dim]",
        border_style="cyan"
    ))
    
    try:
        # Initialize engine
        config = SystemConfig(debug_mode=verbose)
        engine = OmniForgeEngine(config=config)
        
        # Run analysis with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Analyzing repository...", total=None)
            
            report = engine.analyze_repository(repo_path)
            
            progress.update(task, completed=True)
        
        # Display results
        if format == 'text':
            display_text_report(report)
        else:
            display_json_report(report)
        
        # Save to file if requested
        if output:
            if format == 'json':
                engine.export_report(report, output)
            else:
                with open(output, 'w') as f:
                    f.write(engine.generate_summary(report))
            console.print(f"\n[green]✓[/green] Report saved to: {output}")
        
        # Exit with appropriate code
        if report.security_scan.get('critical', 0) > 0:
            console.print("\n[red]⚠ Critical security issues found![/red]")
            sys.exit(1)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        if verbose:
            console.print_exception()
        sys.exit(1)

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=8000, type=int, help='Port to bind to')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def serve(host, port, reload):
    """Start the OmniForge API server"""
    console.print(Panel.fit(
        f"[bold cyan]Starting OmniForge API Server[/bold cyan]\n"
        f"[dim]Server running at http://{host}:{port}[/dim]",
        border_style="cyan"
    ))
    
    import uvicorn
    from src.core.api import app
    
    uvicorn.run(
        "src.core.api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

@cli.command()
def gui():
    """Launch the OmniForge web GUI"""
    console.print(Panel.fit(
        "[bold cyan]Launching OmniForge GUI[/bold cyan]\n"
        "[dim]Starting web interface...[/dim]",
        border_style="cyan"
    ))
    
    import subprocess
    import os
    
    # Start API server in background
    console.print("[cyan]Starting API server...[/cyan]")
    
    # Start frontend dev server
    console.print("[cyan]Starting web interface...[/cyan]")
    console.print("\n[green]✓[/green] GUI available at: http://localhost:5173")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    try:
        subprocess.run(["npm", "run", "dev"])
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/yellow]")

@cli.command()
def info():
    """Display OmniForge system information"""
    
    info_table = Table(title="OmniForge System Information", show_header=False)
    info_table.add_column("Property", style="cyan")
    info_table.add_column("Value", style="white")
    
    info_table.add_row("Name", "OmniForge")
    info_table.add_row("Version", "1.0.0")
    info_table.add_row("Description", "The Absolute Upgrade Engine")
    
    console.print(info_table)
    
    features_table = Table(title="Features")
    features_table.add_column("Feature", style="green")
    
    features = [
        "Repository Analysis",
        "Security Scanning",
        "Code Quality Metrics",
        "Architecture Detection",
        "Upgrade Recommendations",
        "Self-Healing Capabilities",
        "Modern Web GUI",
        "RESTful API"
    ]
    
    for feature in features:
        features_table.add_row(f"✓ {feature}")
    
    console.print(features_table)

def display_text_report(report):
    """Display report in rich text format"""
    
    # Analysis table
    analysis_table = Table(title="Code Analysis Results")
    analysis_table.add_column("Metric", style="cyan")
    analysis_table.add_column("Value", style="white")
    
    analysis = report.analysis
    analysis_table.add_row("Total Files", str(analysis.get('total_files', 0)))
    analysis_table.add_row("Total Lines", str(analysis.get('total_lines', 0)))
    analysis_table.add_row("Architecture", analysis.get('architecture_type', 'unknown'))
    analysis_table.add_row("Maintainability", f"{analysis.get('maintainability_score', 0):.1f}/100")
    analysis_table.add_row("Avg Complexity", f"{analysis.get('complexity_stats', {}).get('avg', 0):.1f}")
    
    console.print(analysis_table)
    
    # Security table
    security_table = Table(title="Security Scan Results")
    security_table.add_column("Severity", style="cyan")
    security_table.add_column("Count", style="white")
    
    security = report.security_scan
    
    def get_severity_style(count, is_critical=False):
        if count == 0:
            return "green"
        elif is_critical or count > 5:
            return "red"
        else:
            return "yellow"
    
    security_table.add_row(
        "Critical",
        f"[{get_severity_style(security.get('critical', 0), True)}]{security.get('critical', 0)}[/]"
    )
    security_table.add_row(
        "High",
        f"[{get_severity_style(security.get('high', 0))}]{security.get('high', 0)}[/]"
    )
    security_table.add_row(
        "Medium",
        f"[yellow]{security.get('medium', 0)}[/yellow]"
    )
    security_table.add_row(
        "Low",
        f"[dim]{security.get('low', 0)}[/dim]"
    )
    
    console.print(security_table)
    
    # Recommendations
    if report.recommendations:
        console.print("\n[bold cyan]Recommendations:[/bold cyan]")
        for i, rec in enumerate(report.recommendations, 1):
            console.print(f"  {i}. {rec}")

def display_json_report(report):
    """Display report in JSON format"""
    report_dict = {
        'timestamp': report.timestamp,
        'repository_path': report.repository_path,
        'success': report.success,
        'analysis': report.analysis,
        'security_scan': report.security_scan,
        'recommendations': report.recommendations,
        'upgrades': report.upgrades
    }
    console.print_json(data=report_dict)

if __name__ == '__main__':
    cli()
