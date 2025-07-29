"""Command-line interface for notion-to-json."""

import asyncio
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

import click
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from notion_to_json import __version__
from notion_to_json.client import NotionClient
from notion_to_json.exporter import JSONExporter
from notion_to_json.logging import console, get_logger, setup_logging

logger = get_logger(__name__)


def filter_items(
    items: list[dict],
    include_pattern: str | None = None,
    exclude_pattern: str | None = None,
    modified_after: datetime | None = None,
) -> list[dict]:
    """Filter items based on criteria.

    Args:
        items: List of items to filter
        include_pattern: Regex pattern for titles to include
        exclude_pattern: Regex pattern for titles to exclude
        modified_after: Only include items modified after this date

    Returns:
        Filtered list of items
    """
    filtered = []

    include_re = re.compile(include_pattern, re.IGNORECASE) if include_pattern else None
    exclude_re = re.compile(exclude_pattern, re.IGNORECASE) if exclude_pattern else None

    for item in items:
        # Extract title
        title = extract_title(item) if "properties" in item else extract_database_title(item)

        # Apply include pattern
        if include_re and not include_re.search(title):
            logger.debug(f"Skipping '{title}' - doesn't match include pattern")
            continue

        # Apply exclude pattern
        if exclude_re and exclude_re.search(title):
            logger.debug(f"Skipping '{title}' - matches exclude pattern")
            continue

        # Apply date filter
        if modified_after:
            last_edited = item.get("last_edited_time", "")
            if last_edited:
                item_date = datetime.fromisoformat(last_edited.replace("Z", "+00:00"))
                # Make modified_after timezone-aware if it isn't
                if modified_after.tzinfo is None:
                    modified_after_tz = modified_after.replace(tzinfo=UTC)
                else:
                    modified_after_tz = modified_after

                if item_date < modified_after_tz:
                    logger.debug(f"Skipping '{title}' - modified before {modified_after}")
                    continue

        filtered.append(item)

    return filtered


async def test_connection(api_key: str) -> bool:
    """Test connection to Notion API.

    Args:
        api_key: Notion API integration token

    Returns:
        True if connection successful, False otherwise
    """
    try:
        async with NotionClient(api_key) as client:
            console.print("[cyan]Testing connection to Notion API...[/cyan]")
            result = await client.get_users()

            if "results" in result:
                user_count = len(result["results"])
                console.print(f"[green]✓ Successfully connected! Found {user_count} users.[/green]")

                # Display first user info if available
                if user_count > 0:
                    first_user = result["results"][0]
                    user_type = first_user.get("type", "unknown")
                    user_name = first_user.get("name", "Unknown")
                    console.print(f"[dim]First user: {user_name} (type: {user_type})[/dim]")

                return True
            else:
                console.print("[red]✗ Unexpected response format from API[/red]")
                return False

    except Exception as e:
        console.print(f"[red]✗ Connection failed: {str(e)}[/red]")
        return False


