# DAG Generator Module

This module provides the `DagGenerator` class, which is used to create JSON configurations for Microsoft Fabric notebook job definitions (Directed Acyclic Graphs or DAGs).

## Overview

The `DagGenerator` class helps build structured workflow definitions that can be used to schedule and execute notebook activities in Microsoft Fabric, with control over execution order, dependencies, and resources.

## Features

- Generate JSON configurations for DAGs from a list of tables.
- Support for specifying dependencies between activities.
- Advanced configuration options for custom notebook paths and arguments.

## Usage

### Steps to Use the `DagGenerator` Class

1. **Import the Class**
   
   Import the `DagGenerator` class from the module:
   
   ```python
   from fabricdataingest.dags import DagGenerator
   ```

2. **Initialize the `DagGenerator`**
   
   Create an instance of the `DagGenerator` class by providing the required parameters:
   
   ```python
   dag_generator = DagGenerator(
       customer="customer_name",
       notebookPath="/path/to/notebook",
       shufflePartitions=10,
       timeoutInSeconds=3600,
       concurrency=5
   )
   ```

3. **Generate JSON for Tables**
   
   Use the `generate_json` method to create a DAG configuration for a list of tables:
   
   ```python
   tables = ["SalesLT.Customer", "SalesLT.Address", "SalesLT.Product"]
   dag_json = dag_generator.generate_json(tables)
   print(dag_json)
   ```

4. **Add Dependencies (Optional)**
   
   If certain tables depend on others, specify the dependencies as a dictionary:
   
   ```python
   dependencies = {
       "SalesLT.OrderDetail": ["NotebookCustomer_SalesLT.Order"]
   }
   dag_json = dag_generator.generate_json(tables, dependencies)
   ```

5. **Advanced Configuration**
   
   For more complex workflows, use the `generate_json_from_array` method with custom notebook configurations:
   
   ```python
   notebook_configs = [
       {
           "table": "SalesLT.Customer",
           "notebook_path": "/path/to/customer_notebook"
       },
       {
           "table": "SalesLT.Order",
           "dependencies": ["NotebookCustomer_SalesLT.Customer"],
           "args": {"additional_param": "value"}
       }
   ]
   advanced_dag = dag_generator.generate_json_from_array(notebook_configs)
   print(advanced_dag)
   ```

## Methods

### `generate_json(tables, dependencies=None)`

Generates a JSON configuration for a list of tables.

- **Parameters**:
  - `tables` (list): List of table names to process.
  - `dependencies` (dict, optional): Dictionary mapping tables to their dependency activities.

- **Returns**: JSON string representing the DAG.

### `generate_json_from_array(notebook_configs)`

Generates a JSON configuration from an array of notebook configurations.

- **Parameters**:
  - `notebook_configs` (list): List of dictionaries, each containing:
    - `table` (str): Table name.
    - `dependencies` (list, optional): List of activity names this table depends on.
    - `notebook_path` (str, optional): Override the default notebook path.
    - `args` (dict, optional): Additional arguments for this specific notebook.

- **Returns**: JSON string representing the DAG.

## Testing

To test the functionality, create test cases for different configurations of tables, dependencies, and advanced notebook settings.