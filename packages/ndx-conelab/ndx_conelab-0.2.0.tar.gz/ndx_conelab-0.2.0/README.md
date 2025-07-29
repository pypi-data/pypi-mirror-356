# ndx-conelab

NWB extension for custom Task Parameters used in the Cone Lab.

This package provides the NWB extension definition (YAML) and Python API 
for storing and retrieving Cone Lab-specific task parameters within NWB 2.0 files.

## Installation

```bash
pip install ndx-conelab
```
(Once published to PyPI)

Or, for local development:
```bash
git clone https://github.com/JConeLab/ndx-conelab.git # Or your repo URL
cd ndx-conelab
pip install -e .
```

## Usage

Once installed, PyNWB will automatically be able to read NWB files containing
the `conelab.TaskParameters` neurodata type.

To create this data type in a new NWB file:

```python
from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime
from ndx_conelab import TaskParameters # Import the custom class

# ... (create your NWBFile object) ...
nwbfile = NWBFile(
    session_description='My session description',
    identifier='MY_SESSION_ID',
    session_start_time=datetime.now().astimezone(),
    # ... other required fields ...
)

# Create an instance of your custom TaskParameters
conelab_task_params = TaskParameters(
    name="MyExperimentTaskParams", # Name is required (from LabMetaData parent)
    reaction_time_window_ms=1000,
    intertrial_interval_ms=2000,
    iti_jitter_percentage=0.2,
    # ... fill in other parameters as needed ...
    description="Parameters for the RDK task, easy difficulty."
)

# Add the TaskParameters object to the NWB file.
# Since TaskParameters inherits from LabMetaData, it can be added directly
# using add_lab_meta_data(). PyNWB will typically store this under 
# /general/lab_meta_data/<object_name>/ 
# (e.g., /general/lab_meta_data/MyExperimentTaskParams/ in this case)
nwbfile.add_lab_meta_data(conelab_task_params)

# ... (write your NWB file) ...
# with NWBHDF5IO('test_nwb_with_conelab_extension.nwb', 'w') as io:
#     io.write(nwbfile)
```

## Extension Definition

The extension schema is defined in `ndx_conelab/spec/`:
* `conelab.namespace.yaml`
* `conelab.extensions.yaml`

This defines a `TaskParameters` group inheriting from `LabMetaData` to store various experimental parameters. 