async def search_workspace(api_key: str, show_all: bool = False, save_path: str | None = None) -> None:
    """Search and display all pages and databases in the workspace.

    Args:
        api_key: Notion API key
        show_all: Show all results, not just first 10
        save_path: Path to save the results to a file
    """
    async with NotionClient(api_key) as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Search for pages
            pages_task = progress.add_task("[cyan]Searching for pages...", total=None)
            pages = await client.search_pages()
            progress.remove_task(pages_task)

            # Search for databases
            db_task = progress.add_task("[cyan]Searching for databases...", total=None)
            databases = await client.search_databases()
            progress.remove_task(db_task)

        # Display results in a table
        console.print(f"\n[bold]Found {len(pages)} pages and {len(databases)} databases[/bold]\n")

        # Save to file if requested
        if save_path:
            save_results_to_file(pages, databases, save_path)
            console.print(f"[green]Results saved to: {save_path}[/green]\n")

        # Determine how many items to show
        page_limit = len(pages) if show_all else min(10, len(pages))
        db_limit = len(databases) if show_all else len(databases)  # Always show all databases

        # Pages table
        if pages:
            pages_table = Table(title="Pages", show_lines=True)
            pages_table.add_column("Title", style="cyan", no_wrap=False, width=50)
            pages_table.add_column("ID", style="dim")
            pages_table.add_column("URL", style="blue", no_wrap=False)
            pages_table.add_column("Last Edited", style="dim")

            for _i, page in enumerate(pages[:page_limit]):
                title = extract_title(page)
                page_id = page.get("id", "")
                url = page.get("url", "")
                last_edited = page.get("last_edited_time", "")[:10]  # Date only

                # Format URL for display
                notion_prefix = "https://www.notion.so/"
                short_url = url.replace(notion_prefix, "")
                display_url = short_url[:40] + "..." if len(short_url) > 40 else short_url

                pages_table.add_row(title, page_id[:8] + "...", display_url, last_edited)

            if not show_all and len(pages) > 10:
                pages_table.add_row(
                    f"[dim]... and {len(pages) - 10} more pages[/dim]",
                    "[dim]...[/dim]",
                    "[dim]Use --list-all to see all[/dim]",
                    "[dim]...[/dim]",
                )

            console.print(pages_table)

        # Databases table
        if databases:
            console.print()  # Add spacing
            db_table = Table(title="Databases", show_lines=True)
            db_table.add_column("Title", style="green", no_wrap=False, width=30)
            db_table.add_column("ID", style="dim")
            db_table.add_column("URL", style="blue", no_wrap=False)
            db_table.add_column("Last Edited", style="dim")

            for db in databases[:db_limit]:
                title = extract_database_title(db)
                db_id = db.get("id", "")
                url = db.get("url", "")
                last_edited = db.get("last_edited_time", "")[:10]  # Date only

                # Format URL for display
                notion_prefix = "https://www.notion.so/"
                short_url = url.replace(notion_prefix, "")
                display_url = short_url[:40] + "..." if len(short_url) > 40 else short_url

                db_table.add_row(title, db_id[:8] + "...", display_url, last_edited)

            console.print(db_table)

            if databases:
                console.print("\n[yellow]Note: Make sure your integration is shared with each database![/yellow]")


def extract_title(page: dict) -> str:
    """Extract title from a page object."""
    if "properties" in page:
        # Look for title property
        for _prop_name, prop_value in page["properties"].items():
            if prop_value.get("type") == "title":
                title_array = prop_value.get("title", [])
                if title_array and "plain_text" in title_array[0]:
                    return title_array[0]["plain_text"]
    return "Untitled"


def extract_database_title(database: dict) -> str:
    """Extract title from a database object."""
    title_array = database.get("title", [])
    if title_array and "plain_text" in title_array[0]:
        return title_array[0]["plain_text"]
    return "Untitled"


def save_results_to_file(pages: list[dict], databases: list[dict], file_path: str) -> None:
    """Save search results to a JSON file.

    Args:
        pages: List of page objects
        databases: List of database objects
        file_path: Path to save the file
    """
    # Prepare data with metadata
    data = {
        "export_date": datetime.now().isoformat(),
        "summary": {
            "total_pages": len(pages),
            "total_databases": len(databases),
        },
        "pages": [
            {
                "title": extract_title(page),
                "id": page.get("id", ""),
                "url": page.get("url", ""),
                "created_time": page.get("created_time", ""),
                "last_edited_time": page.get("last_edited_time", ""),
                "parent": page.get("parent", {}),
            }
            for page in pages
        ],
        "databases": [
            {
                "title": extract_database_title(db),
                "id": db.get("id", ""),
                "url": db.get("url", ""),
                "created_time": db.get("created_time", ""),
                "last_edited_time": db.get("last_edited_time", ""),
                "parent": db.get("parent", {}),
            }
            for db in databases
        ],
    }

    # Write to file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


