# netviz_tools

**A versatile network data visualization and analysis toolkit.**

`netviz_tools` provides:

- **DataManager**: Load, clean, transform, and analyze network data from various sources
- **NetworkManager**: Build NetworkX graphs, compute network metrics, and create interactive visualizations
- **TimeSeries**: Analyze temporal patterns and generate time series plots of network metrics
- **Utilities**: Helper functions and constants for visualization and data export

---

## 📦 Installation

```bash
# From PyPI
pip install netviz_tools

# Or, for local development
git clone https://github.com/tyson-j/netviz_tools.git
cd netviz_tools
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# For Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .[dev]
```

*(The `[dev]` extra pulls in testing tools like `pytest`.)*

---

## 🚀 Quick Start

```python
from netviz_tools import DataManager, NetworkManager

# 1. Load data from CSV files
dm = DataManager(
    nodes_path="path/to/nodes.csv",
    edges_path="path/to/edges.csv"
)

# 2. Clean and prepare the data
dm.clean_data()
dm.data_summary()  # Print summary of the loaded data

# 3. Convert to NetworkX graph
G = dm.to_networkx(directed=True)

# 4. Filter data by year if needed
if dm.has_year:
    year = dm.available_years[0]  # Take the first available year
    filtered_dm = dm.filter_by_year(year)
    G = filtered_dm.to_networkx()

# 5. Analyze network statistics
stats = dm.network_stats()

# 6. Save processed data if needed
dm.save_data(format='csv')

# 7. When NetworkManager is fully implemented:
# network = NetworkManager(G)
# network.plot_interactive(json_path="output/network.json")
```

---

## 📚 Documentation

Detailed documentation and examples are available in the [`docs/`](./docs) folder. Key components:

- **DataManager**: The primary data handling class that loads, cleans, and transforms network data
- **NetworkManager**: For network visualization and metric calculation (coming soon)
- **TimeSeries**: For time-based network analysis (coming soon)

For API documentation, see the [Python module docs](./docs/python/).

## ✨ Features

- **Flexible Data Import**: Load network data from CSV, JSON, Excel files, pandas DataFrames, or NetworkX graphs
- **Data Preprocessing**: Automatic cleaning, normalization, and detection of key attributes
- **Time-Series Support**: Analyze how networks evolve over time with built-in year detection and filtering
- **Graph Conversion**: Seamless conversion between data formats and NetworkX graph objects
- **Network Analysis**: Calculate and visualize network metrics and properties
- **Interactive Visualization**: Generate rich, interactive visualizations (with full implementation of NetworkManager)

---

## 🛠️ Development

1. **Create a virtualenv** (see Installation above).  
2. **Install dev requirements**:  
   ```bash
   pip install -e .[dev]
   ```
3. **Run tests**:  
   ```bash
   pytest
   ```
4. **Build distribution**:  
   ```bash
   python -m build
   ```
5. **Publish**:  
   ```bash
   twine upload dist/*
   ```

---

## 🤝 Contributing (coming soon)

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes
4. Add tests for any new functionality
5. Ensure all tests pass (`pytest`)
6. Open a Pull Request

Please follow the existing code style and include documentation for new features.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

