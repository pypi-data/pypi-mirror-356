"""
Module: mcpf_db.influx

This module provides functionality to write pandas DataFrames into an InfluxDB database. 
It includes utilities for handling configuration, authentication, and writing data 
to InfluxDB using the InfluxDB Python client.

Functions:
    - influx_df_write(data: dict[str, Any]) -> dict[str, Any]:
        Writes a pandas DataFrame into an InfluxDB database. The function supports 
        dynamic configuration through YAML arguments and allows for secure token 
        management.

Dependencies:
    - mcpf_core.core.routines: Provides utility functions for metadata handling and 
      database configuration retrieval.
    - mcpf_core.func.constants: Contains constants used throughout the module.
    - influxdb_client: The official Python client for InfluxDB.
    - influxdb_client.client.write_api.SYNCHRONOUS: Write API mode for synchronous 
      operations.
    - mcpf_db.influx.types.InfluxConfig: A configuration class for InfluxDB settings
        filled with 

Usage:
    The `influx_df_write` function is the primary entry point for writing data to 
    InfluxDB. It requires a dictionary containing the input data and configuration 
    details. The function dynamically merges default arguments with user-provided 
    arguments and writes the data to the specified InfluxDB bucket.

Example:
    ```yaml
input_path: &base_dir '.'
output_path: *base_dir
entry_point: 'main_p'
database_configs:
  - type: influx
    url: "http://my-influx:8086/"
    org: "acme.acres"
    bucket: "core-dump"

imports:
  - testfunc
  - mcpf_db.influx
pipelines:
  - main_p:
      - set_df:
          - with_index: true
            index_column: 'Ts'
      - setval:
          - output: 'API-TOKEN'
            value: 'secret-token-value'
      - influx_df_write:
          - measurement_name: 'my_measurement'
            token_from_data: 'API-TOKEN'
            tags: [ "Nam" ]
```

Notes:
    - The `token` argument is not recommended for use in YAML files as it is an 
      unencrypted secret. Use `token_from_data` for dynamic token management.
    - The `output` argument is not implemented yet and will raise a 
      `NotImplementedError` if provided.

"""
from typing import Any

import mcpf_core.core.routines as routines
import mcpf_core.func.constants as constants
from influxdb_client.client import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from mcpf_db.influx.types import InfluxConfig


def influx_df_write(data: dict[str, Any]) -> dict[str, Any]:
    """
    It writes its input pandas dataframe into influx database.
    Yaml args:
        'input':            it is a label in "data", which identifies the input data
                            (given in terms of pandas dataframe),
                            by default it is the value identified with the label
                            constants.DEFAULT_IO_DATA_LABEL (if it is a string)
        'type':             type of the database cpnfiguration to use, by default it is "influx"
        'token_from_data':  it is a label in "data", which identifies the API token.
                            Using `token_from_data` is preferred over `token` as you can
                            dynamically provide the token and you are not required to hardcode
                            the secret in the yaml file.
        'token':            API token for influx database. `token` takes precedence over
                            `token_from_data` if both are provided.
                            Note: `token` is not recommended to be used in the yaml file
                            as it is an unencrypted secret.
        'measurement_name': name of the measurement to be used in influx database.
        'tags':             list of columns to be written as tags into the influx measurements table.

    Returns in data:
        'output':   Not implemented yet!
                    it should be  a label in 'data' which identifies the output
                    (the content of the input pandas dataframe in pandas dataframe),
                    by default it is constants.DEFAULT_IO_DATA_LABEL
    """

    meta = routines.get_meta_data(data)
    # token: str = os.environ.get("INFLUXDB_TOKEN")
    arg = {
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "type": "influx",
        "token_from_data": "",
        "token": "",
        "measurement_name": "",
        "tags": [],
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]

    if "output" in arg:
        raise NotImplementedError("output is not implemented yet")

    db_conf = routines.get_db_config(meta, arg["type"])
    db_config = InfluxConfig.from_dict(db_conf)
    # override token if applicable
    if arg["token"]:
        token = arg["token"]
    elif arg["token_from_data"]:
        token = data[arg["token_from_data"]]
    else:
        token = db_config.token

    tags = arg["tags"] if "tags" in arg else []

    with influxdb_client.InfluxDBClient(url=db_config.url, token=token, org=db_config.org) as influx_client:
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)

        # writing entire dataframe into database.
        write_api.write(
            org=db_config.org,
            record=data[arg["input"]],
            bucket=db_config.bucket,
            data_frame_measurement_name=arg["measurement_name"],
            data_frame_tag_columns=tags,
        )
    # general code part 2/2
    routines.set_meta_in_data(data, meta)
    return data
