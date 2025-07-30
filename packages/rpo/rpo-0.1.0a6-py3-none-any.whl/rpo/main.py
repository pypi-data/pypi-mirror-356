import json
import logging
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Literal
from urllib.parse import quote

import click
import polars.selectors as cs
from click_option_group import optgroup

from rpo.analyzer import RepoAnalyzer
from rpo.models import (
    ActivityReportCmdOptions,
    BlameCmdOptions,
    DataSelectionOptions,
    GitOptions,
    PunchcardCmdOptions,
)
from rpo.types import AggregateBy, IdentifyBy, SortBy

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", logging.INFO),
    format="[%(asctime)s] %(levelname)s: %(name)s.%(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S.%s",
)
logger = logging.getLogger(__name__)


@click.group("rpo")
@click.option("--repository", "-r", type=click.Path(exists=True), default=Path.cwd())
@click.option("--branch", "-b", type=str, default=None)
@click.option(
    "--allow-dirty",
    is_flag=True,
    default=False,
    help="Proceed with analyis even if repository has uncommitted changes",
)
@optgroup(
    "File selection",
    help="Give you control over which files should be included in your analysis",
)
@optgroup.option(
    "--glob",
    "-g",
    "include_globs",
    type=str,
    multiple=True,
    help="File path glob patterns to INCLUDE. If specified, matching paths will be the only files included in aggregation.\
            If neither --glob nor --xglob are specified, all files will be included in aggregation. Paths are relative to root of repository.",
)
@optgroup.option(
    "--xglob",
    "-xg",
    "exclude_globs",
    type=str,
    multiple=True,
    help="File path glob patterns to EXCLUDE. If specified, matching paths will be filtered before aggregation.\
            If neither --glob nor --xglob are specified, all files will be included in aggregation. Paths are relative to root of repository.",
)
@optgroup.option(
    "--exclude-generated",
    "exclude_generated",
    is_flag=True,
    default=False,
    help="If set, exclude common generated files like package-manager generated lock files from analysis",
)
@optgroup(
    "Data selection", help="Control over how repository data is aggregated and sorted"
)
@optgroup.option(
    "--aggregate-by",
    "-A",
    "aggregate_by",
    type=str,
    help="Controls the field used to aggregate data",
    default="author",
)
@optgroup.option(
    "--identify-by",
    "-I",
    "identify_by",
    type=str,
    help="Controls the field used to identify auhors.",
    default="name",
)
@optgroup.option(
    "--sort-by",
    "-S",
    "sort_by",
    type=str,
    help="Controls the field used to sort output",
    default="user",
)
@optgroup("Plot options", help="Control plot output, if available")
@optgroup.option(
    "--plot",
    "-p",
    "plot_location",
    type=click.Path(dir_okay=True, file_okay=True),
    help="The directory where plot output visualization will live. Either a filename ending with '.png' or a directory.",
)
@optgroup("Output options", help="Control how data is displayed or saved")
@optgroup.option(
    "--save-as",
    type=click.Path(dir_okay=False, file_okay=True, writable=True),
    multiple=True,
    help="Save the report data to the path provided; format is determined by the filename extension,\
            which must be one of (.json|.csv). If no save-as path is provided, the report will be printed to stdout",
)
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(readable=True, dir_okay=False),
    help="The location of the json formatted config file to use. Defaults to a hidden config.json file in the current working directory. If it exists, then options in the config file take precedence over command line flags.",
)
@click.pass_context
def cli(
    ctx: click.Context,
    repository: str | None = None,
    branch: str | None = None,
    allow_dirty: bool = False,
    ignore_whitespace: bool = False,
    ignore_merges: bool = False,
    aggregate_by: AggregateBy = "author",
    identify_by: IdentifyBy = "name",
    sort_by: SortBy = "user",
    exclude_globs: list[str] | None = None,
    include_globs: list[str] | None = None,
    exclude_generated: bool = False,
    plot_location: os.PathLike[str] | None = None,
    save_as: Iterable[str | os.PathLike[str]] | None = None,
    exclude_users: list[str] | None = None,
    aliases: dict[str, str] | None = None,
    limit: int | None = None,
    config_file: os.PathLike[str] | None = None,
):
    _ = ctx.ensure_object(dict)

    if not config_file:
        default_xdg = Path.home() / ".config" / "rpo" / "config.json"
        for cfg in [default_xdg, Path.cwd() / ".rpo.config.json"]:
            if cfg.exists():
                config_file = cfg
                logger.warning(f"Using config file at {config_file}")
                break
        else:
            logger.warning("No config file found, using defaults and/or cmd line flags")

    if config_file:
        with open(config_file, "r") as f:
            config = json.load(f)

        allow_dirty = config.get("allow_dirty", allow_dirty)
        ignore_whitespace = config.get("ignore_whitespace", ignore_whitespace)
        ignore_merges = config.get("ignore_merges", ignore_merges)

        aggregate_by = config.get("aggregate_by", aggregate_by)
        sort_by = config.get("sort_by", sort_by)
        identify_by = config.get("identify_by", identify_by)

        include_globs = config.get("include_globs", include_globs)
        exclude_globs = config.get("exclude_globs", exclude_globs)
        exclude_generated = config.get("exclude_generated", exclude_generated)

        exclude_users = config.get("exclude_users", [])
        aliases = config.get("aliases", {})
        limit = config.get("limit", limit or 0)

        ctx.obj["config"] = config

    ctx.obj["analyzer"] = RepoAnalyzer(
        path=repository or Path.cwd(),
        options=GitOptions(
            branch=branch,
            allow_dirty=allow_dirty,
            ignore_whitespace=ignore_whitespace,
            ignore_merges=ignore_merges,
        ),
    )
    ctx.obj["data_selection"] = DataSelectionOptions(
        aggregate_by=aggregate_by,
        identify_by=identify_by,
        sort_by=sort_by,
        aliases=aliases or {},
        exclude_users=exclude_users or [],
        include_globs=include_globs,
        exclude_globs=exclude_globs,
        exclude_generated=exclude_generated,
    )

    ctx.obj["plot_location"] = plot_location
    ctx.obj["file_output"] = save_as


