"""CLI for BioMed-Enriched."""
from __future__ import annotations

from pathlib import Path
import logging
from typing import Optional, List

import typer

from . import populate

app = typer.Typer(add_help_option=True, rich_help_panel="BioMed-Enriched")


@app.command()
def main(
    dataset: Path = typer.Option(..., "--input", "-i", help="Path to input HF dataset"),
    xml_root: Path = typer.Option(..., "--xml-root", help="PMC XML dump root directory"),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional separate output directory. By default input is overwritten.",
    ),
    num_proc: int = typer.Option(None, "--num-proc", "-n", help="Number of parallel workers"),
    splits: List[str] = typer.Option(None, "--splits", "-s", help="One or more dataset splits (use 'all' for every split)"),
    index_dataset: Optional[str] = typer.Option(None, "--index", help="Local Parquet index path or HF dataset ID"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
) -> None:
    """Enrich dataset."""

    # Configure logging

    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        force=True,
    )

    splits_arg = list(splits) if splits else "non-comm"
    populate(str(dataset), xml_root, output, splits=splits_arg, num_proc=num_proc, index_dataset=index_dataset)


if __name__ == "__main__":  # pragma: no cover
    app() 