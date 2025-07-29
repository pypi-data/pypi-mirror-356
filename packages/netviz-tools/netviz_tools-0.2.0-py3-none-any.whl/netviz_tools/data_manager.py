"""
Network Data Manager

This module provides a class `DataManager` that handles preparation of data for NetworkX graphs.
It offers functionality for loading, saving, cleaning, and converting network data to NetworkX objects.

Core features:
    - Data loading from multiple sources (CSV, JSON, Excel, pandas DataFrames, NetworkX graphs)
    - Data transformation and cleaning
    - Automatic detection of node/edge properties
    - Conversion to/from NetworkX graph objects
    - Filtering by year, node type, edge type, etc.
    - Data validation and error handling
    - Export to various formats
"""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import networkx as nx
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from rich.console import Console
from rich.table import Table

# -- Constants -----------------------------------------------------------------
PACKAGE_DIR = Path(__file__).parent
DATA_DIR = PACKAGE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR = PACKAGE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "data_manager.log"
if not LOG_FILE.exists():
    LOG_FILE.touch()

# -- Logger Setup --------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Only add handlers if they don't exist yet
if not logger.handlers:
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Initialize the console for rich output
console = Console()


# -- Data Manager Class --------------------------------------------------------
class DataManager(BaseModel):
    """
    A comprehensive data manager for network graph data.

    This class provides functionality for loading, transforming, and validating network data
    for use with NetworkX. It supports various data sources including CSV, JSON, Excel files,
    pandas DataFrames, and NetworkX graph objects.

    Attributes:
        nodes (pd.DataFrame): DataFrame containing node data.
        edges (pd.DataFrame): DataFrame containing edge data.
        src_col (str): Column name for edge source nodes.
        tgt_col (str): Column name for edge target nodes.
        weight_col (Optional[str]): Column name for edge weights.
        year_col (Optional[str]): Column name for year data.
        label_col (Optional[str]): Column name for node labels.
        has_year (bool): Whether year data is available.
        available_years (List[int]): List of available years in the data.
        node_types (List[str]): List of detected node types.
        edge_types (List[str]): List of detected edge types.
        data_dir (Path): Directory for data storage.
        nodes_path (Optional[Path]): Path to nodes file.
        edges_path (Optional[Path]): Path to edges file.
    """

    # Data storage
    nodes: pd.DataFrame = Field(
        default_factory=pd.DataFrame, description="DataFrame containing node data."
    )
    edges: pd.DataFrame = Field(
        default_factory=pd.DataFrame, description="DataFrame containing edge data."
    )

    # Column mappings
    src_col: str = Field("source", description="Column name for edge sources.")
    tgt_col: str = Field("target", description="Column name for edge targets.")
    weight_col: Optional[str] = Field(None, description="Column name for edge weights.")
    year_col: Optional[str] = Field(
        None, description="Column name for years; auto-detected."
    )
    label_col: Optional[str] = Field(None, description="Column name for node labels.")

    # Derived metadata
    has_year: bool = Field(False, description="Whether year data is available.")
    available_years: List[int] = Field(
        default_factory=list, description="Available years in the data."
    )
    node_types: List[str] = Field(
        default_factory=list, description="List of node types."
    )
    edge_types: List[str] = Field(
        default_factory=list, description="List of edge types."
    )

    # File paths
    data_dir: Path = Field(default=DATA_DIR, description="Directory for data storage.")
    nodes_path: Optional[Union[str, Path]] = Field(
        None, description="Path to nodes file."
    )
    edges_path: Optional[Union[str, Path]] = Field(
        None, description="Path to edges file."
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(
        self,
        *,
        edges_path: Optional[Union[str, Path]] = None,
        nodes_path: Optional[Union[str, Path]] = None,
        src_col: str = "source",
        tgt_col: str = "target",
        weight_col: Optional[str] = None,
        year_col: Optional[str] = None,
        label_col: Optional[str] = None,
        data_dir: Path = DATA_DIR,
        edges: Optional[Union[pd.DataFrame, nx.Graph]] = None,
        nodes: Optional[pd.DataFrame] = None,
    ):
        """
        Initialize DataManager with optional file paths, column mappings, or data.

        Args:
            edges_path: Path to edges file (CSV, JSON, Excel)
            nodes_path: Path to nodes file (CSV, JSON, Excel)
            src_col: Column name for edge sources
            tgt_col: Column name for edge targets
            weight_col: Column name for edge weights
            year_col: Column name for years (auto-detected if None)
            label_col: Column name for node labels
            data_dir: Directory for data storage
            edges: Edge data as DataFrame or NetworkX graph
            nodes: Node data as DataFrame
        """
        # Handle NetworkX graph input
        if edges is not None and isinstance(edges, nx.Graph):
            # Convert NetworkX graph to DataFrames
            edges_df = nx.to_pandas_edgelist(edges)

            # Extract node attributes if present
            nodes_data = []
            for node, attrs in edges.nodes(data=True):
                node_data = {"id": node}
                node_data.update(attrs)
                nodes_data.append(node_data)

            nodes_df = pd.DataFrame(nodes_data) if nodes_data else pd.DataFrame()

            edges = edges_df
            nodes = nodes_df

            # Set default column names based on nx conversion
            if src_col == "source" and "source" not in edges.columns:
                src_col = "source"
            if tgt_col == "target" and "target" not in edges.columns:
                tgt_col = "target"

        super().__init__(
            edges_path=edges_path,
            nodes_path=nodes_path,
            src_col=src_col,
            tgt_col=tgt_col,
            weight_col=weight_col,
            year_col=year_col,
            label_col=label_col,
            data_dir=data_dir,
            edges=edges if edges is not None else pd.DataFrame(),
            nodes=nodes if nodes is not None else pd.DataFrame(),
        )

    @model_validator(mode="before")
    @classmethod
    def _load_paths(cls, values):
        """
        Load DataFrames from file paths if provided.

        This validator runs before initialization and loads data from file paths
        if they are provided.
        """
        # Coerce edges_path/nodes_path into DataFrames if provided
        for path_field, df_field in (("edges_path", "edges"), ("nodes_path", "nodes")):
            p = values.get(path_field)
            if isinstance(p, (str, Path)):
                path = Path(p)
                if not path.exists():
                    raise FileNotFoundError(f"File not found: {path}")

                suffix = path.suffix.lower()
                if suffix == ".csv":
                    df = pd.read_csv(path)
                elif suffix == ".json":
                    try:
                        # Try reading line-delimited JSON first
                        df = pd.read_json(path, orient="records", lines=True)
                    except (ValueError, json.JSONDecodeError):
                        # Fall back to standard JSON format
                        df = pd.read_json(path)
                elif suffix in (".xls", ".xlsx"):
                    df = pd.read_excel(path)
                else:
                    raise ValueError(f"Unsupported file format: {suffix}")

                values[df_field] = df

        return values

    @field_validator("edges")
    @classmethod
    def _validate_edges(cls, df, info):
        """
        Validate edge data to ensure required columns are present.
        """
        if df.empty:
            return df

        required = [info.data.get("src_col"), info.data.get("tgt_col")]
        # Only check for required columns that are specified (not None)
        missing = [c for c in required if c and c not in df.columns]
        if missing:
            raise KeyError(f"Edges missing required columns: {missing}")

        return df

    @model_validator(mode="after")
    def _setup(self):
        """
        Set up derived attributes after initialization.

        This validator runs after initialization and sets up derived attributes
        like column detection, year detection, and node derivation.
        """
        # Normalize and derive if edges loaded
        if not self.edges.empty:
            self._normalize_column_names()
            self._detect_years()
            self._detect_types()
            self._derive_nodes_if_needed()

        logger.info(
            "DataManager ready: %d nodes, %d edges", len(self.nodes), len(self.edges)
        )
        return self

    def load(self) -> None:
        """
        Load data from provided paths.

        This method loads data from the paths provided during initialization.
        """
        if self.edges_path:
            path = Path(self.edges_path)
            suffix = path.suffix.lower()
            if suffix == ".csv":
                self.edges = pd.read_csv(path)
            elif suffix == ".json":
                try:
                    self.edges = pd.read_json(path, orient="records", lines=True)
                except (ValueError, json.JSONDecodeError):
                    self.edges = pd.read_json(path)
            elif suffix in (".xls", ".xlsx"):
                self.edges = pd.read_excel(path)
            else:
                raise ValueError(f"Unsupported file format: {suffix}")

        if self.nodes_path:
            path = Path(self.nodes_path)
            suffix = path.suffix.lower()
            if suffix == ".csv":
                self.nodes = pd.read_csv(path)
            elif suffix == ".json":
                try:
                    self.nodes = pd.read_json(path, orient="records", lines=True)
                except (ValueError, json.JSONDecodeError):
                    self.nodes = pd.read_json(path)
            elif suffix in (".xls", ".xlsx"):
                self.nodes = pd.read_excel(path)
            else:
                raise ValueError(f"Unsupported file format: {suffix}")

        # Re-run setup steps
        self._normalize_column_names()
        self._detect_years()
        self._detect_types()
        self._derive_nodes_if_needed()
        logger.info("Loaded data: %d nodes, %d edges", len(self.nodes), len(self.edges))

    def load_example_data(self) -> None:
        """
        Load built-in example data from data_dir/example_data.

        This method loads example data from the data directory and sets up
        default column mappings.
        """
        example_dir = self.data_dir / "example_data"
        if not example_dir.exists():
            raise FileNotFoundError(f"Example data not found: {example_dir}")

        # Load example data
        nodes_path = example_dir / "nodes.csv"
        edges_path = example_dir / "edges.csv"

        if not nodes_path.exists() or not edges_path.exists():
            logger.error(
                f"Example data files do not exist. Expected at {nodes_path} and {edges_path}."
            )
            raise FileNotFoundError("Example data files do not exist.")

        self.edges = pd.read_csv(edges_path)
        self.nodes = pd.read_csv(nodes_path)

        # Set default column names based on example data
        self.src_col = "o_name"  # in edges
        self.tgt_col = "d_name"  # in edges
        self.weight_col = "weight"  # in edges
        self.label_col = "country"  # in nodes

        # Normalize and derive attributes
        self._normalize_column_names()
        self._detect_years()
        self._detect_types()
        logger.info(
            "Loaded example data: %d nodes, %d edges", len(self.nodes), len(self.edges)
        )

    def _normalize_column_names(self) -> None:
        """
        Normalize column names by converting to lowercase and replacing spaces with underscores.
        """

        def mapper(c):
            return c.strip().lower().replace(" ", "_")

        if not self.edges.empty:
            self.edges.columns = [mapper(c) for c in self.edges.columns]

        if not self.nodes.empty:
            self.nodes.columns = [mapper(c) for c in self.nodes.columns]

    def _detect_years(self) -> None:
        """
        Detect and extract year information from the data.

        This method looks for year columns in the data and extracts available years.
        """
        if self.edges.empty:
            return

        cols = list(self.edges.columns)
        col = None

        # Check if year_col is already set and exists
        if self.year_col in cols:
            col = self.year_col
        # Check for 'year' column (case insensitive)
        elif "year" in map(str.lower, cols):
            col = next(c for c in cols if c.lower() == "year")
        # Look for columns that might contain year information
        else:
            year_columns = [
                c for c in cols if re.search(r"\byear\b|date|time", c, re.IGNORECASE)
            ]
            if year_columns:
                col = year_columns[0]

        if col:
            self.year_col = col
            self.has_year = True
            vals = self.edges[col].dropna()
            try:
                yrs = vals.astype(int)
                self.available_years = sorted(yrs.unique().tolist())
                logger.info(
                    "Detected year column '%s' with %d years",
                    col,
                    len(self.available_years),
                )
            except (ValueError, TypeError):
                # If conversion to int fails, try to extract years from date strings
                logger.warning(
                    "Year column '%s' contains non-integer values, attempting date parsing",
                    col,
                )
                try:
                    # Try to parse as datetime and extract year
                    dates = pd.to_datetime(vals)
                    self.available_years = sorted(dates.dt.year.unique().tolist())
                    logger.info(
                        "Extracted %d years from date column '%s'",
                        len(self.available_years),
                        col,
                    )
                except (ValueError, TypeError):
                    logger.warning("Failed to extract years from column '%s'", col)
                    self.has_year = False
        else:
            self.has_year = False

    def _detect_types(self) -> None:
        """
        Detect node and edge types from the data.

        This method looks for type columns in the data and extracts available types.
        """
        # Detect node types
        if not self.nodes.empty and "type" in self.nodes.columns:
            self.node_types = self.nodes["type"].dropna().unique().tolist()
            logger.info("Detected %d node types", len(self.node_types))

        # Detect edge types
        if not self.edges.empty and "type" in self.edges.columns:
            self.edge_types = self.edges["type"].dropna().unique().tolist()
            logger.info("Detected %d edge types", len(self.edge_types))

    def _derive_nodes_if_needed(self) -> None:
        """
        Derive node data from edge data if node data is not provided.

        This method extracts unique node IDs from edge source and target columns
        and creates a nodes DataFrame if one doesn't exist.
        """
        if self.nodes.empty and not self.edges.empty:
            # Extract unique node IDs from edges
            ids = pd.Series(
                pd.concat([self.edges[self.src_col], self.edges[self.tgt_col]])
                .dropna()
                .unique(),
                name="id",
            )
            self.nodes = pd.DataFrame(ids)
            logger.info("Derived %d unique nodes from edges", len(self.nodes))

    def clean_data(self) -> None:
        """
        Clean the data by removing duplicates, handling missing values, and ensuring consistent formatting.
        """
        logger.info("Cleaning data.")

        # Handle edges
        if not self.edges.empty:
            # Remove duplicates
            orig_len = len(self.edges)
            self.edges.drop_duplicates(inplace=True)
            logger.info(f"Removed {orig_len - len(self.edges)} duplicate edges")

            # Handle missing values in required columns
            self.edges.dropna(subset=[self.src_col, self.tgt_col], inplace=True)

            # If weight column exists, fill NaN with 1.0
            if self.weight_col and self.weight_col in self.edges.columns:
                self.edges[self.weight_col].fillna(1.0, inplace=True)

        # Handle nodes
        if not self.nodes.empty:
            # Remove duplicates
            orig_len = len(self.nodes)
            self.nodes.drop_duplicates(inplace=True)
            logger.info(f"Removed {orig_len - len(self.nodes)} duplicate nodes")

        logger.info("Data cleaning completed.")

    def save_data(
        self, nodes_name: str = "nodes", edges_name: str = "edges", format: str = "csv"
    ) -> None:
        """
        Save data to specified file format.

        Args:
            nodes_name: Base name for the nodes file
            edges_name: Base name for the edges file
            format: File format ('csv', 'json', or 'xlsx')
        """
        logger.info(f"Saving data to {self.data_dir} in {format} format.")

        # Create data directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)

        if format == "csv":
            self.nodes.to_csv(self.data_dir / f"{nodes_name}.csv", index=False)
            self.edges.to_csv(self.data_dir / f"{edges_name}.csv", index=False)
        elif format == "json":
            self.nodes.to_json(
                self.data_dir / f"{nodes_name}.json", orient="records", lines=True
            )
            self.edges.to_json(
                self.data_dir / f"{edges_name}.json", orient="records", lines=True
            )
        elif format == "xlsx":
            with pd.ExcelWriter(self.data_dir / f"{nodes_name}.xlsx") as writer:
                self.nodes.to_excel(writer, sheet_name="nodes", index=False)
                self.edges.to_excel(writer, sheet_name="edges", index=False)
        else:
            logger.error(f"Unsupported file format: {format}")
            raise ValueError(f"Unsupported file format: {format}")

        logger.info("Data saved successfully.")

    def filter_by_year(self, year: int) -> "DataManager":
        """
        Filter data by year and return a new DataManager instance.

        Args:
            year: Year to filter by

        Returns:
            New DataManager instance with filtered data
        """
        if not self.has_year:
            logger.warning("No year column detected, cannot filter by year")
            return self

        if year not in self.available_years:
            logger.warning(
                f"Year {year} not in available years: {self.available_years}"
            )
            return self

        # Filter edges by year
        filtered_edges = self.edges[self.edges[self.year_col] == year].copy()

        # Create new DataManager with filtered data
        new_manager = DataManager(
            src_col=self.src_col,
            tgt_col=self.tgt_col,
            weight_col=self.weight_col,
            year_col=self.year_col,
            label_col=self.label_col,
            data_dir=self.data_dir,
            edges=filtered_edges,
        )

        # Derive nodes from filtered edges
        new_manager._derive_nodes_if_needed()

        logger.info(
            f"Filtered data by year {year}: {len(new_manager.edges)} edges, {len(new_manager.nodes)} nodes"
        )
        return new_manager

    def filter_by_type(
        self, node_type: Optional[str] = None, edge_type: Optional[str] = None
    ) -> "DataManager":
        """
        Filter data by node and/or edge type and return a new DataManager instance.

        Args:
            node_type: Node type to filter by
            edge_type: Edge type to filter by

        Returns:
            New DataManager instance with filtered data
        """
        filtered_nodes = self.nodes.copy()
        filtered_edges = self.edges.copy()

        # Filter nodes by type if specified
        if node_type and "type" in self.nodes.columns:
            if node_type not in self.node_types:
                logger.warning(
                    f"Node type {node_type} not in available types: {self.node_types}"
                )
            else:
                filtered_nodes = filtered_nodes[filtered_nodes["type"] == node_type]

        # Filter edges by type if specified
        if edge_type and "type" in self.edges.columns:
            if edge_type not in self.edge_types:
                logger.warning(
                    f"Edge type {edge_type} not in available types: {self.edge_types}"
                )
            else:
                filtered_edges = filtered_edges[filtered_edges["type"] == edge_type]

        # Create new DataManager with filtered data
        new_manager = DataManager(
            src_col=self.src_col,
            tgt_col=self.tgt_col,
            weight_col=self.weight_col,
            year_col=self.year_col,
            label_col=self.label_col,
            data_dir=self.data_dir,
            nodes=filtered_nodes,
            edges=filtered_edges,
        )

        logger.info(
            f"Filtered data by types: {len(new_manager.edges)} edges, {len(new_manager.nodes)} nodes"
        )
        return new_manager

    def to_networkx(
        self,
        directed: bool = True,
        weight_attr: Optional[str] = None,
        node_id_col: Optional[str] = None,
        filter_year: Optional[int] = None,
    ) -> nx.Graph:
        """
        Convert data to NetworkX graph.

        Args:
            directed: Whether to create a directed graph
            weight_attr: Name of edge attribute to use as weight (defaults to weight_col)
            node_id_col: Column to use as unique node identifier (defaults to 'cc' if available, otherwise 'id')
            filter_year: Optional year to filter the data by before creating the graph

        Returns:
            NetworkX graph
        """
        # Choose graph type
        G = nx.DiGraph() if directed else nx.Graph()

        # Filter edges by year if specified
        edges_to_use = self.edges
        if (
            filter_year is not None
            and self.has_year
            and filter_year in self.available_years
        ):
            edges_to_use = self.edges[self.edges[self.year_col] == filter_year]
            logger.info(
                f"Filtered edges by year {filter_year}: {len(edges_to_use)} edges"
            )

        # Get all unique nodes from edges
        all_sources = set(edges_to_use[self.src_col].dropna().unique())
        all_targets = set(edges_to_use[self.tgt_col].dropna().unique())
        all_nodes = all_sources.union(all_targets)
        logger.info(f"Found {len(all_nodes)} unique entities in edge data")

        # Determine node ID column
        if not self.nodes.empty:
            # If a specific node ID column is provided, use it
            if node_id_col and node_id_col in self.nodes.columns:
                id_col = node_id_col
            # Otherwise, prefer 'cc' for country code if available
            elif "cc" in self.nodes.columns:
                id_col = "cc"
            # If 'id' column exists, use it as node identifier
            elif "id" in self.nodes.columns:
                id_col = "id"
            # Otherwise use the first column as node identifier
            else:
                id_col = self.nodes.columns[0]
            # Get the country/node name column (to match with edge data)
            name_col = (
                self.label_col
                if self.label_col and self.label_col in self.nodes.columns
                else "country"
            )

            # Create a mapping of country name to ID (for linking edge data to node attributes)
            name_to_id = {}
            # Initialize nodes_to_use outside the if block to ensure it's always defined
            nodes_to_use = self.nodes
            if name_col in self.nodes.columns:
                # Filter nodes by year if specified
                if (
                    filter_year is not None
                    and self.has_year
                    and "year" in self.nodes.columns
                ):
                    nodes_to_use = self.nodes[self.nodes["year"] == filter_year]
                    logger.info(
                        f"Filtered nodes by year {filter_year}: {len(nodes_to_use)} nodes"
                    )

                # Create mapping of country names to their IDs
                for _, row in nodes_to_use.iterrows():
                    if (
                        row[name_col] in all_nodes
                    ):  # Only include nodes that appear in edges
                        name_to_id[row[name_col]] = row[id_col]

            # Create a dict to store the node attributes
            node_attrs = {}

            # Add node attributes from nodes DataFrame when available
            for _, row in nodes_to_use.iterrows():
                if (
                    row[name_col] in all_nodes
                ):  # Only include nodes that appear in edges
                    node_id = row[id_col]
                    # Create a copy of the row data excluding the ID column
                    attrs = row.drop(id_col).to_dict()
                    node_attrs[node_id] = attrs

        # Add all nodes to graph (including those without attributes)
        for node_name in all_nodes:
            # If we have node attributes, use them
            if not self.nodes.empty and node_name in name_to_id:
                node_id = name_to_id[node_name]
                G.add_node(node_id, name=node_name, **node_attrs.get(node_id, {}))
            else:
                # This handles countries that exist in edge data but not in node data
                # (historical entities like USSR, Yugoslavia, etc.)
                # or when filtering by a year that has no node data
                # We add them with minimal attributes (just their name)
                G.add_node(node_name, name=node_name, missing_from_nodes=True)

        # Add edges with attributes
        if not edges_to_use.empty:
            weight_col = weight_attr or self.weight_col

            for _, row in edges_to_use.iterrows():
                source = row[self.src_col]
                target = row[self.tgt_col]

                # Skip edges with missing source or target
                if pd.isna(source) or pd.isna(target):
                    continue

                # Map source/target to node IDs if available
                source_id = (
                    name_to_id.get(source, source) if not self.nodes.empty else source
                )
                target_id = (
                    name_to_id.get(target, target) if not self.nodes.empty else target
                )

                # Extract edge attributes excluding source and target
                attrs = {
                    col: row[col]
                    for col in edges_to_use.columns
                    if col not in [self.src_col, self.tgt_col]
                }

                # If weight_col is specified and exists, use it as 'weight'
                if weight_col and weight_col in edges_to_use.columns:
                    attrs["weight"] = row[weight_col]

                G.add_edge(source_id, target_id, **attrs)

        logger.info(
            f"Created NetworkX graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges"
        )
        return G

    def from_networkx(self, G: nx.Graph) -> None:
        """
        Load data from NetworkX graph.

        Args:
            G: NetworkX graph
        """
        # Extract edges with attributes
        self.edges = nx.to_pandas_edgelist(G)

        # Set source and target column names
        self.src_col = "source"
        self.tgt_col = "target"

        # Check for weight column
        if "weight" in self.edges.columns:
            self.weight_col = "weight"

        # Extract nodes with attributes
        nodes_data = []
        for node, attrs in G.nodes(data=True):
            node_data = {"id": node}
            node_data.update(attrs)
            nodes_data.append(node_data)

        self.nodes = pd.DataFrame(nodes_data)

        # Run setup
        self._normalize_column_names()
        self._detect_years()
        self._detect_types()

        logger.info(
            f"Loaded data from NetworkX graph: {len(self.nodes)} nodes, {len(self.edges)} edges"
        )

    def data_stats(self) -> None:
        """
        Print descriptive statistics for the loaded data.
        """
        logger.info("Printing data statistics.")

        if self.nodes.empty:
            console.print("[bold red]No node data available.[/]")
        else:
            console.print("[bold]Node Statistics:[/]")
            console.print(self.nodes.describe().to_string())

        if self.edges.empty:
            console.print("[bold red]No edge data available.[/]")
        else:
            console.print("\n[bold]Edge Statistics:[/]")
            console.print(self.edges.describe().to_string())

    def data_summary(self) -> None:
        """
        Print a summary of the loaded data.
        """
        logger.info("Printing data summary.")

        # Create a table for node information
        node_table = Table(title="Node Information")
        node_table.add_column("Property", style="cyan")
        node_table.add_column("Value", style="green")

        node_table.add_row("Number of Nodes", str(len(self.nodes)))
        if not self.nodes.empty:
            node_table.add_row("Node Columns", ", ".join(self.nodes.columns))
        if self.node_types:
            node_table.add_row("Node Types", ", ".join(self.node_types))

        # Create a table for edge information
        edge_table = Table(title="Edge Information")
        edge_table.add_column("Property", style="cyan")
        edge_table.add_column("Value", style="green")

        edge_table.add_row("Number of Edges", str(len(self.edges)))
        if not self.edges.empty:
            edge_table.add_row("Edge Columns", ", ".join(self.edges.columns))
            edge_table.add_row("Source Column", self.src_col)
            edge_table.add_row("Target Column", self.tgt_col)
            if self.weight_col:
                edge_table.add_row("Weight Column", self.weight_col)
        if self.edge_types:
            edge_table.add_row("Edge Types", ", ".join(self.edge_types))

        # Create a table for year information if available
        if self.has_year:
            year_table = Table(title="Time Information")
            year_table.add_column("Property", style="cyan")
            year_table.add_column("Value", style="green")

            year_table.add_row("Year Column", self.year_col)
            year_table.add_row(
                "Available Years", ", ".join(map(str, self.available_years))
            )

            console.print(node_table)
            console.print(edge_table)
            console.print(year_table)
        else:
            console.print(node_table)
            console.print(edge_table)

        logger.info("Data summary printed.")

    def network_stats(self) -> Dict[str, Any]:
        """
        Calculate network statistics using NetworkX.

        Returns:
            Dictionary of network statistics
        """
        logger.info("Calculating network statistics.")

        G = self.to_networkx()
        stats = {}

        # Basic statistics
        stats["num_nodes"] = G.number_of_nodes()
        stats["num_edges"] = G.number_of_edges()
        stats["density"] = nx.density(G)

        # Try to calculate more complex statistics (may fail for large or disconnected graphs)
        try:
            stats["avg_clustering"] = nx.average_clustering(G)
        except nx.NetworkXError:
            stats["avg_clustering"] = "N/A"

        try:
            stats["avg_shortest_path"] = nx.average_shortest_path_length(G)
        except nx.NetworkXError:
            stats["avg_shortest_path"] = "N/A"

        # Degree statistics
        degrees = [d for _, d in G.degree()]
        stats["min_degree"] = min(degrees) if degrees else 0
        stats["max_degree"] = max(degrees) if degrees else 0
        stats["avg_degree"] = sum(degrees) / len(degrees) if degrees else 0

        # Print statistics
        console.print("[bold]Network Statistics:[/]")
        for key, value in stats.items():
            console.print(f"{key}: {value}")

        logger.info("Network statistics calculated.")
        return stats

    @property
    def output(self) -> dict:
        """
        Return a dictionary of the current state of the DataManager.

        Returns:
            Dictionary of DataManager state
        """
        return {
            "edges": self.edges,
            "nodes": self.nodes,
            "has_year": self.has_year,
            "available_years": self.available_years,
            "src_col": self.src_col,
            "tgt_col": self.tgt_col,
            "weight_col": self.weight_col,
            "year_col": self.year_col,
            "label_col": self.label_col,
            "node_types": self.node_types,
            "edge_types": self.edge_types,
        }


# Example usage
if __name__ == "__main__":
    logger.info("Testing data manager functionality.")

    # Example 1: Load example data
    console.print("[bold]Example 1: Loading example data[/]")
    dm1 = DataManager()
    dm1.load_example_data()
    dm1.data_summary()

    # Example 2: Filter by year
    if dm1.has_year and dm1.available_years:
        console.print("\n[bold]Example 2: Filtering by year[/]")
        year = dm1.available_years[0]
        dm_filtered = dm1.filter_by_year(year)
        dm_filtered.data_summary()

    # Example 3: Convert to NetworkX
    console.print("\n[bold]Example 3: Converting to NetworkX[/]")
    G = dm1.to_networkx()
    console.print(
        f"Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges"
    )

    # Example 4: Calculate network statistics
    console.print("\n[bold]Example 4: Network statistics[/]")
    dm1.network_stats()

    console.print("\n[bold green]Data manager testing completed successfully![/]")
