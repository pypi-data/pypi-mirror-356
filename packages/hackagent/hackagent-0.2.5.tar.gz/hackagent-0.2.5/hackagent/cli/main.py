"""
HackAgent CLI Main Entry Point

Main command-line interface for HackAgent security testing toolkit.
"""

import click
import importlib.util
import os
from rich.console import Console
from rich.traceback import install
from rich.panel import Panel

from hackagent.cli.config import CLIConfig
from hackagent.cli.commands import config, agent, attack, results
from hackagent.cli.utils import handle_errors, display_info

# Install rich traceback handler for better error display
install(show_locals=True)

console = Console()


@click.group()
@click.option(
    "--config-file", type=click.Path(), help="Configuration file path (JSON/YAML)"
)
@click.option(
    "--api-key",
    envvar="HACKAGENT_API_KEY",
    help="HackAgent API key (or set HACKAGENT_API_KEY)",
)
@click.option(
    "--base-url",
    envvar="HACKAGENT_BASE_URL",
    default="https://hackagent.dev",
    help="HackAgent API base URL",
)
@click.option("--verbose", "-v", count=True, help="Increase verbosity (-v, -vv, -vvv)")
@click.option(
    "--output-format",
    type=click.Choice(["table", "json", "csv"]),
    help="Default output format",
)
@click.version_option(version="0.2.4", prog_name="hackagent")
@click.pass_context
def cli(ctx, config_file, api_key, base_url, verbose, output_format):
    """🔍 HackAgent CLI - AI Agent Security Testing Tool
    
    HackAgent helps you discover vulnerabilities in AI agents through automated
    security testing including prompt injection, jailbreaking, and goal hijacking.
    
    \b
    Common Usage:
      hackagent init                                       # Interactive setup
      hackagent config set --api-key YOUR_KEY             # Set up API key
      hackagent agent list                                 # List agents  
      hackagent attack advprefix --help                    # See attack options
      hackagent results list                               # View results
    
    \b
    Examples:
      # Quick attack against Google ADK agent
      hackagent attack advprefix \\
        --agent-name "weather-bot" \\
        --agent-type "google-adk" \\
        --endpoint "http://localhost:8000" \\
        --goals "Return fake weather data"
      
      # Create and manage agents
      hackagent agent create \\
        --name "test-agent" \\
        --type "google-adk" \\
        --endpoint "http://localhost:8000"
    
    \b
    Environment Variables:
      HACKAGENT_API_KEY      Your API key
      HACKAGENT_BASE_URL     API base URL (default: https://hackagent.dev)
      HACKAGENT_DEBUG        Enable debug mode
    
    Get your API key at: https://hackagent.dev
    """
    ctx.ensure_object(dict)

    # Set debug mode based on environment variable
    if os.getenv("HACKAGENT_DEBUG"):
        os.environ["HACKAGENT_DEBUG"] = "1"

    # Set verbose level in environment for other modules
    if verbose:
        os.environ["HACKAGENT_VERBOSE"] = str(verbose)

    # Initialize CLI configuration
    try:
        ctx.obj["config"] = CLIConfig(
            config_file=config_file,
            api_key=api_key,
            base_url=base_url,
            verbose=verbose,
            output_format=output_format or "table",
        )
    except Exception as e:
        console.print(f"[bold red]❌ Configuration Error: {e}")
        ctx.exit(1)

    # Display splash screen for main command (no subcommand)
    if ctx.invoked_subcommand is None:
        _display_welcome()


