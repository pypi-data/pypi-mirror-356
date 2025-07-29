# Ohm AI Library Documentation

**Welcome to the Ohm library documentation!**

This Python library provides tools for interacting with the Ohm API, allowing you to access and analyze your battery data.

### Key Features

- Data Retrieval: Easily fetch battery observation metrics, dataset cycle data, and metadata.
- Filtering: Refine your data retrieval using flexible filter options.
- Data Handling: Work with data in a structured format using pandas DataFrames.

### Installation

```bash
pip install ohm-ai
```

### Usage

**1. Initialization:**

```python
from ohm_ai import OhmClient, OhmFilter, OhmFilterOperator, OhmFilterGroup, OhmFilterGroupType

# For synchronous operations
ohm_client = OhmClient(api_key="YOUR_API_TOKEN")
```

**2. Data Retrieval:**

- **Get Battery Observation Metrics:**

```python
# Get all battery observation metrics
observation_data = ohm_client.get_observation_data()
```

- **Get Battery Dataset Cycle Data:**

```python
# Get all battery dataset cycle data
cycle_data = ohm_client.get_dataset_cycle_data()
```

- **Get Battery Metadata:**

```python
# Get all battery metadata
metadata = ohm_client.get_metadata()
```

**3. Filtering:**

```python
# Create filters using OhmFilterOperator enumerable or their string values direcly
filter_1 = OhmFilter(column="voltage", operator=OhmFilterOperator.EQ, value=3.5)
filter_2 = OhmFilter(column="voltage", operator="equals", value=3.5)

# Create a filter group using the OhmFilterGroupType or their string values directly
filter_group_1 = OhmFilterGroup([filter_1, filter_2], type=OhmFilterGroupType.AND)
filter_group_2 = OhmFilterGroup([filter_1, filter_2], type="and")

# OhmFilterGroup objects can be nested to create complex logic
filter_group_3 = OhmFilterGroup([filter_group_1, filter_group_2], type="or")

# Retrieve a chunk of filtered observation data -> Returns a pandas dataframe object
# Use either a list of filters or a OhmFilterGroup object
filtered_observation_data = ohm_client.get_observation_data(filters=[filter_1, filter_2])
filtered_observation_data = ohm_client.get_observation_data(filters=filter_group_3)

# Retrieve a chunk of filtered dataset cycle data -> Returns a pandas dataframe object
filtered_cycle_data = ohm_client.get_dataset_cycle_data(filters=[filter_1, filter_2])
filtered_cycle_data = ohm_client.get_dataset_cycle_data(filters=filter_group_3)

# Retrieve a chunk of filtered metadata -> Returns a pandas dataframe object
filtered_metadata = ohm_client.get_metadata(filters=[filter_1, filter_2])
filtered_metadata = ohm_client.get_metadata(filters=filter_group_3)
```