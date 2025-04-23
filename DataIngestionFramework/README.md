# Fabric Data Ingestion Framework

## Current Components

### Completed Modules

#### 1. [Ingestion Logs with Event Streams](../Docs/IngestionLogsWithEventStreams.md)
This module demonstrates how to implement a logging system for data ingestion processes using Event Streams and Event House in Microsoft Fabric. It provides:
- A way to track the status of data ingestion processes
- Integration with Fabric's Event Streams for real-time monitoring
- Examples of error handling and retry logic

<div align="left">
  <img src="../images/IngestionLogsRTI.png" alt="Ingestion Logs Real-Time Intelligence" height="500" width="800" />
</div>

#### 2. [DAG Generation](../Docs/DagGen.md)
This module shows how to programmatically generate Directed Acyclic Graphs (DAGs) for orchestrating data pipelines in Fabric. It leverages the `notebookutils.notebook.runMultiple()` method, which allows you to run multiple notebooks in parallel or with a predefined topological structure. The API uses a multi-thread implementation mechanism within a spark session, meaning that reference notebook runs share compute resources. This module covers:
- Dynamic dependency management
- Simplified orchestration for running multiple notebooks simultaneously 
- Efficient resource utilization by running notebooks in parallel

For more information on `notebookutils.notebook.runMultiple()`, you can visit the [official Microsoft documentation](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-utilities#reference-run-multiple-notebooks-in-parallel).

## Package Structure

The package is organized into several modules:
- `dags`: Contains functionality for DAG generation and management
- `eventhouse`: Provides connectors for Fabric Event House
- `eventstreams`: Handles sending events to Fabric Event Streams
- `ingestion`: Core data ingestion functionality
- `utils`: Utility functions for various operations

## Getting Started

Clone this repository and install:

```
git clone <this repo>
cd FabricDataEng/DataIngestionFramework
python -m pip install --upgrade build
pip install dist/*.whl
```

## Contributing

This project is meant to grow with the community's needs. Feel free to suggest new modules or improvements to existing ones by opening an issue or submitting a pull request.

## Disclaimer

This framework is not intended for production use. It serves as a learning resource and starting point for your own implementations.
