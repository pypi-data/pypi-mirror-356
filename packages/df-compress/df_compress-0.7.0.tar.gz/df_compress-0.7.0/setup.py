from setuptools import setup
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='df-compress',
    version='0.7.0',    
    description="A python package to compress pandas DataFrames akin to Stata's `compress` command",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    url='https://github.com/phchavesmaia/df-compress',
    author='Pedro H. Chaves Maia',
    author_email='pedro.maia@imdsbrasil.org',
    license='MIT',
    packages=['df_compress'],
    install_requires=['pandas',
                      'numpy',  
                      'dask',  
                      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.13',
    ],
)
