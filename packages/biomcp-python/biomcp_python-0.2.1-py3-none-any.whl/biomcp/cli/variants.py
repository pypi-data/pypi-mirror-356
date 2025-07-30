"""BioMCP Command Line Interface for genetic variants."""

import asyncio
from typing import Annotated, Optional

import typer

from .. import const
from ..variants import getter, search

variant_app = typer.Typer(help="Search and get variants from MyVariant.info.")


@variant_app.command("get")
def get_variant(
    variant_id: Annotated[
        str,
        typer.Argument(
            help="rsID (rs456) or MyVariant ID (chr1:g.1234A>G)",
        ),
    ],
    output_json: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Render in JSON format",
            case_sensitive=False,
        ),
    ] = False,
):
    """
    Get detailed information about a specific genetic variant.

    Supports HGVS identifiers (e.g., 'chr7:g.140453136A>T') or dbSNP rsIDs.

    Examples:
        Get by HGVS: biomcp variant get "chr7:g.140453136A>T"
        Get by rsID: biomcp variant get rs113488022
        Get as JSON: biomcp variant get rs113488022 --format json
    """
    if not variant_id:
        typer.echo("Error: A variant identifier must be provided.", err=True)
        raise typer.Exit(code=1)

    result = asyncio.run(
        getter.get_variant(variant_id, output_json=output_json)
    )
    typer.echo(result)


@variant_app.command("search")
def search_variant_cmd(
    gene: Annotated[
        Optional[str],
        typer.Option(
            "--gene",
            help="Gene symbol (e.g., BRCA1)",
        ),
    ] = None,
    hgvsp: Annotated[
        Optional[str],
        typer.Option(
            "--hgvsp",
            help="Protein notation (e.g., p.Val600Glu).",
        ),
    ] = None,
    hgvsc: Annotated[
        Optional[str],
        typer.Option(
            "--hgvsc",
            help="cDNA notation (e.g., c.1799T>A).",
        ),
    ] = None,
    rsid: Annotated[
        Optional[str],
        typer.Option(
            "--rsid",
            help="dbSNP rsID (e.g., rs113488022)",
        ),
    ] = None,
    region: Annotated[
        Optional[str],
        typer.Option(
            "--region",
            help="Genomic region (e.g., chr1:69000-70000)",
        ),
    ] = None,
    significance: Annotated[
        Optional[search.ClinicalSignificance],
        typer.Option(
            "--significance",
            help="Clinical significance (e.g., pathogenic, likely benign)",
            case_sensitive=False,
        ),
    ] = None,
    min_frequency: Annotated[
        Optional[float],
        typer.Option(
            "--min-frequency",
            help="Minimum gnomAD exome allele frequency (0.0 to 1.0)",
            min=0.0,
            max=1.0,
        ),
    ] = None,
    max_frequency: Annotated[
        Optional[float],
        typer.Option(
            "--max-frequency",
            help="Maximum gnomAD exome allele frequency (0.0 to 1.0)",
            min=0.0,
            max=1.0,
        ),
    ] = None,
    cadd: Annotated[
        Optional[float],
        typer.Option(
            "--cadd",
            help="Minimum CADD phred score",
            min=0.0,
        ),
    ] = None,
    polyphen: Annotated[
        Optional[search.PolyPhenPrediction],
        typer.Option(
            "--polyphen",
            help="PolyPhen-2 prediction: Probably damaging = D,"
            "Possibly damaging = P, Benign = B",
            case_sensitive=False,
        ),
    ] = None,
    sift: Annotated[
        Optional[search.SiftPrediction],
        typer.Option(
            "--sift",
            help="SIFT prediction: D = Deleterious, T = Tolerated",
            case_sensitive=False,
        ),
    ] = None,
    size: Annotated[
        int,
        typer.Option(
            "--size",
            help="Maximum number of results to return",
            min=1,
            max=100,
        ),
    ] = const.SYSTEM_PAGE_SIZE,
    sources: Annotated[
        Optional[str],
        typer.Option(
            "--sources",
            help="Specific sources to include in results (comma-separated)",
        ),
    ] = None,
    output_json: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Render in JSON format",
            case_sensitive=False,
        ),
    ] = False,
):
    query = search.VariantQuery(
        gene=gene,
        hgvsp=hgvsp,
        hgvsc=hgvsc,
        rsid=rsid,
        region=region,
        significance=significance,
        min_frequency=min_frequency,
        max_frequency=max_frequency,
        cadd=cadd,
        polyphen=polyphen,
        sift=sift,
        size=size,
        sources=sources.split(",") if sources else [],
    )

    result = asyncio.run(search.search_variants(query, output_json))
    typer.echo(result)
