"""
VisiData MCP Server

This module implements a Model Context Protocol server that provides access to VisiData functionality.
VisiData is a terminal spreadsheet multitool for discovering and arranging tabular data.
"""

import asyncio
import io
import json
import os
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import visidata as vd
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
import warnings

# Try to import visualization packages early to detect missing dependencies
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    VISUALIZATION_AVAILABLE = False
    VISUALIZATION_ERROR = f"Visualization libraries not available: {e}. Please install matplotlib and seaborn."

# Suppress VisiData warnings and output
warnings.filterwarnings("ignore")

# Redirect VisiData's stderr to suppress warnings
class NullWriter:
    def write(self, txt): pass
    def flush(self): pass

# Temporarily redirect stderr during VisiData initialization
original_stderr = sys.stderr
sys.stderr = NullWriter()

try:
    # Initialize VisiData with headless mode
    vd.options.batch = True  # Run in batch mode
    vd.options.header = 1  # Assume first row is header by default
    
    # Try to set confirm_overwrite option if it exists
    try:
        vd.options.confirm_overwrite = False  # Don't ask for confirmations
    except (AttributeError, Exception):
        # Option doesn't exist in this VisiData version, ignore
        pass
        
    # Suppress VisiData's verbose output
    try:
        vd.options.debug = False
        vd.options.verbose = False
    except (AttributeError, Exception):
        pass
        
finally:
    # Restore stderr
    sys.stderr = original_stderr

# Create the MCP server
mcp = FastMCP("VisiData")


