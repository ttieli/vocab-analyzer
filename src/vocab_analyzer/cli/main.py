"""
Main CLI interface for vocab-analyzer.
"""
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.progress import track

from ..analyzers import StatisticsAnalyzer
from ..core.analyzer import VocabularyAnalyzer
from ..core.config import Config
from ..exporters import CsvExporter, JsonExporter, MarkdownExporter

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="vocab-analyzer")
def cli():
    """
    Vocab Analyzer - English Book Vocabulary Level Analysis Tool

    Analyze vocabulary in English texts and classify by CEFR levels (A1-C2).
    """
    pass


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "csv", "markdown", "md"], case_sensitive=False),
    default="json",
    help="Output format (default: json)",
)
@click.option(
    "--output", "-o", type=click.Path(), help="Output file path (default: auto-generated)"
)
@click.option(
    "--no-examples", is_flag=True, help="Exclude example sentences from output"
)
@click.option(
    "--min-level",
    type=click.Choice(["A1", "A2", "B1", "B2", "C1", "C2"], case_sensitive=False),
    help="Minimum CEFR level to include",
)
@click.option(
    "--max-level",
    type=click.Choice(["A1", "A2", "B1", "B2", "C1", "C2", "C2+"], case_sensitive=False),
    help="Maximum CEFR level to include",
)
@click.option("--config", "-c", type=click.Path(exists=True), help="Custom config file")
@click.option("--quiet", "-q", is_flag=True, help="Suppress progress output")
def analyze(file_path, format, output, no_examples, min_level, max_level, config, quiet):
    """
    Analyze vocabulary in a file.

    Supports TXT, PDF, DOCX, and JSON formats.

    Example:
        vocab-analyzer analyze book.txt --format csv --output results.csv
    """
    try:
        # Load config
        cfg = Config(config) if config else Config()

        if not quiet:
            console.print(f"\n[bold blue]Analyzing:[/bold blue] {file_path}")
            console.print(f"[dim]Format: {format.upper()}[/dim]\n")

        # Create analyzer
        analyzer = VocabularyAnalyzer(cfg)

        # Analyze file
        if not quiet:
            with console.status("[bold green]Processing text..."):
                result = analyzer.analyze(file_path)
        else:
            result = analyzer.analyze(file_path)

        # Filter by level if specified
        if min_level or max_level:
            result = _filter_by_level(result, min_level, max_level)

        # Determine output file
        if not output:
            from ..utils import get_output_file_path

            output = str(get_output_file_path(file_path, format.lower().replace("md", "markdown")))

        # Export
        include_examples = not no_examples

        if format.lower() == "json":
            exporter = JsonExporter()
            exporter.export(result, output, include_words=True, include_phrases=False)

        elif format.lower() == "csv":
            exporter = CsvExporter()
            exporter.export(result, output, include_examples=include_examples)

        elif format.lower() in ["markdown", "md"]:
            exporter = MarkdownExporter()
            exporter.export(result, output, include_examples=include_examples)

        if not quiet:
            console.print(f"\n[bold green]✓ Analysis complete![/bold green]")
            console.print(f"[dim]Output saved to: {output}[/dim]")

            # Print summary
            console.print("\n[bold]Quick Summary:[/bold]")
            console.print(f"  • Total unique words: {len(result.words)}")
            console.print(
                f"  • Total occurrences: {result.statistics['total_word_occurrences']}"
            )

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}", style="red")
        if not quiet:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--config", "-c", type=click.Path(exists=True), help="Custom config file")
def stats(file_path, config):
    """
    Show statistics for a file without exporting.

    Example:
        vocab-analyzer stats book.txt
    """
    try:
        # Load config
        cfg = Config(config) if config else Config()

        console.print(f"\n[bold blue]Analyzing:[/bold blue] {file_path}\n")

        # Create analyzer
        analyzer = VocabularyAnalyzer(cfg)

        # Analyze
        with console.status("[bold green]Processing..."):
            result = analyzer.analyze(file_path)

        # Print statistics
        StatisticsAnalyzer.print_summary(result)

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--levels",
    "-l",
    multiple=True,
    type=click.Choice(["A1", "A2", "B1", "B2", "C1", "C2", "C2+"], case_sensitive=False),
    help="Specific levels to extract (can specify multiple)",
)
@click.option("--config", "-c", type=click.Path(exists=True), help="Custom config file")
def extract(file_path, levels, config):
    """
    Extract vocabulary for specific CEFR levels.

    Example:
        vocab-analyzer extract book.txt --levels B2 --levels C1
    """
    try:
        # Load config
        cfg = Config(config) if config else Config()

        if not levels:
            console.print(
                "[yellow]No levels specified. Use --levels option (e.g., --levels B2)[/yellow]"
            )
            return

        console.print(f"\n[bold blue]Extracting levels {', '.join(levels)} from:[/bold blue] {file_path}\n")

        # Create analyzer
        analyzer = VocabularyAnalyzer(cfg)

        # Analyze
        with console.status("[bold green]Processing..."):
            result = analyzer.analyze(file_path)

        # Extract words for specified levels
        for level in levels:
            words = result.get_words_by_level(level)
            console.print(f"\n[bold]{level} Level ({len(words)} words):[/bold]")

            for word in sorted(words, key=lambda w: w.frequency, reverse=True)[:20]:
                console.print(f"  • {word.word:15} (freq: {word.frequency:2}) - {word.definition_cn[:40] if word.definition_cn else 'N/A'}")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}", style="red")
        sys.exit(1)


def _filter_by_level(analysis, min_level, max_level):
    """Filter analysis results by CEFR level range."""
    level_order = ["A1", "A2", "B1", "B2", "C1", "C2", "C2+"]

    min_idx = level_order.index(min_level) if min_level else 0
    max_idx = level_order.index(max_level) if max_level else len(level_order) - 1

    allowed_levels = set(level_order[min_idx : max_idx + 1])

    # Create new analysis with filtered words
    from ..models import VocabularyAnalysis

    filtered = VocabularyAnalysis(source_file=analysis.source_file)

    for word in analysis.words.values():
        if word.level in allowed_levels:
            filtered.add_word(word)

    return filtered


@cli.command()
@click.option(
    "--host",
    "-h",
    default="127.0.0.1",
    help="Host to bind the web server (default: 127.0.0.1)",
)
@click.option(
    "--port", "-p", default=5000, type=int, help="Port to bind the web server (default: 5000)"
)
@click.option("--debug", is_flag=True, help="Run in debug mode with auto-reload")
def web(host, port, debug):
    """
    Start the web interface for vocabulary analysis.

    Example:
        vocab-analyzer web --debug
        vocab-analyzer web --host 0.0.0.0 --port 8080
    """
    try:
        from ..web.app import create_app

        console.print(f"\n[bold blue]Starting Vocabulary Analyzer Web Interface[/bold blue]")
        console.print(f"[dim]Server: http://{host}:{port}[/dim]")
        console.print(f"[dim]Debug mode: {'ON' if debug else 'OFF'}[/dim]\n")

        if not debug:
            console.print(
                "[yellow]Tip: Use --debug flag for development with auto-reload[/yellow]\n"
            )

        app = create_app()
        app.run(host=host, port=port, debug=debug)

    except ImportError as e:
        console.print(
            f"\n[bold red]Error:[/bold red] Flask web dependencies not installed", style="red"
        )
        console.print(f"[dim]Install with: pip install 'Flask>=3.0.0' 'pytest-flask>=1.3.0'[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
