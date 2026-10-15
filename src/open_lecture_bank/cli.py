"""Command-line interface for Open Lecture Bank."""

import click
from pathlib import Path
from open_lecture_bank.config import AppConfig


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Open Lecture Bank: Transform lecture PDFs into validated MCQ question banks."""
    pass


@main.command()
@click.option("--input", "-i", type=click.Path(exists=True), default="./data/input", help="Directory containing lecture PDFs.")
def extract(input):
    """Extract page-indexed text from lecture PDFs (Stage 2)."""
    click.echo(f"Scanning input directory: {input}...")
    click.echo("Extraction engine is under development (Stage 2). See docs/ROADMAP.md.")


@main.command()
def analyze():
    """Analyze extracted text to synthesize examinable topics (Stage 3)."""
    click.echo("Topic analyzer is under development (Stage 3). See docs/ROADMAP.md.")


@main.command()
@click.option("--batch-size", "-b", type=int, default=3, help="Number of lectures per batch.")
def generate(batch_size):
    """Generate 4-option MCQs from synthesized topics (Stage 3)."""
    click.echo(f"Generating questions with batch size: {batch_size}...")
    click.echo("Question generator is under development (Stage 3). See docs/ROADMAP.md.")


@main.command()
def validate():
    """Perform psychometric and option parity validation (Stage 4)."""
    click.echo("Validating assessment question bank (Stage 4). See docs/ROADMAP.md.")


@main.command()
@click.option("--output", "-o", type=click.Path(), default="./data/output", help="Output directory.")
def export(output):
    """Export consolidated question bank and manifest (Stage 5)."""
    click.echo(f"Exporting to directory: {output}...")
    click.echo("Exporter is under development (Stage 5). See docs/ROADMAP.md.")


@main.command()
@click.option("--input", "-i", type=click.Path(exists=True), default="./data/input", help="Input PDF directory.")
@click.option("--output", "-o", type=click.Path(), default="./data/output", help="Output directory.")
def run(input, output):
    """Execute the full end-to-end processing pipeline."""
    click.echo(f"Starting Open Lecture Bank pipeline from {input} to {output}...")
    click.echo("Full pipeline orchestration planned for Stage 5. See docs/ROADMAP.md.")


if __name__ == "__main__":
    main()
