# VisiData MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that provides access to [VisiData](https://visidata.org) functionality with enhanced data visualization and analysis capabilities.

## 🚀 Features

### 📊 **Data Visualization**
- **`create_correlation_heatmap`** - Generate correlation matrices with beautiful heatmap visualizations
- **`create_distribution_plots`** - Create statistical distribution plots (histogram, box, violin, kde)
- **`create_graph`** - Custom graphs (scatter, line, bar, histogram) with categorical grouping support

### 🧠 **Advanced Skills Analysis**
- **`parse_skills_column`** - Parse comma-separated skills into individual skills with one-hot encoding
- **`analyze_skills_by_location`** - Comprehensive skills frequency and distribution analysis by location
- **`create_skills_location_heatmap`** - Visual heatmap showing skills distribution across locations
- **`analyze_salary_by_location_and_skills`** - Advanced salary statistics by location and skills combination

### 🔧 **Core Data Tools**
- **`load_data`** - Load and inspect data files from various formats
- **`get_data_sample`** - Get a preview of your data with configurable row count
- **`analyze_data`** - Perform comprehensive data analysis with column types and statistics
- **`convert_data`** - Convert between different data formats (CSV ↔ JSON ↔ Excel, etc.)
- **`filter_data`** - Filter data based on conditions (equals, contains, greater/less than)
- **`get_column_stats`** - Get detailed statistics for specific columns
- **`sort_data`** - Sort data by any column in ascending or descending order

## 📦 Installation

### 🚀 Quick Install (Recommended)

```bash
npm install -g @moeloubani/visidata-mcp@beta
```

**Prerequisites**: Python 3.10+ (the installer will check and guide you if needed)

### Alternative: Python Install

```bash
pip install visidata-mcp
```

### Development Install

```bash
git clone https://github.com/moeloubani/visidata-mcp.git
cd visidata-mcp
pip install -e .
```

## ⚙️ Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "visidata": {
      "command": "visidata-mcp"
    }
  }
}
```

### Cursor AI

Create `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "visidata": {
      "command": "visidata-mcp"
    }
  }
}
```

**Restart your AI application** after configuration changes.

## 🎯 Example Usage

### Data Visualization

```python
# Create a correlation heatmap
create_correlation_heatmap("sales_data.csv", "correlation_heatmap.png")

# Generate distribution plots for all numeric columns
create_distribution_plots("sales_data.csv", "distributions.png", plot_type="histogram")

# Create a scatter plot with categorical grouping
create_graph("sales_data.csv", "price", "sales", "scatter_plot.png", 
            graph_type="scatter", category_column="region")
```

### Skills Analysis

```python
# Parse comma-separated skills into individual columns
parse_skills_column("jobs.csv", "required_skills", "skills_parsed.csv")

# Analyze skills distribution by location
analyze_skills_by_location("jobs.csv", "required_skills", "location", "skills_analysis.json")

# Create skills-location heatmap
create_skills_location_heatmap("jobs.csv", "required_skills", "location", "skills_heatmap.png")

# Comprehensive salary analysis
analyze_salary_by_location_and_skills("jobs.csv", "salary", "location", "required_skills", "salary_analysis.xlsx")
```

### Basic Data Operations

```python
# Load and analyze data
load_data("data.csv")
get_data_sample("data.csv", 10)
analyze_data("data.csv")

# Transform data
convert_data("data.csv", "data.json")
filter_data("data.csv", "revenue", "greater_than", "1000", "high_revenue.csv")
sort_data("data.csv", "date", False, "sorted_data.csv")
```

## 📊 Supported Data Formats

- **Spreadsheets**: CSV, TSV, Excel (XLSX/XLS)
- **Structured Data**: JSON, JSONL, XML, YAML
- **Databases**: SQLite
- **Scientific**: HDF5, Parquet, Arrow
- **Archives**: ZIP, TAR, GZ, BZ2, XZ
- **Web**: HTML tables

## 🔧 Troubleshooting

### Common Issues

**"No module named 'matplotlib'"**
- Make sure you're using the correct MCP server path
- For local development: `/path/to/visidata-mcp/venv/bin/visidata-mcp`
- Restart your AI application after configuration changes

**"0 tools available"**
- Verify the MCP server path in your configuration
- Check that Python 3.10+ is installed
- Restart your AI application completely

### Verification

Test your installation:
```bash
# Check if server starts
visidata-mcp

# Test with Python
python -c "from visidata_mcp.server import main; print('✅ Server ready')"
```

## 🎨 Key Features

- ✅ **Complete visualization support** with matplotlib, seaborn, and scipy
- ✅ **Advanced skills analysis** for job market and HR data
- ✅ **Skills-location correlation** analysis and visualization
- ✅ **Salary analysis** by location and skills combination
- ✅ **Enhanced error handling** with dependency validation
- ✅ **Publication-ready visualizations** (300 DPI PNG output)

## 📈 Use Cases

### Job Market Analysis
- Skills demand analysis by geographic location
- Salary benchmarking across locations and skill sets
- Market trend visualization with correlation analysis

### Data Science Workflows
- Complete statistical analysis pipeline
- Publication-ready visualizations
- Advanced text processing for categorical data

### Business Intelligence
- Location-based performance analysis
- Skills gap identification
- Compensation analysis and benchmarking

## 🛠 Development

```bash
# Install for development
git clone https://github.com/moeloubani/visidata-mcp.git
cd visidata-mcp
pip install -e .

# Build package
python -m build

# Run tests
python -c "from visidata_mcp.server import main; print('✅ Ready')"
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Links

- [VisiData Website](https://visidata.org)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [GitHub Repository](https://github.com/moeloubani/visidata-mcp) 