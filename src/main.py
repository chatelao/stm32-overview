import os
import sys
import click
import yaml

from src.core.repository import DataRepository
from src.core.registry import RegistryEngine
from src.core.comparison import ComparisonEngine
from src.core.recommendation import Constraints, RecommendationEngine
from src.core.generator import DocGenerator

# Initialize repository and registry
possible_dirs = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "specification"),
    "specification",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "specification")
]

spec_dir = "specification"
for d in possible_dirs:
    if os.path.isdir(d):
        spec_dir = d
        break

repository = DataRepository(spec_dir)
registry = RegistryEngine(repository)
comparison_engine = ComparisonEngine(registry)
recommendation_engine = RecommendationEngine(registry)

@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose debug output.")
@click.pass_context
def cli(ctx, verbose):
    """STM32 Workshop Microcontroller Overview and Comparison Tool."""
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose

@cli.command(name="list")
def list_boards():
    """List all registered STM32 boards."""
    try:
        boards = registry.list_boards()
        if not boards:
            click.echo("No registered boards found.")
            return
        click.echo("Registered STM32 boards:")
        for board in boards:
            click.echo(f"  - {board}")
    except Exception as e:
        click.echo(f"Error listing boards: {e}", err=True)
        sys.exit(1)

@cli.command(name="show")
@click.option("-b", "--board", required=True, help="Name of the board to inspect (e.g. Nucleo-F446RE).")
def show_board(board):
    """Show full details of a specific board."""
    try:
        details = registry.get_board_details(board)
        formatted = yaml.dump(details, default_flow_style=False, sort_keys=False)
        click.echo(formatted)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)

@cli.command(name="compare")
@click.option("-b", "--board", multiple=True, required=True, help="Names of the boards to compare (can be repeated).")
def compare_boards(board):
    """Compare two or more boards."""
    try:
        board_list = list(board)
        result = comparison_engine.compare(board_list)
        md_table = DocGenerator.to_markdown_table(result)
        click.echo(md_table)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)

@cli.command(name="recommend")
@click.option("-f", "--flash", type=int, default=0, help="Minimum flash capacity in KB. [Default: 0]")
@click.option("-s", "--sram", type=int, default=0, help="Minimum SRAM capacity in KB. [Default: 0]")
@click.option("-m", "--freq", type=int, default=0, help="Minimum clock frequency in MHz. [Default: 0]")
@click.option("-u", "--fpu", is_flag=True, help="Require Floating Point Unit (FPU).")
@click.option("-c", "--cordic", is_flag=True, help="Require CORDIC accelerator.")
@click.option("-a", "--fmac", is_flag=True, help="Require FMAC accelerator.")
@click.option("-d", "--dsp", is_flag=True, help="Require DSP support.")
@click.option("-r", "--arch", type=str, default="", help="Require CPU architecture (like M33, M4, M3).")
@click.option("-p", "--peripheral", multiple=True, help="Required peripherals (can be repeated).")
def recommend_board(flash, sram, freq, fpu, cordic, fmac, dsp, arch, peripheral):
    """Recommend a board based on constraints."""
    try:
        constraints = Constraints(
            min_flash_kb=flash,
            min_sram_kb=sram,
            min_freq_mhz=freq,
            requires_fpu=fpu,
            requires_cordic=cordic,
            requires_fmac=fmac,
            requires_dsp=dsp,
            requires_arch=arch,
            peripherals=list(peripheral)
        )
        recommendations = recommendation_engine.evaluate(constraints)
        if not recommendations:
            click.echo("No recommendations available.")
            return

        click.echo("Recommendations (sorted by match score):")
        for idx, rec in enumerate(recommendations, 1):
            click.echo(f"\n{idx}. Board: {rec.board_name} (Match Score: {rec.match_score}%)")
            click.echo(f"   Matched Features: {', '.join(rec.matched_features) if rec.matched_features else 'None'}")
            click.echo(f"   Missing Features: {', '.join(rec.missing_features) if rec.missing_features else 'None'}")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)

@cli.command(name="export")
@click.option("-o", "--output", default="docs/comparison_matrix.md", type=click.Path(), help="Target markdown file path for exporting comparison data. [Default: docs/comparison_matrix.md]")
def export_matrix(output):
    """Export comparison matrix to Markdown files."""
    try:
        boards = registry.list_boards()
        if not boards:
            click.echo("No boards to export.")
            return

        # Check if the output is a root-level file and already exists
        abs_output = os.path.abspath(output)
        abs_root = os.path.abspath(os.getcwd())
        if os.path.exists(abs_output) and os.path.dirname(abs_output) == abs_root:
            if not click.confirm(
                f"Warning: You are about to overwrite a root-level file '{os.path.basename(abs_output)}'. Do you want to continue?",
                default=False
            ):
                click.echo("Export aborted.")
                return

        result = comparison_engine.compare(boards)
        DocGenerator.export_report(result, output)
        click.echo(f"Successfully exported comparison matrix to '{output}'.")
    except Exception as e:
        click.echo(f"Error exporting comparison data: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    cli()