async def retrieve_page_content(api_key: str, page_id: str, output_file: str | None = None) -> None:
    """Retrieve and display page content.

    Args:
        api_key: Notion API key
        page_id: ID of the page to retrieve
        output_file: Optional file to save content to
    """
    async with NotionClient(api_key) as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Get page metadata
            meta_task = progress.add_task("[cyan]Retrieving page metadata...", total=None)
            try:
                page = await client.get_page(page_id)
                progress.remove_task(meta_task)

                # Get page content
                content_task = progress.add_task("[cyan]Retrieving page content...", total=None)
                content = await client.get_page_content_recursive(page_id)
                progress.remove_task(content_task)

                # Combine metadata and content
                full_page = {
                    "metadata": page,
                    "content": content,
                    "retrieved_at": datetime.now().isoformat(),
                }

                if output_file:
                    # Save to file
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(full_page, f, indent=2, ensure_ascii=False)
                    console.print(f"[green]Page content saved to: {output_file}[/green]")
                else:
                    # Display summary
                    title = extract_title(page)
                    block_count = len(content.get("blocks", []))
                    console.print(f"\n[bold]Page: {title}[/bold]")
                    console.print(f"ID: {page_id}")
                    console.print(f"Blocks: {block_count}")
                    console.print(f"URL: {page.get('url', '')}")

            except Exception as e:
                progress.remove_task(meta_task)
                console.print(f"[red]Error retrieving page: {str(e)}[/red]")
                raise


async def retrieve_database_content(api_key: str, database_id: str, output_file: str | None = None) -> None:
    """Retrieve and display database content.

    Args:
        api_key: Notion API key
        database_id: ID of the database to retrieve
        output_file: Optional file to save content to
    """
    async with NotionClient(api_key) as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Get database schema
            schema_task = progress.add_task("[cyan]Retrieving database schema...", total=None)
            try:
                database = await client.get_database(database_id)
                progress.remove_task(schema_task)

                # Get database entries
                entries_task = progress.add_task("[cyan]Retrieving database entries...", total=None)
                entries = await client.get_all_database_entries(database_id)
                progress.remove_task(entries_task)

                # Combine schema and entries
                full_database = {
                    "schema": database,
                    "entries": entries,
                    "entry_count": len(entries),
                    "retrieved_at": datetime.now().isoformat(),
                }

                if output_file:
                    # Save to file
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(full_database, f, indent=2, ensure_ascii=False)
                    console.print(f"[green]Database content saved to: {output_file}[/green]")
                else:
                    # Display summary
                    title = extract_database_title(database)
                    console.print(f"\n[bold]Database: {title}[/bold]")
                    console.print(f"ID: {database_id}")
                    console.print(f"Entries: {len(entries)}")
                    console.print(f"Properties: {len(database.get('properties', {}))}")
                    console.print(f"URL: {database.get('url', '')}")

            except Exception as e:
                progress.remove_task(schema_task)
                console.print(f"[red]Error retrieving database: {str(e)}[/red]")
                raise


