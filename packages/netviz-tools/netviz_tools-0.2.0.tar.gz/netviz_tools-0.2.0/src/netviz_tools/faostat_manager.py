"""
FAOSTAT Data Manager

This module provides specialized functionality for working with FAOSTAT agricultural trade data.
It extends the base DataManager class with methods specifically designed for loading, filtering,
and analyzing FAOSTAT trade networks.

Features:
    - Easy loading of FAOSTAT commodity data
    - Browse available commodities
    - Filter by commodity, year, country
    - Integrate with economic/country data
    - Create trade networks for specific crops
    - Multi-commodity analysis
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

import networkx as nx
import pandas as pd
from pydantic import Field
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from .data_manager import DataManager

logger = logging.getLogger(__name__)
console = Console()


class FAOSTATManager(DataManager):
    """
    A specialized data manager for FAOSTAT agricultural trade data.

    This class extends DataManager with FAOSTAT-specific functionality for
    loading commodity trade data, browsing available items, and creating
    agricultural trade networks.

    Attributes:
        faostat_dir (Path): Path to FAOSTAT data directory
        available_items (List[str]): List of available commodity items
        loaded_commodities (Set[str]): Set of currently loaded commodities
    """

    # Add FAOSTAT-specific fields to the Pydantic model
    faostat_dir: Path = Field(
        default=None, description="Path to FAOSTAT data directory"
    )
    items_dir: Path = Field(default=None, description="Path to FAOSTAT items directory")
    available_items: List[str] = Field(
        default_factory=list, description="List of available commodity items"
    )
    loaded_commodities: Set[str] = Field(
        default_factory=set, description="Set of currently loaded commodities"
    )

    def __init__(self, faostat_dir: Optional[Union[str, Path]] = None, **kwargs):
        """
        Initialize FAOSTAT Manager.

        Args:
            faostat_dir: Path to FAOSTAT data directory (defaults to data/example_data/faostat)
            **kwargs: Additional arguments passed to DataManager
        """
        # Set up FAOSTAT-specific paths before calling super().__init__
        if faostat_dir is None:
            data_dir = kwargs.get("data_dir", Path(__file__).parent / "data")
            faostat_dir = Path(data_dir) / "example_data" / "faostat"
        else:
            faostat_dir = Path(faostat_dir)

        if not faostat_dir.exists():
            raise FileNotFoundError(f"FAOSTAT directory not found: {faostat_dir}")

        items_dir = faostat_dir / "items"

        # Set FAOSTAT-specific column mappings as defaults
        kwargs.setdefault("src_col", "o_name")  # origin country name
        kwargs.setdefault("tgt_col", "d_name")  # destination country name
        kwargs.setdefault("weight_col", "weight")  # trade volume
        kwargs.setdefault("year_col", "year")

        # Initialize parent class first
        super().__init__(**kwargs)

        # Set FAOSTAT-specific attributes after parent initialization
        object.__setattr__(self, "faostat_dir", faostat_dir)
        object.__setattr__(self, "items_dir", items_dir)
        object.__setattr__(self, "available_items", [])
        object.__setattr__(self, "loaded_commodities", set())

        # Load available items after initialization
        self._load_available_items()

        logger.info(
            f"FAOSTAT Manager initialized with {len(self.available_items)} available commodities"
        )

    def _load_available_items(self) -> None:
        """Load list of available commodity items from items.txt file."""
        items_file = self.faostat_dir / "items.txt"

        if items_file.exists():
            with open(items_file, "r", encoding="utf-8") as f:
                items = [line.strip() for line in f if line.strip()]
                # Update the available_items using model assignment
                object.__setattr__(self, "available_items", items)
        else:
            # Fallback: scan items directory
            if self.items_dir.exists():
                items = [f.stem for f in self.items_dir.glob("*.csv")]
                object.__setattr__(self, "available_items", items)
            else:
                logger.warning("No FAOSTAT items found")
                object.__setattr__(self, "available_items", [])

    def list_commodities(self, search: Optional[str] = None, limit: int = 50) -> None:
        """
        Display available commodities in a formatted table.

        Args:
            search: Optional search term to filter commodities
            limit: Maximum number of items to display
        """
        items = self.available_items.copy()

        if search:
            search_lower = search.lower()
            items = [item for item in items if search_lower in item.lower()]

        if not items:
            console.print("[red]No commodities found[/red]")
            return

        # Limit results
        if len(items) > limit:
            items = items[:limit]
            showing_limited = True
        else:
            showing_limited = False

        # Create table
        table = Table(
            title=f"Available FAOSTAT Commodities{f' (search: {search})' if search else ''}"
        )
        table.add_column("Index", style="cyan", width=6)
        table.add_column("Commodity", style="green")
        table.add_column("Status", style="yellow", width=10)

        for i, item in enumerate(items, 1):
            status = "Loaded" if item in self.loaded_commodities else ""
            # Format commodity name (replace underscores with spaces, title case)
            display_name = item.replace("_", " ").title()
            table.add_row(str(i), display_name, status)

        console.print(table)

        if showing_limited:
            console.print(
                f"[yellow]Showing first {limit} results. Use search parameter to narrow down.[/yellow]"
            )

    def search_commodities(self, search_term: str) -> List[str]:
        """
        Search for commodities containing the search term.

        Args:
            search_term: Term to search for in commodity names

        Returns:
            List of matching commodity names
        """
        search_lower = search_term.lower()
        matches = [
            item for item in self.available_items if search_lower in item.lower()
        ]
        return matches

    def load_commodity(self, commodity: str, append: bool = True) -> None:
        """
        Load trade data for a specific commodity.

        Args:
            commodity: Name of the commodity to load
            append: If True, append to existing data; if False, replace existing data
        """
        if commodity not in self.available_items:
            # Try to find close matches
            matches = self.search_commodities(commodity)
            if matches:
                console.print(f"[red]'{commodity}' not found. Did you mean:[/red]")
                for match in matches[:5]:
                    console.print(f"  - {match.replace('_', ' ').title()}")
                return
            else:
                raise ValueError(
                    f"Commodity '{commodity}' not found in available items"
                )

        # Load the commodity data
        commodity_file = self.items_dir / f"{commodity}.csv"

        if not commodity_file.exists():
            raise FileNotFoundError(f"Data file not found: {commodity_file}")

        try:
            commodity_data = pd.read_csv(commodity_file)
            logger.info(f"Loaded {len(commodity_data)} trade records for {commodity}")

            if append and not self.edges.empty:
                # Append to existing data
                new_edges = pd.concat([self.edges, commodity_data], ignore_index=True)
                object.__setattr__(self, "edges", new_edges)
            else:
                # Replace existing data
                object.__setattr__(self, "edges", commodity_data)
                object.__setattr__(self, "loaded_commodities", set())

            # Update loaded commodities
            new_loaded = self.loaded_commodities.copy()
            new_loaded.add(commodity)
            object.__setattr__(self, "loaded_commodities", new_loaded)

            # Re-run setup steps
            self._normalize_column_names()
            self._detect_years()
            self._detect_types()
            self._derive_nodes_if_needed()

            console.print(
                f"[green]Successfully loaded {commodity.replace('_', ' ').title()}[/green]"
            )
            console.print(f"Total records: {len(self.edges)}")

        except Exception as e:
            logger.error(f"Error loading commodity {commodity}: {e}")
            raise

    def load_commodities(self, commodities: List[str]) -> None:
        """
        Load multiple commodities at once.

        Args:
            commodities: List of commodity names to load
        """
        console.print(f"Loading {len(commodities)} commodities...")

        all_data = []
        successful_loads = []

        with Progress() as progress:
            task = progress.add_task("Loading commodities...", total=len(commodities))

            for commodity in commodities:
                try:
                    if commodity not in self.available_items:
                        console.print(f"[red]Skipping '{commodity}' - not found[/red]")
                        continue

                    commodity_file = self.items_dir / f"{commodity}.csv"
                    if commodity_file.exists():
                        data = pd.read_csv(commodity_file)
                        all_data.append(data)
                        successful_loads.append(commodity)
                    else:
                        console.print(f"[red]File not found for '{commodity}'[/red]")

                except Exception as e:
                    console.print(f"[red]Error loading '{commodity}': {e}[/red]")

                progress.update(task, advance=1)

        if all_data:
            # Combine all data
            combined_edges = pd.concat(all_data, ignore_index=True)
            object.__setattr__(self, "edges", combined_edges)
            object.__setattr__(self, "loaded_commodities", set(successful_loads))

            # Re-run setup steps
            self._normalize_column_names()
            self._detect_years()
            self._detect_types()
            self._derive_nodes_if_needed()

            console.print(
                f"[green]Successfully loaded {len(successful_loads)} commodities[/green]"
            )
            console.print(f"Total records: {len(self.edges)}")
            console.print(
                f"Loaded commodities: {', '.join([c.replace('_', ' ').title() for c in successful_loads])}"
            )
        else:
            console.print("[red]No commodities were successfully loaded[/red]")

    def get_commodity_info(self, commodity: str) -> Dict:
        """
        Get information about a specific commodity's trade data.

        Args:
            commodity: Name of the commodity

        Returns:
            Dictionary with commodity information
        """
        if commodity not in self.loaded_commodities:
            raise ValueError(
                f"Commodity '{commodity}' not loaded. Use load_commodity() first."
            )

        # Filter data for this commodity
        commodity_data = self.edges[self.edges["item"] == commodity]

        info = {
            "name": commodity.replace("_", " ").title(),
            "total_records": len(commodity_data),
            "countries_exporting": commodity_data[self.src_col].nunique(),
            "countries_importing": commodity_data[self.tgt_col].nunique(),
            "years_available": sorted(commodity_data[self.year_col].unique().tolist()),
            "year_range": (
                commodity_data[self.year_col].min(),
                commodity_data[self.year_col].max(),
            ),
            "total_volume": commodity_data[self.weight_col].sum(),
            "top_exporters": commodity_data.groupby(self.src_col)[self.weight_col]
            .sum()
            .sort_values(ascending=False)
            .head(5),
            "top_importers": commodity_data.groupby(self.tgt_col)[self.weight_col]
            .sum()
            .sort_values(ascending=False)
            .head(5),
        }

        return info

    def commodity_summary(self, commodity: Optional[str] = None) -> None:
        """
        Display summary information for a commodity or all loaded commodities.

        Args:
            commodity: Specific commodity name, or None for all loaded commodities
        """
        if commodity:
            if commodity not in self.loaded_commodities:
                console.print(f"[red]Commodity '{commodity}' not loaded[/red]")
                return

            info = self.get_commodity_info(commodity)

            # Create detailed table for single commodity
            table = Table(title=f"Commodity Summary: {info['name']}")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("Total Records", f"{info['total_records']:,}")
            table.add_row("Exporting Countries", str(info["countries_exporting"]))
            table.add_row("Importing Countries", str(info["countries_importing"]))
            table.add_row(
                "Year Range", f"{info['year_range'][0]} - {info['year_range'][1]}"
            )
            table.add_row("Total Volume", f"{info['total_volume']:,.0f}")

            console.print(table)

            # Top exporters
            console.print("\n[bold]Top Exporters:[/bold]")
            for country, volume in info["top_exporters"].head(5).items():
                console.print(f"  {country}: {volume:,.0f}")

            # Top importers
            console.print("\n[bold]Top Importers:[/bold]")
            for country, volume in info["top_importers"].head(5).items():
                console.print(f"  {country}: {volume:,.0f}")

        else:
            # Summary for all loaded commodities
            if not self.loaded_commodities:
                console.print("[yellow]No commodities loaded[/yellow]")
                return

            table = Table(title="Loaded Commodities Summary")
            table.add_column("Commodity", style="cyan")
            table.add_column("Records", style="green", justify="right")
            table.add_column("Countries", style="blue", justify="right")
            table.add_column("Years", style="yellow")
            table.add_column("Total Volume", style="magenta", justify="right")

            for commodity in sorted(self.loaded_commodities):
                info = self.get_commodity_info(commodity)
                table.add_row(
                    info["name"],
                    f"{info['total_records']:,}",
                    f"{info['countries_exporting']}→{info['countries_importing']}",
                    f"{info['year_range'][0]}-{info['year_range'][1]}",
                    f"{info['total_volume']:,.0f}",
                )

            console.print(table)

    def filter_by_commodity(
        self, commodities: Union[str, List[str]]
    ) -> "FAOSTATManager":
        """
        Filter data to include only specific commodities.

        Args:
            commodities: Single commodity name or list of commodity names

        Returns:
            New FAOSTATManager instance with filtered data
        """
        if isinstance(commodities, str):
            commodities = [commodities]

        # Check if all commodities are loaded
        missing = [c for c in commodities if c not in self.loaded_commodities]
        if missing:
            raise ValueError(f"Commodities not loaded: {missing}")

        # Filter edges
        filtered_edges = self.edges[self.edges["item"].isin(commodities)].copy()

        # Create new manager instance
        new_manager = FAOSTATManager(
            faostat_dir=self.faostat_dir,
            src_col=self.src_col,
            tgt_col=self.tgt_col,
            weight_col=self.weight_col,
            year_col=self.year_col,
            label_col=self.label_col,
            data_dir=self.data_dir,
            edges=filtered_edges,
            nodes=self.nodes.copy() if not self.nodes.empty else pd.DataFrame(),
        )

        object.__setattr__(new_manager, "loaded_commodities", set(commodities))

        logger.info(f"Filtered data by commodities: {len(filtered_edges)} edges")
        return new_manager

    def filter_by_countries(
        self,
        exporters: Optional[Union[str, List[str]]] = None,
        importers: Optional[Union[str, List[str]]] = None,
    ) -> "FAOSTATManager":
        """
        Filter data by exporting and/or importing countries.

        Args:
            exporters: Single country name or list of exporter countries
            importers: Single country name or list of importer countries

        Returns:
            New FAOSTATManager instance with filtered data
        """
        filtered_edges = self.edges.copy()

        if exporters:
            if isinstance(exporters, str):
                exporters = [exporters]
            filtered_edges = filtered_edges[
                filtered_edges[self.src_col].isin(exporters)
            ]

        if importers:
            if isinstance(importers, str):
                importers = [importers]
            filtered_edges = filtered_edges[
                filtered_edges[self.tgt_col].isin(importers)
            ]

        # Create new manager instance
        new_manager = FAOSTATManager(
            faostat_dir=self.faostat_dir,
            src_col=self.src_col,
            tgt_col=self.tgt_col,
            weight_col=self.weight_col,
            year_col=self.year_col,
            label_col=self.label_col,
            data_dir=self.data_dir,
            edges=filtered_edges,
            nodes=self.nodes.copy() if not self.nodes.empty else pd.DataFrame(),
        )

        object.__setattr__(
            new_manager, "loaded_commodities", self.loaded_commodities.copy()
        )

        logger.info(f"Filtered data by countries: {len(filtered_edges)} edges")
        return new_manager

    def get_trade_flows(
        self,
        commodity: Optional[str] = None,
        year: Optional[int] = None,
        min_volume: Optional[float] = None,
    ) -> pd.DataFrame:
        """
        Get trade flows with optional filtering.

        Args:
            commodity: Specific commodity to filter by
            year: Specific year to filter by
            min_volume: Minimum trade volume to include

        Returns:
            DataFrame with trade flows
        """
        flows = self.edges.copy()

        if commodity:
            if commodity not in self.loaded_commodities:
                raise ValueError(f"Commodity '{commodity}' not loaded")
            flows = flows[flows["item"] == commodity]

        if year:
            flows = flows[flows[self.year_col] == year]

        if min_volume:
            flows = flows[flows[self.weight_col] >= min_volume]

        return flows.sort_values(self.weight_col, ascending=False)

    def top_trade_partners(
        self,
        country: str,
        role: str = "both",
        commodity: Optional[str] = None,
        year: Optional[int] = None,
        top_n: int = 10,
    ) -> pd.DataFrame:
        """
        Get top trade partners for a specific country.

        Args:
            country: Country name
            role: "exporter", "importer", or "both"
            commodity: Specific commodity to analyze
            year: Specific year to analyze
            top_n: Number of top partners to return

        Returns:
            DataFrame with top trade partners
        """
        flows = self.get_trade_flows(commodity=commodity, year=year)

        if role in ["exporter", "both"]:
            exports = flows[flows[self.src_col] == country]
            export_partners = (
                exports.groupby(self.tgt_col)[self.weight_col]
                .sum()
                .sort_values(ascending=False)
                .head(top_n)
            )

        if role in ["importer", "both"]:
            imports = flows[flows[self.tgt_col] == country]
            import_partners = (
                imports.groupby(self.src_col)[self.weight_col]
                .sum()
                .sort_values(ascending=False)
                .head(top_n)
            )

        if role == "exporter":
            return export_partners.to_frame("export_volume")
        elif role == "importer":
            return import_partners.to_frame("import_volume")
        else:
            # Combine both
            result = pd.DataFrame(
                index=set(export_partners.index) | set(import_partners.index)
            )
            result["export_volume"] = export_partners
            result["import_volume"] = import_partners
            result = result.fillna(0)
            result["total_volume"] = result["export_volume"] + result["import_volume"]
            return result.sort_values("total_volume", ascending=False).head(top_n)

    def create_trade_network(
        self,
        commodity: Optional[str] = None,
        year: Optional[int] = None,
        min_volume: Optional[float] = None,
        directed: bool = True,
    ) -> nx.Graph:
        """
        Create a NetworkX graph from trade flows.

        Args:
            commodity: Specific commodity to include
            year: Specific year to include
            min_volume: Minimum trade volume for edges
            directed: Whether to create directed graph

        Returns:
            NetworkX graph
        """
        flows = self.get_trade_flows(
            commodity=commodity, year=year, min_volume=min_volume
        )

        # Create temporary manager with filtered data
        temp_manager = FAOSTATManager(
            faostat_dir=self.faostat_dir,
            edges=flows,
            nodes=self.nodes.copy() if not self.nodes.empty else pd.DataFrame(),
            src_col=self.src_col,
            tgt_col=self.tgt_col,
            weight_col=self.weight_col,
            year_col=self.year_col,
            label_col=self.label_col,
        )

        return temp_manager.to_networkx(directed=directed, filter_year=year)

    def compare_commodities(
        self,
        commodities: List[str],
        metric: str = "total_volume",
        year: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Compare different commodities by various metrics.

        Args:
            commodities: List of commodities to compare
            metric: Metric to compare ("total_volume", "countries", "records")
            year: Specific year to analyze

        Returns:
            DataFrame with comparison results
        """
        results = []

        for commodity in commodities:
            if commodity not in self.loaded_commodities:
                continue

            flows = self.get_trade_flows(commodity=commodity, year=year)

            if metric == "total_volume":
                value = flows[self.weight_col].sum()
            elif metric == "countries":
                value = len(set(flows[self.src_col]) | set(flows[self.tgt_col]))
            elif metric == "records":
                value = len(flows)
            else:
                raise ValueError(f"Unknown metric: {metric}")

            results.append(
                {"commodity": commodity.replace("_", " ").title(), "value": value}
            )

        df = pd.DataFrame(results).sort_values("value", ascending=False)
        return df

    def load_country_data(self) -> None:
        """Load country/economic data from the nodes.csv file."""
        nodes_file = self.data_dir / "example_data" / "nodes.csv"

        if nodes_file.exists():
            nodes_df = pd.read_csv(nodes_file)
            object.__setattr__(self, "nodes", nodes_df)
            # Normalize column names
            self._normalize_column_names()
            logger.info(f"Loaded country data: {len(self.nodes)} countries")
            console.print(
                f"[green]Loaded country data for {len(self.nodes)} countries[/green]"
            )
        else:
            logger.warning("Country data file not found")
            console.print("[yellow]Country data file not found[/yellow]")