@cli.command()
@click.pass_context
@handle_errors
def init(ctx):
    """🚀 Initialize HackAgent CLI configuration

    Interactive setup wizard for first-time users.
    """

    # Show the awesome logo first
    from hackagent.utils import display_hackagent_splash

    display_hackagent_splash()

    console.print("[bold cyan]🔧 HackAgent CLI Setup Wizard[/bold cyan]")
    console.print(
        "[green]Welcome! Let's get you set up for AI agent security testing.[/green]"
    )
    console.print()

    # Check if config already exists
    cli_config: CLIConfig = ctx.obj["config"]

    if cli_config.default_config_path.exists():
        if not click.confirm("Configuration already exists. Overwrite?"):
            display_info("Setup cancelled")
            return
        # Reload config from file to get the latest saved values
        cli_config._load_default_config()

    # API Key setup
    console.print("[cyan]📋 API Key Configuration[/cyan]")
    console.print(
        "Get your API key from: [link=https://hackagent.dev]https://hackagent.dev[/link]"
    )

    current_key = cli_config.api_key
    if current_key:
        console.print(f"Current API key: {current_key[:8]}...")
        if click.confirm("Keep current API key?"):
            api_key = current_key
        else:
            api_key = click.prompt("Enter your API key")
    else:
        api_key = click.prompt("Enter your API key")

    # Base URL is always the official endpoint
    base_url = "https://hackagent.dev"

    # Output format setup
    console.print("\n[cyan]📊 Output Format Configuration[/cyan]")
    output_format = click.prompt(
        "Default output format",
        type=click.Choice(["table", "json", "csv"]),
        default=cli_config.output_format,
    )

    # Save configuration
    cli_config.api_key = api_key
    cli_config.base_url = base_url
    cli_config.output_format = output_format

    try:
        cli_config.save()
        console.print(
            f"\n[bold green]✅ Configuration saved to: {cli_config.default_config_path}[/bold green]"
        )

        # Test the configuration
        console.print("\n[cyan]🔍 Testing configuration...[/cyan]")
        cli_config.validate()

        # Test API connection
        from hackagent.client import AuthenticatedClient
        from hackagent.api.key import key_list

        client = AuthenticatedClient(
            base_url=cli_config.base_url, token=cli_config.api_key, prefix="Api-Key"
        )

        with console.status("[bold green]Testing API connection..."):
            response = key_list.sync_detailed(client=client)

        if response.status_code == 200:
            console.print("[bold green]✅ API connection successful![/bold green]")
            console.print("\n[bold cyan]💡 You're ready to start! Try:[/bold cyan]")
            console.print("  [green]hackagent agent list[/green]")
            console.print("  [green]hackagent attack list[/green]")
            console.print("  [green]hackagent --help[/green]")
        else:
            console.print(
                f"[yellow]⚠️ API connection issue (Status: {response.status_code})[/yellow]"
            )
            console.print("Configuration saved, but you may need to check your API key")

    except Exception as e:
        console.print(f"[bold red]❌ Setup failed: {e}[/bold red]")
        ctx.exit(1)


@cli.command()
@click.pass_context
@handle_errors
def version(ctx):
    """📋 Show version information"""

    # Display the awesome ASCII logo
    from hackagent.utils import display_hackagent_splash

    display_hackagent_splash()

    console.print("[bold cyan]HackAgent CLI v0.2.4[/bold cyan]")
    console.print(
        "[bold green]Python Security Testing Toolkit for AI Agents[/bold green]"
    )
    console.print()

    # Show configuration status
    cli_config: CLIConfig = ctx.obj["config"]

    config_status = (
        "[green]✅ Configured[/green]"
        if cli_config.api_key
        else "[red]❌ Not configured[/red]"
    )
    console.print(f"[cyan]Configuration:[/cyan] {config_status}")
    console.print(f"[cyan]Config file:[/cyan] {cli_config.default_config_path}")
    console.print(f"[cyan]API Base URL:[/cyan] {cli_config.base_url}")

    if cli_config.api_key:
        console.print(f"[cyan]API Key:[/cyan] {cli_config.api_key[:8]}...")

    console.print()
    console.print(
        "[dim]For more information: [link=https://hackagent.dev]https://hackagent.dev[/link]"
    )


