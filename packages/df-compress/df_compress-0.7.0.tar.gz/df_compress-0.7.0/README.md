[![Build](https://github.com/phchavesmaia/df-compress/actions/workflows/main.yaml/badge.svg)](https://github.com/phchavesmaia/df-compress/actions/workflows/main.yaml) 
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![PyPI](https://img.shields.io/pypi/v/df-compress?label=pypi%20package)
[![DOI](https://zenodo.org/badge/960013907.svg)](https://doi.org/10.5281/zenodo.15148480)

# df-compress
A python package to compress pandas DataFrames akin to Stata's `compress` command. This function may prove particularly helpfull to those dealing with large datasets.

## Installation
You can install `df-compress` by running the following command:
```python
pip install df_compress
```

## How to use
After installing the package use the following import: 
```python
from df_compress import compress
```

## Example
It follows a reproducible example on `df-compress` usage:
```python
from df_compress import compress
import pandas as pd
import numpy as np

size = 1000000
df = pd.DataFrame(columns=["Year","State","Value","Int_value"])
df.Year = np.random.randint(low=2000,high=2023,size=size).astype(str)
df.State = np.random.choice(['RJ','SP','ES','MT'],size=size)
df.Value= np.random.rand(size,1)
df.Int_value = df.Value*10 // 1

compress(df, show_conversions=True, parallel = False) # which modifies the original DataFrame without needing to reassign it
```
Which will print for you the transformations and memory saved:
```
Initial memory usage: 114.44 MB
Final memory usage: 7.63 MB
Memory reduced by: 106.81 MB (93.3%)

Variable type conversions:
   column    from       to  memory saved (MB)
     Year  object    int16          48.637264
    State  object category          47.683231
    Value float64  float32           3.814571
Int_value float64     int8           6.675594
```

## Optional Parameters
The function has three optimal parameters (arguments):
  - `convert_strings` (bool): Whether to attempt to parse object columns as numbers
    - defaults to `True`
  - `numeric_threshold` (float): Indicates the proportion of valid numeric entries needed to convert a string to numeric
    - defaults to `0.999`   
  - `show_conversions` (bool): whether to report the changes made column by column
    - defaults to `False`
  - `parallel` (bool): whether to compress the columns in parallel
    - defaults to `False`

## Parallelization Caveats
The parallelization is implemented using `Dask` and a local client. Moreover, the code is parallelized at the columns. Thus, opting for the parallel compression **does not** guarantees perfomance improvements and should be a conscious decision taken at the case-by-case basis. To prove this point, the implementation example provided above runs significantly slower when opting for the parallel compression (0.29x).

As far as I know, the reason why parallelization does not guarantee efficency regards the overhead time. Whenever you run some code in parallel you must "organize" it before computing the operation, which may take some time. If the efficiency gains from parallelizing the operation do not cover the overhead time, you incur an efficiency loss. Therefore, my recommendation is to only **opt for the parallel compression when you have a DataFrame with many columns**.

It follows a quick benchmark on a 12 CPUs computer to give you perspective on when to use the parallel compression:
```python
import pandas as pd
from df_compress import compress
import sys, os
import numpy as np
from time import time

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def timereps(reps, func):
    start = time()
    for i in range(0, reps):
        func()
    end = time()
    return (end - start) / reps

def benchmark_compression(df):
    print("Running benchmark on DataFrame with shape:", df.shape, "\n")
    
    # Non-parallel
    print("Testing non-parallel compression...")
    with HiddenPrints():
        time_non_parallel = timereps(10, lambda: compress(df.copy(deep=True), parallel=False, show_conversions=False))
    print(f"Non-parallel time: {time_non_parallel:.2f} seconds\n")
    
    # Parallel
    print("Testing parallel compression...")
    with HiddenPrints():
        time_parallel = timereps(10, lambda: compress(df.copy(deep=True), parallel=True, show_conversions=False))
    print(f"Parallel time: {time_parallel:.2f} seconds\n")
    
    # Summary
    speedup = time_non_parallel / time_parallel if time_parallel > 0 else float('inf')
    print(f"Parallel speedup: {speedup:.2f}x")

def generate_test_dataframe(n_rows=1_000_000, n_object_cols=10, n_numeric_cols=10):
    data = {}
    for i in range(n_object_cols):
        data[f"obj_{i}"] = np.random.choice(['A', 'B', 'C', 'D', 'E'], size=n_rows)
    for i in range(n_numeric_cols):
        data[f"num_{i}"] = np.random.randn(n_rows)
    return pd.DataFrame(data)
```
When testing for a 40 column DataFrame (`benchmark_compression(generate_test_dataframe(n_object_cols=20, n_numeric_cols=20))`) I find that
```
Running benchmark on DataFrame with shape: (1000000, 40) 

Testing non-parallel compression...
Non-parallel time: 17.60 seconds

Testing parallel compression...
Parallel time: 12.06 seconds

Parallel speedup: 1.46x
```