@cli.command()
@click.pass_context
def summary(ctx: click.Context):
    """Generate very high level summary for the repository"""
    ra = ctx.obj.get("analyzer")
    summary_df = ra.summary(ctx.obj.get("data_selection"))
    ra.output(summary_df, ctx.obj.get("file_output"))


@cli.command()
@click.pass_context
def revisions(ctx: click.Context):
    """List all revisions in the repository"""
    ra = ctx.obj.get("analyzer")
    revs = ra.revisions(ctx.obj.get("data_selection"))
    ra.output(revs, ctx.obj.get("file_output"))


@cli.command
@click.option(
    "--report-type",
    "-t",
    type=click.Choice(choices=["user", "users", "file", "files"]),
    default="user",
)
@click.pass_context
def activity_report(
    ctx: click.Context,
    report_type: Literal["user", "users", "file", "files"],
):
    """Produces file or author report of activity at a particular git revision"""
    ra = ctx.obj.get("analyzer")

    options = ActivityReportCmdOptions(**dict(ctx.obj.get("data_selection")))
    if report_type.lower().startswith("file"):
        report_df = ra.file_report(options)
    else:
        report_df = ra.contributor_report(options)
    ra.output(report_df, ctx.obj.get("file_output"))


@cli.command
@click.option("--revision", "-R", "revision", type=str, default=None)
@click.pass_context
def repo_blame(
    ctx: click.Context,
    revision: str,
):
    """Computes the per user blame for all files at a given revision"""
    ra: RepoAnalyzer = ctx.obj.get("analyzer")
    options = BlameCmdOptions(**dict(ctx.obj.get("data_selection")))
    data_key = "lines"
    blame_df = ra.blame(options, rev=revision, data_field=data_key)
    ra.output(blame_df, ctx.obj.get("file_output"))
    if plot := ctx.obj.get("plot_location"):
        chart = blame_df.plot.bar(x=f"{data_key}:Q", y=options.group_by_key).properties(
            title=f"{ra.path.name} Blame at {revision[:10] if revision else 'HEAD'}",
        )
        if isinstance(plot, str):
            plot = Path(plot)
        if not plot.name.endswith(".png"):
            _ = plot.mkdir(exist_ok=True, parents=True)
            plot = plot / f"{ra.path.name}_blame_by_{options.group_by_key}.png"
        chart.save(plot, ppi=200)
        logger.info(f"File written to {plot}")


@cli.command()
@click.pass_context
def cumulative_blame(ctx: click.Context):
    """Computes the cumulative blame of the repository over time. For every file in every revision,
    calculate the blame information.
    """
    ra: RepoAnalyzer = ctx.obj.get("analyzer")
    options = BlameCmdOptions(**dict(ctx.obj.get("data_selection")))
    data_key = "lines"
    blame_df = ra.cumulative_blame(options)
    ra.output(
        blame_df.pivot(
            [options.group_by_key],
            index="datetime",
            values=data_key,
            aggregate_function="sum",
        )
        .sort(cs.temporal())
        .fill_null(0),
        ctx.obj.get("file_output"),
    )

    if plot := ctx.obj.get("plot_location"):
        # see https://altair-viz.github.io/user_guide/marks/area.html
        chart = blame_df.plot.area(
            x="datetime:T",
            y=f"sum({data_key}):Q",
            color=f"{options.group_by_key}:N",
        ).properties(
            title=f"{ra.path.name} Cumulative Blame",
        )
        if isinstance(plot, str):
            plot = Path(plot)
        if not plot.name.endswith(".png"):
            _ = plot.mkdir(exist_ok=True, parents=True)
            plot = (
                plot / f"{ra.path.name}_cumulative_blame_by_{options.group_by_key}.png"
            )
        chart.save(plot, ppi=200)


@cli.command()
@click.argument("identifier", type=str)
@click.pass_context
def punchcard(ctx: click.Context, identifier: str):
    """Computes commits for a given user by datetime"""
    ra: RepoAnalyzer = ctx.obj.get("analyzer")
    options = PunchcardCmdOptions(
        **dict(ctx.obj.get("data_selection")),
        identifier=identifier,
    )
    punchcard_df = ra.punchcard(options)
    ra.output(punchcard_df, ctx.obj.get("file_output"))

    if plot := ctx.obj.get("plot_location"):
        # see https://altair-viz.github.io/user_guide/marks/area.html
        chart = (
            punchcard_df.rename({identifier: "count", options.punchcard_key: "time"})
            .plot.circle(
                x="hours(time):O",
                y="day(time):O",
                color="sum(count):Q",
                size="sum(count):Q",
            )
            .properties(
                title=f"{identifier} Punchcard".title(),
            )
        )
        if isinstance(plot, str):
            plot = Path(plot)
        if not plot.name.endswith(".png"):
            _ = plot.mkdir(exist_ok=True, parents=True)
            plot = plot / f"{ra.path.name}_punchcard_{quote(identifier)}.png"
        chart.save(plot, ppi=200)