async def export_workspace(
    api_key: str,
    output_dir: str,
    filter_type: str = "all",
    include_pattern: str | None = None,
    exclude_pattern: str | None = None,
    modified_after: datetime | None = None,
) -> None:
    """Export entire workspace to JSON files.

    Args:
        api_key: Notion API key
        output_dir: Directory to save exported files
        filter_type: Type of content to export ("page", "database", or "all")
        include_pattern: Regex pattern for titles to include
        exclude_pattern: Regex pattern for titles to exclude
        modified_after: Only export items modified after this date
    """
    async with NotionClient(api_key) as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Discover all content
            discovery_task = progress.add_task("[cyan]Discovering workspace content...", total=None)

            pages = []
            databases = []

            # Get pages if needed
            if filter_type in ["all", "page"]:
                pages = await client.search_pages()
                logger.info(f"Found {len(pages)} pages")

            # Get databases if needed
            if filter_type in ["all", "database"]:
                databases = await client.search_databases()
                logger.info(f"Found {len(databases)} databases")

            progress.remove_task(discovery_task)

            # Apply filters
            if include_pattern or exclude_pattern or modified_after:
                original_page_count = len(pages)
                original_db_count = len(databases)

                pages = filter_items(pages, include_pattern, exclude_pattern, modified_after)
                databases = filter_items(databases, include_pattern, exclude_pattern, modified_after)

                logger.info(
                    f"After filtering: {len(pages)}/{original_page_count} pages, "
                    f"{len(databases)}/{original_db_count} databases"
                )

            console.print(f"\n[bold]Will export {len(pages)} pages and {len(databases)} databases[/bold]")

        # Create exporter and export everything
        exporter = JSONExporter(output_dir)
        await exporter.export_workspace(client, pages, databases)


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--api-key",
    envvar="NOTION_API_KEY",
    help="Notion API integration token",
    required=True,
)
@click.option(
    "--output-dir",
    default="./exports",
    help="Directory to save exported JSON files",
    type=click.Path(),
)
@click.option(
    "--test",
    is_flag=True,
    help="Test API connection only",
)
@click.option(
    "--search",
    is_flag=True,
    help="Search and list all pages and databases",
)
@click.option(
    "--list-all",
    is_flag=True,
    help="List all pages and databases (no limit)",
)
@click.option(
    "--save-list",
    type=click.Path(),
    help="Save the list of discovered content to a file",
)
@click.option(
    "--get-page",
    help="Retrieve content for a specific page by ID",
)
@click.option(
    "--get-database",
    help="Retrieve content for a specific database by ID",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for page/database content",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Minimize output (errors only)",
)
@click.option(
    "--log-file",
    type=click.Path(),
    help="Write logs to file",
)
@click.option(
    "--filter-type",
    type=click.Choice(["page", "database", "all"]),
    default="all",
    help="Export only specific type of content",
)
@click.option(
    "--include-pattern",
    help="Only export items with titles matching this pattern (regex)",
)
@click.option(
    "--exclude-pattern",
    help="Skip items with titles matching this pattern (regex)",
)
@click.option(
    "--modified-after",
    type=click.DateTime(),
    help="Only export items modified after this date",
)
def main(
    api_key: str,
    output_dir: str,
    test: bool,
    search: bool,
    list_all: bool,
    save_list: str | None,
    get_page: str | None,
    get_database: str | None,
    output: str | None,
    verbose: bool,
    quiet: bool,
    log_file: str | None,
    filter_type: str,
    include_pattern: str | None,
    exclude_pattern: str | None,
    modified_after: datetime | None,
) -> None:
    """Export Notion pages and databases to JSON."""
    # Setup logging first
    setup_logging(verbose=verbose, quiet=quiet, log_file=Path(log_file) if log_file else None)

    # Validate mutually exclusive options
    if verbose and quiet:
        console.print("[red]Error: Cannot use --verbose and --quiet together[/red]")
        sys.exit(1)

    if not quiet:
        console.print(
            Panel(
                f"[bold green]Notion to JSON Exporter v{__version__}[/bold green]",
                expand=False,
            )
        )

    logger.info(f"Starting notion-to-json v{__version__}")

    # Run async code
    if test:
        # Test mode - just verify connection
        success = asyncio.run(test_connection(api_key))
        sys.exit(0 if success else 1)
    elif get_page:
        # Retrieve specific page content
        asyncio.run(retrieve_page_content(api_key, get_page, output))
    elif get_database:
        # Retrieve specific database content
        asyncio.run(retrieve_database_content(api_key, get_database, output))
    elif search or list_all:
        # Search mode - discover all content
        asyncio.run(search_workspace(api_key, show_all=list_all, save_path=save_list))
    else:
        # Default behavior - export entire workspace
        console.print(f"Output directory: {output_dir}")

        # Test connection first
        success = asyncio.run(test_connection(api_key))
        if not success:
            console.print("[red]Please check your API key and try again.[/red]")
            sys.exit(1)

        # Export workspace with filters
        asyncio.run(
            export_workspace(
                api_key,
                output_dir,
                filter_type=filter_type,
                include_pattern=include_pattern,
                exclude_pattern=exclude_pattern,
                modified_after=modified_after,
            )
        )


if __name__ == "__main__":
    main()
