import pandas as pd
import numpy as np
from dask.distributed import Client

def compress_column(col_data: pd.Series, convert_strings=True, numeric_threshold=0.999) -> pd.Series:
    """
    Compress a single column of a DataFrame by:
    - Downcasting numeric types
    - Converting object types to categories
    - Optionally converting strings to numeric types if a high percentage are numeric
    
    Parameters:
        col_data (pd.Series): The column data to compress.
        convert_strings (bool, optional): Whether to attempt parsing object columns as numbers. Defaults to True.
        numeric_threshold (float, optional): Proportion of valid numeric entries needed to convert (0.0 - 1.0). Defaults to 0.999.

    Returns:
        pd.Series: Compressed column data with reduced memory usage.
    """
    old_dtype = col_data.dtype
    new_data = col_data.copy()

    if pd.api.types.is_object_dtype(old_dtype):
        # Attempt numeric conversion if enabled
        if convert_strings:
            temp = pd.to_numeric(new_data, errors='coerce')
            if temp.notna().mean() >= numeric_threshold:
                new_data = temp

        # If still object, consider converting to category
        if pd.api.types.is_object_dtype(new_data.dtype):
            if new_data.nunique() / len(new_data) < 0.5:
                new_data = new_data.astype('category')

    # Downcast numeric types
    if pd.api.types.is_integer_dtype(new_data):
        # Downcast interger types
        new_data = pd.to_numeric(new_data, downcast='integer')
    elif pd.api.types.is_float_dtype(new_data):
        # Attempt to downcast float types to integers, if no information is lost. Otherwise, keep as float
        if np.all(np.isclose(new_data.dropna() % 1, 0)):
            new_data = pd.to_numeric(new_data, downcast='integer')
        else:
            new_data = pd.to_numeric(new_data, downcast='float')

    return new_data
    
def compress(df, convert_strings=True, numeric_threshold=0.999, show_conversions=False, parallel=False) -> pd.DataFrame:
    """
    Compress DataFrame by:
    - Applying `compress_column` to each column of the DataFrame
    
    Parameters:
    - convert_strings (bool): attempt to parse object columns as numbers
    - numeric_threshold (float): proportion of valid numeric entries needed to convert (0.0 - 1.0)
    - show_conversions (bool): whether to report the changes made column by column
    - parallel (bool): whether to use Dask for parallel processing
    
    Returns:
    - Compressed DataFrame (in place)
    """
    old_memory = df.memory_usage(deep=True) / 1024**2
    start_mem = old_memory.sum()
    print(f"Initial memory usage: {start_mem:.2f} MB")
    changes = []
        
    # Without parallel processing #
    if parallel == False:
        # looping over the columns
        for col in df.columns:
            col_data = df[col]
            old_dtype = col_data.dtype
            old_mem = old_memory[col]
            new_data = compress_column(col_data, convert_strings, numeric_threshold)

            new_dtype = new_data.dtype
            new_mem = new_data.memory_usage(deep=True) / 1024**2

            # If the dtype has changed, record the change
            if new_dtype != old_dtype:
                changes.append({
                    "column": col,
                    "from": str(old_dtype),
                    "to": str(new_dtype),
                    "memory saved (MB)": (old_mem - new_mem) 
                })

            # Update the DataFrame with the compressed column (in place)
            df[col] = new_data

        # Printing final memory usage
        end_mem = df.memory_usage(deep=True).sum() / 1024**2
        print(f"Final memory usage: {end_mem:.2f} MB")
        print(f"Memory reduced by: {start_mem - end_mem:.2f} MB ({100 * (start_mem - end_mem) / start_mem:.1f}%)\n")

        # Show conversions if requested
        if show_conversions==True:
            if changes:
                print("Variable type conversions:")
                print(pd.DataFrame(changes).to_string(index=False))
            else:
                print("No conversions were applied.")
                
    # With parallel processing #            
    else:
        with Client(processes=True, dashboard_address=":8788") as client:
            old_dtypes = df.dtypes
            
            # Submit each column to Dask scheduler
            futures = {
                col: client.submit(compress_column, df[col].copy(), convert_strings, numeric_threshold)
                for col in df.columns
            }

            # Gather results from futures
            results = client.gather(list(futures.values()))

            # Build DataFrame from gathered column results
            for col, new_col in zip(futures.keys(), results):
                df[col] = new_col
            new_memory = df.memory_usage(deep=True) / 1024**2
            end_mem = new_memory.sum()

            # Printing memory usage
            print(f"Final memory usage: {end_mem:.2f} MB")
            print(f"Memory reduced by: {start_mem - end_mem:.2f} MB ({100 * (start_mem - end_mem) / start_mem:.1f}%)\n")
            
            # Show conversions if requested
            if show_conversions==True:
                new_dtypes = df.dtypes
                for col in df.columns[old_dtypes != new_dtypes]:
                    changes.append({
                            "column": col,
                            "from": str(old_dtypes[col]),
                            "to": str(new_dtypes[col]),
                            "memory saved (MB)": (old_memory[col] - new_memory[col])
                        })
                
                if changes:
                    print("Variable type conversions:")
                    print(pd.DataFrame(changes).to_string(index=False))
                else:
                    print("No conversions were applied.")
                    
    return df