from pynwb import get_class, register_class
from pynwb.file import LabMetaData
from hdmf.utils import docval, getargs, popargs

# Get the namespace
namespace = "conelab"


@register_class("TaskParameters", namespace)
class TaskParameters(LabMetaData):
    """A custom NWB container for storing task-specific parameters from the Cone Lab."""

    __nwbfields__ = (
        "reaction_time_window_ms",
        "intertrial_interval_ms",
        "iti_jitter_percentage",
        "prestimulus_min_ms",
        "prestimulus_max_ms",
        "solenoid_open_duration_ms",
        "solenoid_open_count",
        "too_fast_threshold_ms",
        "false_alarm_timeout_ms",
        "fail_timeout_ms",
    )

    @docval(
        {
            "name": "name",
            "type": str,
            "doc": "Name of this TaskParameters set (e.g., \"RDK_easy_short_ITI\").",
        },
        {
            "name": "reaction_time_window_ms",
            "type": int,
            "doc": "Reaction time window in milliseconds.",
            "default": None,
        },
        {
            "name": "intertrial_interval_ms",
            "type": int,
            "doc": "Base intertrial interval in milliseconds.",
            "default": None,
        },
        {
            "name": "iti_jitter_percentage",
            "type": float,
            "doc": "Percentage of ITI to use for jitter (e.g., 0.1 for 10%).",
            "default": None,
        },
        {
            "name": "prestimulus_min_ms",
            "type": int,
            "doc": "Minimum prestimulus duration in milliseconds.",
            "default": None,
        },
        {
            "name": "prestimulus_max_ms",
            "type": int,
            "doc": "Maximum prestimulus duration in milliseconds.",
            "default": None,
        },
        {
            "name": "solenoid_open_duration_ms",
            "type": int,
            "doc": "Duration of solenoid opening for reward/punishment in milliseconds.",
            "default": None,
        },
        {
            "name": "solenoid_open_count",
            "type": int,
            "doc": "Number of times the solenoid opens per event.",
            "default": None,
        },
        {
            "name": "too_fast_threshold_ms",
            "type": int,
            "doc": "Threshold for defining a response as 'too fast' in milliseconds.",
            "default": None,
        },
        {
            "name": "false_alarm_timeout_ms",
            "type": int,
            "doc": "Timeout duration for a false alarm in milliseconds.",
            "default": None,
        },
        {
            "name": "fail_timeout_ms",
            "type": int,
            "doc": "Timeout duration for a failure/miss in milliseconds.",
            "default": None,
        },
        {
            "name": "description",
            "type": str,
            "doc": "Description of this set of task parameters or its use case.",
            "default": "N/A",
        },
    )
    def __init__(self, name, reaction_time_window_ms=None, intertrial_interval_ms=None,
                 iti_jitter_percentage=None, prestimulus_min_ms=None, prestimulus_max_ms=None,
                 solenoid_open_duration_ms=None, solenoid_open_count=None,
                 too_fast_threshold_ms=None, false_alarm_timeout_ms=None,
                 fail_timeout_ms=None, description=None):

        super().__init__(name=name)
        self.description = description
        # KNOWN ISSUE: The 'description' field currently reads back as its default value ('N/A' or None)
        # when the NWB file is re-opened, despite being set here.
        # All custom fields work correctly. Deferring full fix for 'description'.

        # Set custom fields directly from explicit arguments
        self.reaction_time_window_ms = reaction_time_window_ms
        self.intertrial_interval_ms = intertrial_interval_ms
        self.iti_jitter_percentage = iti_jitter_percentage
        self.prestimulus_min_ms = prestimulus_min_ms
        self.prestimulus_max_ms = prestimulus_max_ms
        self.solenoid_open_duration_ms = solenoid_open_duration_ms
        self.solenoid_open_count = solenoid_open_count
        self.too_fast_threshold_ms = too_fast_threshold_ms
        self.false_alarm_timeout_ms = false_alarm_timeout_ms
        self.fail_timeout_ms = fail_timeout_ms 