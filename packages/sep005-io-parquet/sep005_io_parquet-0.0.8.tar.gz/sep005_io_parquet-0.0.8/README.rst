SEP005 24SEA parquet io
-----------------------

Basic package to import data from parquet files as stored by 24SEA's SHM solutions.

NOTE: This wont work for any parquet file, but assumes an underlying structure in the parquet file.

Using the package
------------------

In its most basic usage the package allows to load the parquet file from a specified path:

    .. code-block:: python

        from sep005_io_parquet import read_parquet

        file_path = # Path to the parquet file of interest
        signals = read_parquet(file_path)


The imported signals respect the SEP005 set of rules for timeseries.

Acknowledgements
----------------