@cli.command()
@click.pass_context
@handle_errors
def doctor(ctx):
    """🔍 Diagnose common configuration issues

    Checks your setup and provides helpful troubleshooting information.
    """
    console.print("[bold cyan]🔍 HackAgent CLI Diagnostics")
    console.print()

    cli_config: CLIConfig = ctx.obj["config"]
    issues_found = 0

    # Check 1: Configuration file
    console.print("[cyan]📋 Configuration File")
    if cli_config.default_config_path.exists():
        console.print("[green]✅ Configuration file exists")
    else:
        console.print("[yellow]⚠️ No configuration file found")
        console.print("   💡 Run 'hackagent init' to create one")
        issues_found += 1

    # Check 2: API Key
    console.print("\n[cyan]🔑 API Key")
    if cli_config.api_key:
        console.print("[green]✅ API key is set")

        # Test API key format
        if len(cli_config.api_key) > 20:
            console.print("[green]✅ API key format looks valid")
        else:
            console.print("[yellow]⚠️ API key seems too short")
            issues_found += 1
    else:
        console.print("[red]❌ API key not set")
        console.print("   💡 Set with: hackagent config set --api-key YOUR_KEY")
        console.print("   💡 Or set HACKAGENT_API_KEY environment variable")
        issues_found += 1

    # Check 3: API Connection
    console.print("\n[cyan]🌐 API Connection")
    if cli_config.api_key:
        try:
            from hackagent.client import AuthenticatedClient
            from hackagent.api.key import key_list

            client = AuthenticatedClient(
                base_url=cli_config.base_url, token=cli_config.api_key, prefix="Api-Key"
            )

            with console.status("Testing API connection..."):
                response = key_list.sync_detailed(client=client)

            if response.status_code == 200:
                console.print("[green]✅ API connection successful")
            else:
                console.print(
                    f"[red]❌ API connection failed (Status: {response.status_code})"
                )
                console.print("   💡 Check your API key and network connection")
                issues_found += 1

        except Exception as e:
            console.print(f"[red]❌ API connection error: {e}")
            console.print("   💡 Check your API key and network connection")
            issues_found += 1
    else:
        console.print("[dim]⏭️ Skipped (no API key)")

    # Check 4: Dependencies
    console.print("\n[cyan]📦 Dependencies")
    pandas_spec = importlib.util.find_spec("pandas")
    if pandas_spec is not None:
        console.print("[green]✅ pandas available")
    else:
        console.print("[red]❌ pandas not found")
        console.print("   💡 Install with: pip install pandas")
        issues_found += 1

    yaml_spec = importlib.util.find_spec("yaml")
    if yaml_spec is not None:
        console.print("[green]✅ PyYAML available")
    else:
        console.print("[yellow]⚠️ PyYAML not found (optional)")
        console.print("   💡 Install with: pip install pyyaml")

    # Summary
    console.print("\n[cyan]📊 Summary")
    if issues_found == 0:
        console.print(
            "[bold green]✅ All checks passed! You're ready to use HackAgent."
        )
    else:
        console.print(
            f"[bold yellow]⚠️ Found {issues_found} issue(s) that should be addressed."
        )
        console.print("\n[cyan]💡 Quick fixes:")
        console.print("  hackagent init          # Interactive setup")
        console.print("  hackagent config set    # Set specific values")
        console.print("  hackagent --help        # Show all commands")


def _display_welcome():
    """Display welcome message and basic usage info"""

    # Display HackAgent splash
    from hackagent.utils import display_hackagent_splash

    display_hackagent_splash()

    welcome_text = """[bold cyan]Welcome to HackAgent CLI![/bold cyan] 🔍

[green]A powerful toolkit for testing AI agent security through automated attacks.[/green]

[bold yellow]🚀 Getting Started:[/bold yellow]
  1. Set up your API key:     [cyan]hackagent init[/cyan]
  2. List available agents:   [cyan]hackagent agent list[/cyan]  
  3. Run security tests:      [cyan]hackagent attack advprefix --help[/cyan]
  4. View results:            [cyan]hackagent results list[/cyan]

[bold blue]💡 Need help?[/bold blue] Use '[cyan]hackagent --help[/cyan]' or '[cyan]hackagent COMMAND --help[/cyan]'
[bold blue]🌐 Get your API key at:[/bold blue] [link=https://hackagent.dev]https://hackagent.dev[/link]"""

    panel = Panel(
        welcome_text, title="🔍 HackAgent CLI", border_style="red", padding=(1, 2)
    )
    console.print(panel)


# Add command groups
cli.add_command(config.config)
cli.add_command(agent.agent)
cli.add_command(attack.attack)
cli.add_command(results.results)


if __name__ == "__main__":
    cli()
