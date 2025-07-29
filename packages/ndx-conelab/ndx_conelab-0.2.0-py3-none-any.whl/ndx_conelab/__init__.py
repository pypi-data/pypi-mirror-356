import os
from importlib import import_module
from typing import List

from pynwb import load_namespaces, get_class

# PyNWB 3.0 removed the public ``NWBNamespaceCatalog`` helper, but some older
# versions still expose it.  We *optionally* import it – if unavailable we will
# fall back to a lightweight YAML parse.

try:
    from pynwb.spec import NWBNamespaceCatalog  # type: ignore
except ImportError:  # PyNWB >=3.0
    NWBNamespaceCatalog = None  # type: ignore

# -----------------------------------------------------------------------------
# Namespace loading
# -----------------------------------------------------------------------------

HERE = os.path.dirname(__file__)
SPEC_PATH = os.path.join(HERE, "spec")

# Load/Reload namespace every time the package is imported – this is cheap (~ms)
load_namespaces(os.path.join(SPEC_PATH, "conelab.namespace.yaml"))

# -----------------------------------------------------------------------------
# Ensure the original, hand-coded ``TaskParameters`` class is imported so it is
# properly registered with PyNWB.  (It may later be superseded by a generator
# driven version, but importing it has negligible overhead and maintains full
# backwards-compatibility.)
# -----------------------------------------------------------------------------

from .conelab_extension import TaskParameters  # noqa: E402  pylint: disable=wrong-import-position

# -----------------------------------------------------------------------------
# Auto-import all Python modules living in ``ndx_conelab/extensions`` so that any
# hand-written subclasses (if present) are registered right away.  This keeps
# backwards compatibility with the original, hand-coded ``TaskParameters``
# class while allowing future, code-generated subclasses to coexist.
# -----------------------------------------------------------------------------

_EXT_PKG = f"{__name__}.extensions"
try:
    _mod = import_module(_EXT_PKG)
    # Walk sub-modules (flat directory scan is enough – we don't expect nested
    # packages under "extensions").
    import pkgutil

    for _finder, _name, _is_pkg in pkgutil.iter_modules(_mod.__path__):
        import_module(f"{_EXT_PKG}.{_name}")
except ModuleNotFoundError:
    # The extensions package may not exist in early development versions –
    # that's fine; generator.py will create it when needed.
    pass

# -----------------------------------------------------------------------------
# Collect neurodata_type names defined in the namespace.
# Prefer the PyNWB helper when available; otherwise fall back to a lightweight
# YAML parse that only extracts ``neurodata_type_def`` fields from extension
# YAMLs.
# -----------------------------------------------------------------------------

_types: List[str] = []

namespace_yaml_path = os.path.join(SPEC_PATH, "conelab.namespace.yaml")

if NWBNamespaceCatalog is not None:
    _catalog = NWBNamespaceCatalog()
    _catalog.load_namespaces(namespace_yaml_path)
    _namespace_obj = _catalog.namespaces["conelab"]
    if hasattr(_namespace_obj, "data_types"):
        _types = list(_namespace_obj.data_types)  # type: ignore[attr-defined]
    else:
        _types = list(getattr(_namespace_obj, "neurodata_types"))  # old PyNWB
else:
    # Fallback: parse YAML to find all ``source`` files, then extract group
    # definitions.
    import yaml

    with open(namespace_yaml_path, "r", encoding="utf-8") as fp:
        ns_dict = yaml.safe_load(fp)

    schema_specs = ns_dict["namespaces"][0]["schema"]
    for entry in schema_specs:
        src = entry.get("source")
        if not src:
            continue
        ext_path = os.path.join(SPEC_PATH, src)
        if not os.path.exists(ext_path):
            continue
        with open(ext_path, "r", encoding="utf-8") as e_fp:
            ext_dict = yaml.safe_load(e_fp)
        for grp in ext_dict.get("groups", []):
            ndt = grp.get("neurodata_type_def")
            if ndt:
                _types.append(ndt)

# Filter out base classes we don't want to expose (case-by-case list)
_filter_out = {"LabMetaData"}

# Always keep TaskParameters explicitly
_filter_out.discard("TaskParameters")

for _t in _types:
    if _t in _filter_out:
        continue
    try:
        globals()[_t] = get_class(_t, "conelab")
    except Exception:  # noqa: BLE001 – best-effort; skip if not loadable
        continue

# -----------------------------------------------------------------------------
# Public API re-exports
# -----------------------------------------------------------------------------
from .generator import generate_extension  # noqa: E402 – after top-level init

# Refresh __all__ now that generate_extension is in namespace
_exports = []
for _name, _obj in list(globals().items()):
    if _name.startswith("_"):
        continue
    if _name in ("os", "import_module", "load_namespaces", "get_class", "NWBNamespaceCatalog", "pkgutil"):
        continue
    _exports.append(_name)

__all__ = _exports 