# Convenience functions for quick access
def load_faostat_commodity(
    commodity: str, faostat_dir: Optional[Path] = None
) -> FAOSTATManager:
    """
    Quick function to load a single FAOSTAT commodity.

    Args:
        commodity: Name of the commodity to load
        faostat_dir: Optional path to FAOSTAT data directory

    Returns:
        FAOSTATManager instance with the commodity loaded
    """
    manager = FAOSTATManager(faostat_dir=faostat_dir)
    manager.load_commodity(commodity)
    return manager


def load_faostat_commodities(
    commodities: List[str], faostat_dir: Optional[Path] = None
) -> FAOSTATManager:
    """
    Quick function to load multiple FAOSTAT commodities.

    Args:
        commodities: List of commodity names to load
        faostat_dir: Optional path to FAOSTAT data directory

    Returns:
        FAOSTATManager instance with the commodities loaded
    """
    manager = FAOSTATManager(faostat_dir=faostat_dir)
    manager.load_commodities(commodities)
    return manager


# Example usage
if __name__ == "__main__":
    console.print("[bold]Testing FAOSTAT Manager[/bold]")

    # Initialize manager
    faostat = FAOSTATManager()

    # List available commodities
    console.print("\n[bold]Available commodities (first 10):[/bold]")
    faostat.list_commodities(limit=10)

    # Load a commodity
    if faostat.available_items:
        commodity = faostat.available_items[0]
        console.print(f"\n[bold]Loading {commodity} data:[/bold]")
        faostat.load_commodity(commodity)

        # Show summary
        console.print("\n[bold]Commodity summary:[/bold]")
        faostat.commodity_summary(commodity)

    # Load country data
    console.print("\n[bold]Loading country data:[/bold]")
    faostat.load_country_data()

    console.print("\n[bold green]FAOSTAT Manager testing completed![/bold green]")