@mcp.tool()
def load_data(file_path: str, file_type: Optional[str] = None) -> str:
    """
    Load data from a file using VisiData.
    
    Args:
        file_path: Path to the data file
        file_type: Optional file type hint (csv, json, xlsx, etc.)
    
    Returns:
        String representation of the loaded data structure
    """
    try:
        # Use pandas as a reliable fallback for common formats
        import pandas as pd
        from pathlib import Path
        
        file_extension = Path(file_path).suffix.lower()
        
        # Load with pandas first for reliability
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            # Try CSV as default
            df = pd.read_csv(file_path)
        
        # Get basic information about the dataset
        info = {
            "filename": Path(file_path).name,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns)[:10],  # First 10 columns
            "column_types": [str(df[col].dtype) for col in df.columns[:10]],
            "file_size": Path(file_path).stat().st_size if Path(file_path).exists() else 0
        }
        
        return json.dumps(info, indent=2)
        
    except Exception as e:
        return f"Error loading data: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def get_data_sample(file_path: str, rows: int = 10) -> str:
    """
    Get a sample of data from a file.
    
    Args:
        file_path: Path to the data file
        rows: Number of rows to return (default: 10)
    
    Returns:
        Sample data in JSON format
    """
    try:
        import pandas as pd
        from pathlib import Path
        
        file_extension = Path(file_path).suffix.lower()
        
        # Load with pandas
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        # Get sample rows
        sample_df = df.head(rows)
        
        # Convert to records for JSON serialization
        sample_data = []
        for _, row in sample_df.iterrows():
            row_data = {}
            for col in df.columns:
                value = row[col]
                # Handle pandas/numpy types for JSON serialization
                if pd.isna(value):
                    row_data[col] = None
                elif hasattr(value, 'item'):  # numpy types
                    row_data[col] = value.item()
                else:
                    row_data[col] = str(value) if value is not None else None
            sample_data.append(row_data)
        
        result = {
            "filename": Path(file_path).name,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "sample_rows": len(sample_data),
            "columns": list(df.columns),
            "data": sample_data
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error getting data sample: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def analyze_data(file_path: str) -> str:
    """
    Perform basic analysis on a dataset.
    
    Args:
        file_path: Path to the data file
    
    Returns:
        Analysis results including statistics and data types
    """
    try:
        import pandas as pd
        from pathlib import Path
        
        file_extension = Path(file_path).suffix.lower()
        
        # Load with pandas
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        analysis = {
            "filename": Path(file_path).name,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": []
        }
        
        # Analyze each column
        for col_name in df.columns:
            col_data = df[col_name]
            
            col_info = {
                "name": col_name,
                "type": str(col_data.dtype),
                "null_count": int(col_data.isna().sum()),
                "non_null_count": int(col_data.notna().sum()),
            }
            
            # Get some sample values
            sample_values = []
            valid_values = col_data.dropna().head(5)
            for value in valid_values:
                if hasattr(value, 'item'):  # numpy types
                    sample_values.append(value.item())
                else:
                    sample_values.append(str(value) if value is not None else None)
            
            col_info["sample_values"] = sample_values
            
            # Add basic statistics for numeric columns
            if pd.api.types.is_numeric_dtype(col_data):
                col_info["min"] = float(col_data.min()) if not col_data.empty else None
                col_info["max"] = float(col_data.max()) if not col_data.empty else None
                col_info["mean"] = float(col_data.mean()) if not col_data.empty else None
                col_info["unique_count"] = int(col_data.nunique())
            else:
                col_info["unique_count"] = int(col_data.nunique())
                col_info["most_common"] = list(col_data.value_counts().head(3).index)
            
            analysis["columns"].append(col_info)
        
        return json.dumps(analysis, indent=2)
        
    except Exception as e:
        return f"Error analyzing data: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def convert_data(input_path: str, output_path: str, output_format: Optional[str] = None) -> str:
    """
    Convert data from one format to another using pandas.
    
    Args:
        input_path: Path to the input data file
        output_path: Path for the output file
        output_format: Target format (csv, json, xlsx, etc.)
    
    Returns:
        Success message or error details
    """
    try:
        import pandas as pd
        from pathlib import Path
        
        # Load data with pandas
        input_extension = Path(input_path).suffix.lower()
        
        if input_extension == '.csv':
            df = pd.read_csv(input_path)
        elif input_extension == '.json':
            df = pd.read_json(input_path)
        elif input_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(input_path)
        elif input_extension == '.tsv':
            df = pd.read_csv(input_path, sep='\t')
        else:
            df = pd.read_csv(input_path)
        
        # Determine output format from extension if not specified
        if output_format is None:
            output_format = Path(output_path).suffix.lstrip('.')
        
        # Save in the new format
        if output_format == 'csv':
            df.to_csv(output_path, index=False)
        elif output_format == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif output_format in ['xlsx', 'xls']:
            df.to_excel(output_path, index=False)
        elif output_format == 'tsv':
            df.to_csv(output_path, sep='\t', index=False)
        else:
            # Default to CSV
            df.to_csv(output_path, index=False)
            output_format = 'csv'
        
        result = {
            "input_file": input_path,
            "output_file": output_path,
            "output_format": output_format,
            "rows_converted": len(df),
            "columns_converted": len(df.columns)
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error converting data: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def filter_data(file_path: str, column: str, condition: str, value: str, output_path: Optional[str] = None) -> str:
    """
    Filter data based on a condition.
    
    Args:
        file_path: Path to the data file
        column: Column name to filter on
        condition: Filter condition (equals, contains, greater_than, less_than)
        value: Value to filter by
        output_path: Optional path to save filtered data
    
    Returns:
        Information about the filtered data
    """
    try:
        import pandas as pd
        from pathlib import Path
        
        file_extension = Path(file_path).suffix.lower()
        
        # Load with pandas
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found. Available columns: {list(df.columns)}"
        
        original_rows = len(df)
        
        # Apply filter
        if condition == "equals":
            filtered_df = df[df[column].astype(str) == value]
        elif condition == "contains":
            filtered_df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        elif condition == "greater_than":
            try:
                numeric_value = float(value)
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') > numeric_value]
            except ValueError:
                return f"Error: Cannot convert '{value}' to number for greater_than comparison"
        elif condition == "less_than":
            try:
                numeric_value = float(value)
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') < numeric_value]
            except ValueError:
                return f"Error: Cannot convert '{value}' to number for less_than comparison"
        else:
            return f"Error: Unknown condition '{condition}'. Use: equals, contains, greater_than, less_than"
        
        result = {
            "original_rows": original_rows,
            "filtered_rows": len(filtered_df),
            "filter_applied": f"{column} {condition} {value}"
        }
        
        # If output path is specified, save filtered data
        if output_path:
            output_extension = Path(output_path).suffix.lower()
            if output_extension == '.csv':
                filtered_df.to_csv(output_path, index=False)
            elif output_extension == '.json':
                filtered_df.to_json(output_path, orient='records', indent=2)
            elif output_extension in ['.xlsx', '.xls']:
                filtered_df.to_excel(output_path, index=False)
            else:
                # Default to CSV
                filtered_df.to_csv(output_path, index=False)
            result["saved_to"] = output_path
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error filtering data: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def get_column_stats(file_path: str, column: str) -> str:
    """
    Get statistics for a specific column.
    
    Args:
        file_path: Path to the data file
        column: Column name to analyze
    
    Returns:
        Column statistics in JSON format
    """
    try:
        import pandas as pd
        from pathlib import Path
        
        file_extension = Path(file_path).suffix.lower()
        
        # Load with pandas
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found. Available columns: {list(df.columns)}"
        
        col_data = df[column]
        
        stats = {
            "column": column,
            "type": str(col_data.dtype),
            "total_values": len(col_data),
            "non_null_values": int(col_data.notna().sum()),
            "null_count": int(col_data.isna().sum()),
            "unique_values": int(col_data.nunique())
        }
        
        # Sample values
        sample_values = []
        for value in col_data.dropna().head(10):
            if hasattr(value, 'item'):  # numpy types
                sample_values.append(value.item())
            else:
                sample_values.append(str(value))
        stats["sample_values"] = sample_values
        
        # If numeric, calculate additional stats
        if pd.api.types.is_numeric_dtype(col_data):
            numeric_col = col_data.dropna()
            if not numeric_col.empty:
                stats["min"] = float(numeric_col.min())
                stats["max"] = float(numeric_col.max())
                stats["mean"] = float(numeric_col.mean())
                stats["median"] = float(numeric_col.median())
                stats["std"] = float(numeric_col.std())
                stats["quartiles"] = {
                    "25%": float(numeric_col.quantile(0.25)),
                    "50%": float(numeric_col.quantile(0.50)),
                    "75%": float(numeric_col.quantile(0.75))
                }
        else:
            # For non-numeric, show value counts
            value_counts = col_data.value_counts().head(10)
            stats["most_common"] = []
            for value, count in value_counts.items():
                stats["most_common"].append({
                    "value": str(value),
                    "count": int(count),
                    "percentage": round(count / len(col_data) * 100, 2)
                })
        
        return json.dumps(stats, indent=2)
        
    except Exception as e:
        return f"Error getting column stats: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def sort_data(file_path: str, column: str, descending: bool = False, output_path: Optional[str] = None) -> str:
    """
    Sort data by a specific column.
    
    Args:
        file_path: Path to the data file
        column: Column name to sort by
        descending: Sort in descending order (default: False)
        output_path: Optional path to save sorted data
    
    Returns:
        Information about the sorted data
    """
    try:
        import pandas as pd
        from pathlib import Path
        
        file_extension = Path(file_path).suffix.lower()
        
        # Load with pandas
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found. Available columns: {list(df.columns)}"
        
        # Sort the data
        sorted_df = df.sort_values(by=column, ascending=not descending)
        
        result = {
            "sorted_by": column,
            "descending": descending,
            "total_rows": len(sorted_df)
        }
        
        # If output path is specified, save sorted data
        if output_path:
            output_extension = Path(output_path).suffix.lower()
            if output_extension == '.csv':
                sorted_df.to_csv(output_path, index=False)
            elif output_extension == '.json':
                sorted_df.to_json(output_path, orient='records', indent=2)
            elif output_extension in ['.xlsx', '.xls']:
                sorted_df.to_excel(output_path, index=False)
            else:
                # Default to CSV
                sorted_df.to_csv(output_path, index=False)
            result["saved_to"] = output_path
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error sorting data: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def create_graph(file_path: str, x_column: str, y_column: str, 
                output_path: str, graph_type: str = "scatter", 
                category_column: Optional[str] = None) -> str:
    """
    Create a graph/plot from data using matplotlib/seaborn.
    
    Args:
        file_path: Path to the data file
        x_column: Column name for x-axis (must be numeric)
        y_column: Column name for y-axis (must be numeric) 
        output_path: Path where to save the graph image
        graph_type: Type of graph (scatter, line, bar, histogram)
        category_column: Optional categorical column for grouping/coloring
    
    Returns:
        Information about the created graph
    """
    try:
        if not VISUALIZATION_AVAILABLE:
            return f"Error: {VISUALIZATION_ERROR}"
            
        import pandas as pd
        from pathlib import Path
        
        # Load the data
        file_extension = Path(file_path).suffix.lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        # Validate columns exist
        if x_column not in df.columns:
            return f"Error: Column '{x_column}' not found in data"
        if y_column not in df.columns:
            return f"Error: Column '{y_column}' not found in data"
        if category_column and category_column not in df.columns:
            return f"Error: Category column '{category_column}' not found in data"
        
        # Ensure numeric columns are properly typed
        try:
            df[x_column] = pd.to_numeric(df[x_column], errors='coerce')
            df[y_column] = pd.to_numeric(df[y_column], errors='coerce')
        except:
            return f"Error: Could not convert {x_column} or {y_column} to numeric values"
        
        # Remove rows with NaN values in plotting columns
        plot_columns = [x_column, y_column]
        if category_column:
            plot_columns.append(category_column)
        df_clean = df[plot_columns].dropna()
        
        if len(df_clean) == 0:
            return "Error: No valid data points for plotting after removing NaN values"
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        
        if graph_type == "scatter":
            if category_column:
                sns.scatterplot(data=df_clean, x=x_column, y=y_column, hue=category_column, alpha=0.7)
            else:
                plt.scatter(df_clean[x_column], df_clean[y_column], alpha=0.7)
        elif graph_type == "line":
            if category_column:
                sns.lineplot(data=df_clean, x=x_column, y=y_column, hue=category_column)
            else:
                plt.plot(df_clean[x_column], df_clean[y_column])
        elif graph_type == "bar":
            if category_column:
                # Group by category and take mean of y values for each x value
                grouped = df_clean.groupby([x_column, category_column])[y_column].mean().reset_index()
                sns.barplot(data=grouped, x=x_column, y=y_column, hue=category_column)
            else:
                grouped = df_clean.groupby(x_column)[y_column].mean()
                plt.bar(grouped.index, grouped.values)
        elif graph_type == "histogram":
            if category_column:
                for category in df_clean[category_column].unique():
                    subset = df_clean[df_clean[category_column] == category]
                    plt.hist(subset[y_column], alpha=0.7, label=str(category), bins=20)
                plt.legend()
            else:
                plt.hist(df_clean[y_column], bins=20, alpha=0.7)
            plt.xlabel(y_column)
            plt.ylabel('Frequency')
        else:
            return f"Error: Unsupported graph type '{graph_type}'. Use: scatter, line, bar, histogram"
        
        # Set labels and title
        plt.xlabel(x_column.replace('_', ' ').title())
        plt.ylabel(y_column.replace('_', ' ').title())
        
        title = f"{graph_type.title()} Plot: {y_column} vs {x_column}"
        if category_column:
            title += f" (grouped by {category_column})"
        plt.title(title)
        
        # Add grid for better readability
        plt.grid(True, alpha=0.3)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        result = {
            "graph_created": True,
            "graph_type": graph_type,
            "x_column": x_column,
            "y_column": y_column,
            "category_column": category_column,
            "data_points": len(df_clean),
            "output_file": output_path,
            "file_size": Path(output_path).stat().st_size if Path(output_path).exists() else 0
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error creating graph: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def create_correlation_heatmap(file_path: str, output_path: str, 
                              columns: Optional[List[str]] = None) -> str:
    """
    Create a correlation heatmap from numeric columns in the dataset.
    
    Args:
        file_path: Path to the data file
        output_path: Path where to save the heatmap image
        columns: Optional list of specific columns to include (if None, uses all numeric columns)
    
    Returns:
        Information about the created heatmap
    """
    try:
        if not VISUALIZATION_AVAILABLE:
            return f"Error: {VISUALIZATION_ERROR}"
            
        import pandas as pd
        from pathlib import Path
        
        # Load the data
        file_extension = Path(file_path).suffix.lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        # Select numeric columns
        if columns:
            # Validate specified columns exist
            missing_cols = [col for col in columns if col not in df.columns]
            if missing_cols:
                return f"Error: Columns not found: {missing_cols}"
            numeric_df = df[columns].select_dtypes(include=['number'])
        else:
            numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            return "Error: No numeric columns found for correlation analysis"
        
        # Calculate correlation matrix
        correlation_matrix = numeric_df.corr()
        
        # Create the heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, 
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   fmt='.2f',
                   square=True,
                   linewidths=0.5)
        
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        result = {
            "heatmap_created": True,
            "columns_analyzed": list(correlation_matrix.columns),
            "total_correlations": len(correlation_matrix.columns) ** 2,
            "output_file": output_path,
            "file_size": Path(output_path).stat().st_size if Path(output_path).exists() else 0
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error creating correlation heatmap: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def create_distribution_plots(file_path: str, output_path: str, 
                            columns: Optional[List[str]] = None,
                            plot_type: str = "histogram") -> str:
    """
    Create distribution plots for numeric columns.
    
    Args:
        file_path: Path to the data file
        output_path: Path where to save the distribution plots
        columns: Optional list of specific columns to plot (if None, uses all numeric columns)
        plot_type: Type of distribution plot (histogram, box, violin, kde)
    
    Returns:
        Information about the created distribution plots
    """
    try:
        if not VISUALIZATION_AVAILABLE:
            return f"Error: {VISUALIZATION_ERROR}"
            
        import pandas as pd
        from pathlib import Path
        import math
        
        # Load the data
        file_extension = Path(file_path).suffix.lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        # Select numeric columns
        if columns:
            missing_cols = [col for col in columns if col not in df.columns]
            if missing_cols:
                return f"Error: Columns not found: {missing_cols}"
            numeric_df = df[columns].select_dtypes(include=['number'])
        else:
            numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            return "Error: No numeric columns found for distribution analysis"
        
        # Calculate subplot dimensions
        n_cols = len(numeric_df.columns)
        if n_cols <= 4:
            n_rows, n_plot_cols = 1, n_cols
        else:
            n_plot_cols = 3
            n_rows = math.ceil(n_cols / n_plot_cols)
        
        # Create subplots
        fig, axes = plt.subplots(n_rows, n_plot_cols, figsize=(5*n_plot_cols, 4*n_rows))
        if n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes if n_cols > 1 else [axes]
        else:
            axes = axes.flatten()
        
        # Create distribution plots
        for i, column in enumerate(numeric_df.columns):
            ax = axes[i] if n_cols > 1 else axes[0]
            
            if plot_type == "histogram":
                ax.hist(numeric_df[column].dropna(), bins=20, alpha=0.7, edgecolor='black')
                ax.set_ylabel('Frequency')
            elif plot_type == "box":
                ax.boxplot(numeric_df[column].dropna())
                ax.set_ylabel('Value')
            elif plot_type == "violin":
                sns.violinplot(y=numeric_df[column].dropna(), ax=ax)
            elif plot_type == "kde":
                sns.kdeplot(data=numeric_df[column].dropna(), ax=ax)
                ax.set_ylabel('Density')
            else:
                return f"Error: Unsupported plot type '{plot_type}'. Use: histogram, box, violin, kde"
            
            ax.set_title(f'{plot_type.title()} of {column}')
            ax.set_xlabel(column.replace('_', ' ').title())
            ax.grid(True, alpha=0.3)
        
        # Hide empty subplots
        for i in range(n_cols, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        result = {
            "distribution_plots_created": True,
            "plot_type": plot_type,
            "columns_plotted": list(numeric_df.columns),
            "total_plots": len(numeric_df.columns),
            "output_file": output_path,
            "file_size": Path(output_path).stat().st_size if Path(output_path).exists() else 0
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error creating distribution plots: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def get_supported_formats() -> str:
    """
    Get a list of supported file formats in VisiData.
    
    Returns:
        List of supported formats and their descriptions
    """
    try:
        # VisiData supported formats
        formats = {
            "csv": "Comma-separated values",
            "tsv": "Tab-separated values",
            "json": "JavaScript Object Notation",
            "jsonl": "JSON Lines",
            "xlsx": "Microsoft Excel",
            "xls": "Microsoft Excel (legacy)",
            "sqlite": "SQLite database",
            "html": "HTML tables",
            "xml": "XML files",
            "yaml": "YAML files",
            "hdf5": "HDF5 scientific data format",
            "parquet": "Apache Parquet",
            "arrow": "Apache Arrow",
            "pkl": "Python pickle files",
            "zip": "ZIP archives",
            "tar": "TAR archives",
            "gz": "Gzipped files",
            "bz2": "Bzip2 compressed files",
            "xz": "XZ compressed files"
        }
        
        result = {
            "supported_formats": formats,
            "total_formats": len(formats),
            "note": "VisiData supports many more formats through plugins and loaders"
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error getting supported formats: {str(e)}\n{traceback.format_exc()}"


@mcp.resource("visidata://help")
def get_visidata_help() -> str:
    """Get VisiData help and documentation."""
    help_text = """
# VisiData MCP Server Help

This MCP server provides access to VisiData functionality through the following tools:

## Available Tools:

1. **load_data** - Load and inspect data files
   - Supports multiple formats (CSV, JSON, Excel, etc.)
   - Returns basic information about the dataset

2. **get_data_sample** - Get a preview of your data
   - Returns the first N rows of a dataset
   - Useful for understanding data structure

3. **analyze_data** - Perform basic data analysis
   - Returns column types, sample values, and structure
   - Helps understand your dataset

4. **convert_data** - Convert between data formats
   - Convert CSV to JSON, Excel to CSV, etc.
   - Leverages VisiData's format support

5. **filter_data** - Filter data based on conditions
   - Filter by equals, contains, greater_than, less_than
   - Can save filtered results to a new file

6. **get_column_stats** - Get statistics for a column
   - Returns min/max/mean for numeric columns
   - Returns unique counts for text columns

7. **sort_data** - Sort data by a column
   - Sort ascending or descending
   - Can save sorted results

8. **get_supported_formats** - List supported file formats
   - Shows all formats VisiData can handle

## Usage Examples:

- Load a CSV file: `load_data("/path/to/data.csv")`
- Get 5 rows: `get_data_sample("/path/to/data.csv", 5)`
- Convert CSV to JSON: `convert_data("/path/to/data.csv", "/path/to/output.json")`
- Filter data: `filter_data("/path/to/data.csv", "age", "greater_than", "18")`

## About VisiData:

VisiData is a terminal interface for exploring and arranging tabular data.
It supports numerous data formats and provides powerful data manipulation capabilities.

Visit: https://visidata.org for more information.
"""
    return help_text


@mcp.prompt()
def analyze_dataset_prompt(file_path: str) -> str:
    """
    Generate a comprehensive analysis prompt for a dataset.
    
    Args:
        file_path: Path to the dataset to analyze
    
    Returns:
        A detailed prompt for dataset analysis
    """
    return f"""
Please analyze the dataset at {file_path} using the available VisiData tools.

Follow these steps:
1. First, load the data using `load_data` to understand the basic structure
2. Get a sample of the data using `get_data_sample` to see actual values
3. Perform analysis using `analyze_data` to understand column types and structure
4. For each important column, get statistics using `get_column_stats`

Based on this analysis, provide:
- Summary of the dataset (rows, columns, data types)
- Key insights about the data
- Data quality observations (missing values, outliers, etc.)
- Suggestions for further analysis or data cleaning
- Potential use cases for this dataset

Please be thorough and provide actionable insights.
"""


@mcp.tool()
def parse_skills_column(file_path: str, skills_column: str, output_path: Optional[str] = None) -> str:
    """
    Parse comma-separated skills into individual skills and create one-hot encoding.
    
    Args:
        file_path: Path to the data file
        skills_column: Column name containing comma-separated skills
        output_path: Optional path to save the processed data
    
    Returns:
        Information about the parsed skills data
    """
    try:
        import pandas as pd
        from pathlib import Path
        
        # Load the data
        file_extension = Path(file_path).suffix.lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        if skills_column not in df.columns:
            return f"Error: Column '{skills_column}' not found in data"
        
        # Parse skills and create one-hot encoding
        all_skills = set()
        
        # Extract all unique skills
        for skills_str in df[skills_column].dropna():
            if pd.isna(skills_str):
                continue
            skills = [skill.strip() for skill in str(skills_str).split(',') if skill.strip()]
            all_skills.update(skills)
        
        all_skills = sorted(list(all_skills))
        
        # Create one-hot encoding for each skill
        skills_df = df.copy()
        for skill in all_skills:
            skills_df[f"skill_{skill.replace(' ', '_').replace('-', '_').lower()}"] = 0
        
        # Fill in the one-hot encoding
        for idx, skills_str in enumerate(df[skills_column]):
            if pd.isna(skills_str):
                continue
            skills = [skill.strip() for skill in str(skills_str).split(',') if skill.strip()]
            for skill in skills:
                col_name = f"skill_{skill.replace(' ', '_').replace('-', '_').lower()}"
                if col_name in skills_df.columns:
                    skills_df.loc[idx, col_name] = 1
        
        # Save processed data if output path provided
        if output_path:
            if output_path.endswith('.csv'):
                skills_df.to_csv(output_path, index=False)
            elif output_path.endswith('.json'):
                skills_df.to_json(output_path, orient='records', indent=2)
            elif output_path.endswith(('.xlsx', '.xls')):
                skills_df.to_excel(output_path, index=False)
            else:
                skills_df.to_csv(output_path, index=False)
        
        result = {
            "skills_parsed": True,
            "original_column": skills_column,
            "unique_skills_count": len(all_skills),
            "unique_skills": all_skills[:20],  # First 20 skills for preview
            "rows_processed": len(df),
            "new_columns_added": len(all_skills),
            "output_file": output_path if output_path else None
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error parsing skills: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def analyze_skills_by_location(file_path: str, skills_column: str, location_column: str, 
                              output_path: Optional[str] = None) -> str:
    """
    Analyze skills frequency and distribution by location.
    
    Args:
        file_path: Path to the data file
        skills_column: Column name containing comma-separated skills
        location_column: Column name containing location information
        output_path: Optional path to save the analysis results
    
    Returns:
        Skills analysis by location
    """
    try:
        import pandas as pd
        from pathlib import Path
        from collections import defaultdict, Counter
        
        # Load the data
        file_extension = Path(file_path).suffix.lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        if skills_column not in df.columns:
            return f"Error: Column '{skills_column}' not found in data"
        if location_column not in df.columns:
            return f"Error: Column '{location_column}' not found in data"
        
        # Analyze skills by location
        location_skills = defaultdict(list)
        
        for _, row in df.iterrows():
            location = row[location_column]
            skills_str = row[skills_column]
            
            if pd.isna(location) or pd.isna(skills_str):
                continue
                
            skills = [skill.strip() for skill in str(skills_str).split(',') if skill.strip()]
            location_skills[location].extend(skills)
        
        # Calculate statistics for each location
        analysis_results = []
        for location, skills_list in location_skills.items():
            skill_counts = Counter(skills_list)
            total_skills = len(skills_list)
            unique_skills = len(skill_counts)
            
            # Top 10 most common skills for this location
            top_skills = skill_counts.most_common(10)
            
            analysis_results.append({
                "location": location,
                "total_skill_mentions": total_skills,
                "unique_skills": unique_skills,
                "job_postings": sum(1 for _, row in df.iterrows() 
                                 if row[location_column] == location and not pd.isna(row[skills_column])),
                "top_skills": [{"skill": skill, "count": count, "percentage": round(count/total_skills*100, 2)} 
                              for skill, count in top_skills]
            })
        
        # Sort by total skill mentions
        analysis_results.sort(key=lambda x: x["total_skill_mentions"], reverse=True)
        
        # Save analysis if output path provided
        if output_path:
            analysis_df = pd.DataFrame(analysis_results)
            if output_path.endswith('.csv'):
                analysis_df.to_csv(output_path, index=False)
            elif output_path.endswith('.json'):
                with open(output_path, 'w') as f:
                    json.dump(analysis_results, f, indent=2)
            elif output_path.endswith(('.xlsx', '.xls')):
                analysis_df.to_excel(output_path, index=False)
            else:
                analysis_df.to_csv(output_path, index=False)
        
        result = {
            "analysis_completed": True,
            "locations_analyzed": len(analysis_results),
            "total_locations": len(location_skills),
            "analysis_data": analysis_results[:10],  # First 10 locations for preview
            "output_file": output_path if output_path else None
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error analyzing skills by location: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def create_skills_location_heatmap(file_path: str, skills_column: str, location_column: str, 
                                  output_path: str, top_skills: int = 15, top_locations: int = 10) -> str:
    """
    Create a heatmap showing skills distribution across locations.
    
    Args:
        file_path: Path to the data file
        skills_column: Column name containing comma-separated skills
        location_column: Column name containing location information
        output_path: Path where to save the heatmap image
        top_skills: Number of top skills to include (default: 15)
        top_locations: Number of top locations to include (default: 10)
    
    Returns:
        Information about the created skills-location heatmap
    """
    try:
        if not VISUALIZATION_AVAILABLE:
            return f"Error: {VISUALIZATION_ERROR}"
            
        import pandas as pd
        from pathlib import Path
        from collections import defaultdict, Counter
        
        # Load the data
        file_extension = Path(file_path).suffix.lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        if skills_column not in df.columns:
            return f"Error: Column '{skills_column}' not found in data"
        if location_column not in df.columns:
            return f"Error: Column '{location_column}' not found in data"
        
        # Parse skills and create location-skill matrix
        location_skills = defaultdict(list)
        all_skills = Counter()
        
        for _, row in df.iterrows():
            location = row[location_column]
            skills_str = row[skills_column]
            
            if pd.isna(location) or pd.isna(skills_str):
                continue
                
            skills = [skill.strip() for skill in str(skills_str).split(',') if skill.strip()]
            location_skills[location].extend(skills)
            all_skills.update(skills)
        
        # Get top skills and locations
        top_skills_list = [skill for skill, _ in all_skills.most_common(top_skills)]
        
        # Calculate location totals and get top locations
        location_totals = {loc: len(skills) for loc, skills in location_skills.items()}
        top_locations_list = sorted(location_totals.keys(), key=lambda x: location_totals[x], reverse=True)[:top_locations]
        
        # Create matrix
        matrix_data = []
        for location in top_locations_list:
            location_skill_counts = Counter(location_skills[location])
            total_skills_in_location = sum(location_skill_counts.values())
            
            row = []
            for skill in top_skills_list:
                # Calculate percentage of this skill in this location
                percentage = (location_skill_counts[skill] / total_skills_in_location * 100) if total_skills_in_location > 0 else 0
                row.append(percentage)
            matrix_data.append(row)
        
        # Create DataFrame for heatmap
        heatmap_df = pd.DataFrame(matrix_data, index=top_locations_list, columns=top_skills_list)
        
        # Create the heatmap
        plt.figure(figsize=(max(12, len(top_skills_list) * 0.8), max(8, len(top_locations_list) * 0.6)))
        sns.heatmap(heatmap_df, 
                   annot=True, 
                   fmt='.1f',
                   cmap='YlOrRd',
                   cbar_kws={'label': 'Skill Percentage (%)'},
                   linewidths=0.5)
        
        plt.title(f'Skills Distribution Across Top {top_locations} Locations\n(Top {top_skills} Skills)')
        plt.xlabel('Skills')
        plt.ylabel('Locations')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        result = {
            "skills_location_heatmap_created": True,
            "top_skills_analyzed": len(top_skills_list),
            "top_locations_analyzed": len(top_locations_list),
            "skills_included": top_skills_list,
            "locations_included": top_locations_list,
            "output_file": output_path,
            "file_size": Path(output_path).stat().st_size if Path(output_path).exists() else 0
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error creating skills-location heatmap: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def analyze_salary_by_location_and_skills(file_path: str, salary_column: str, location_column: str, 
                                        skills_column: str, output_path: Optional[str] = None) -> str:
    """
    Analyze salary statistics by location and skills combination.
    
    Args:
        file_path: Path to the data file
        salary_column: Column name containing salary information
        location_column: Column name containing location information
        skills_column: Column name containing comma-separated skills
        output_path: Optional path to save the analysis results
    
    Returns:
        Salary analysis by location and skills
    """
    try:
        import pandas as pd
        from pathlib import Path
        from collections import defaultdict
        import re
        
        # Load the data
        file_extension = Path(file_path).suffix.lower()
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_extension == '.tsv':
            df = pd.read_csv(file_path, sep='\t')
        else:
            df = pd.read_csv(file_path)
        
        # Validate columns exist
        for col in [salary_column, location_column, skills_column]:
            if col not in df.columns:
                return f"Error: Column '{col}' not found in data"
        
        # Clean and convert salary data
        def extract_salary(salary_str):
            if pd.isna(salary_str):
                return None
            # Extract numbers from salary string (handle ranges by taking average)
            numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', str(salary_str))
            if len(numbers) == 0:
                return None
            elif len(numbers) == 1:
                return float(numbers[0].replace(',', ''))
            else:
                # Take average of range
                nums = [float(n.replace(',', '')) for n in numbers]
                return sum(nums) / len(nums)
        
        df['salary_numeric'] = df[salary_column].apply(extract_salary)
        
        # Filter out rows with missing data
        df_clean = df.dropna(subset=['salary_numeric', location_column, skills_column])
        
        if len(df_clean) == 0:
            return "Error: No valid data rows found after cleaning"
        
        # Analyze by location
        location_analysis = []
        for location in df_clean[location_column].unique():
            location_data = df_clean[df_clean[location_column] == location]
            
            salaries = location_data['salary_numeric']
            location_stats = {
                "location": location,
                "job_count": len(location_data),
                "avg_salary": round(salaries.mean(), 2),
                "median_salary": round(salaries.median(), 2),
                "min_salary": round(salaries.min(), 2),
                "max_salary": round(salaries.max(), 2),
                "std_salary": round(salaries.std(), 2)
            }
            location_analysis.append(location_stats)
        
        # Sort by average salary
        location_analysis.sort(key=lambda x: x["avg_salary"], reverse=True)
        
        # Analyze by top skills
        skill_salary_data = defaultdict(list)
        
        for _, row in df_clean.iterrows():
            skills_str = row[skills_column]
            salary = row['salary_numeric']
            
            if pd.isna(skills_str):
                continue
                
            skills = [skill.strip() for skill in str(skills_str).split(',') if skill.strip()]
            for skill in skills:
                skill_salary_data[skill].append(salary)
        
        # Calculate skill statistics (only for skills with enough data points)
        skill_analysis = []
        for skill, salaries in skill_salary_data.items():
            if len(salaries) >= 5:  # At least 5 data points
                skill_stats = {
                    "skill": skill,
                    "job_count": len(salaries),
                    "avg_salary": round(sum(salaries) / len(salaries), 2),
                    "median_salary": round(sorted(salaries)[len(salaries)//2], 2),
                    "min_salary": round(min(salaries), 2),
                    "max_salary": round(max(salaries), 2)
                }
                skill_analysis.append(skill_stats)
        
        # Sort by average salary
        skill_analysis.sort(key=lambda x: x["avg_salary"], reverse=True)
        
        # Save analysis if output path provided
        if output_path:
            analysis_data = {
                "location_analysis": location_analysis,
                "skill_analysis": skill_analysis[:50]  # Top 50 skills
            }
            
            if output_path.endswith('.json'):
                with open(output_path, 'w') as f:
                    json.dump(analysis_data, f, indent=2)
            else:
                # Create separate sheets for locations and skills
                with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                    pd.DataFrame(location_analysis).to_excel(writer, sheet_name='Locations', index=False)
                    pd.DataFrame(skill_analysis).to_excel(writer, sheet_name='Skills', index=False)
        
        result = {
            "salary_analysis_completed": True,
            "locations_analyzed": len(location_analysis),
            "skills_analyzed": len(skill_analysis),
            "total_jobs_analyzed": len(df_clean),
            "top_paying_locations": location_analysis[:10],
            "top_paying_skills": skill_analysis[:15],
            "output_file": output_path if output_path else None
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error analyzing salary by location and skills: {str(e)}\n{traceback.format_exc()}"


def main():
    """Main entry point for the VisiData MCP server."""
    mcp.run()


if __name__ == "__main__":
    main() 