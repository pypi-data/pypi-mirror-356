"""
ndx_conelab.generator
~~~~~~~~~~~~~~~~~~~~~

Utility for generating new NWB extension YAML files for Cone Lab task templates.

This module is **intentionally lightweight** – it has **no external
runtime-dependencies** beyond the standard library and ``PyYAML``.  Keeping the
implementation in a single file (instead of, e.g.
``ndx_conelab/tools/task_template_generator``) avoids growing the public API
surface unnecessarily.

The exposed public API is two-fold:
    1. :pyfunc:`generate_extension` – programmatic entry-point.
    2. ``ndx-conelab gen <spec.json>`` – command-line interface defined via
       ``pyproject.toml``.

Both entry-points take a JSON **task-spec** file produced by the RSO
``task-template-wizard`` and turn it into a fully-fledged NWB extension that is
immediately discoverable by ``PyNWB`` once the ``ndx_conelab`` package is
re-imported.

Key behaviours
--------------
* Creates ``ndx_conelab/extensions/<TaskName>.extensions.yaml``.  The YAML
  conforms to the NWB Specification Language and defines a new
  ``LabMetaData`` subtype with attributes derived from the JSON spec.
* Appends a reference to the generated YAML into
  ``ndx_conelab/spec/conelab.namespace.yaml`` so the extension is loaded the
  next time :pymeth:`pynwb.load_namespaces` is executed.
* Reloads the namespace **in-process** (via ``pynwb.load_namespaces``) so the
  new neurodata_type is available without having to restart the Python
  interpreter.

The JSON schema expected by this script matches the one produced by the
original RSO ``task_template_generator`` tool, but, to stay
self-contained, we only rely on a **minimum subset** of that schema:

```
{
  "task_name": "RDKTaskParameters",        # required – valid Python / NWB ID
  "description": "...",                    # optional – fallback to "N/A"
  "fields": [                              # required – list of attribute defs
    {"name": "foo_ms", "type": "int", "doc": "Foo window (ms)"},
    ...
  ]
}
```

Anything beyond these keys is currently ignored, which keeps the generator
forward-compatible with future schema extensions.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List
import sys
import tempfile
from contextlib import contextmanager
import logging

import yaml
from pynwb import load_namespaces  # type: ignore
from filelock import FileLock, Timeout

try:
    # Optional – keep lightweight fallback if jsonschema missing in runtime env
    import jsonschema  # type: ignore
except ModuleNotFoundError:  # pragma: no cover – optional dependency
    jsonschema = None  # type: ignore

# -----------------------------------------------------------------------------
# Constants & Paths
# -----------------------------------------------------------------------------
log = logging.getLogger(__name__)

HERE = Path(__file__).parent
PACKAGE_ROOT = HERE
SPEC_DIR = PACKAGE_ROOT / "spec"
NAMESPACE_YAML = SPEC_DIR / "conelab.namespace.yaml"
EXTENSIONS_DIR = PACKAGE_ROOT / "extensions"

# Ensure extensions directory exists inside the installed package
EXTENSIONS_DIR.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# JSON Schema – best-practice validation but optional to avoid hard dep
# -----------------------------------------------------------------------------

_JSON_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["task_name", "fields"],
    "properties": {
        "task_name": {
            "type": "string",
            "pattern": r"^[A-Za-z_][A-Za-z0-9_]*$",
            "description": "Valid Python identifier to become the neurodata_type_def",
        },
        "description": {"type": "string"},
        "fields": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["name", "type"],
                "properties": {
                    "name": {
                        "type": "string",
                        "pattern": r"^[A-Za-z_][A-Za-z0-9_]*$",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["int", "float", "str", "string", "bool"],
                    },
                    "doc": {"type": "string"},
                },
            },
        },
    },
}

# -----------------------------------------------------------------------------
# Utility helpers
# -----------------------------------------------------------------------------

@contextmanager
def _atomic_write(path: Path, mode: str = "w", encoding: str | None = "utf-8"):
    """Write to *path* atomically (write-rename)."""
    tmp_fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=".__tmp", text="b" not in mode)
    tmp_path = Path(tmp_name)
    try:
        with open(tmp_fd, mode, encoding=encoding) as fp:  # type: ignore[arg-type]
            yield fp
        tmp_path.replace(path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass


def _validate_spec(spec: Dict[str, Any]) -> None:
    """Validate *spec* against the JSON schema and business rules."""
    if jsonschema is not None:
        jsonschema.validate(spec, _JSON_SCHEMA)  # type: ignore[arg-type]
    else:
        # Fallback manual checks if jsonschema not installed – maintain original behaviour
        required = {"task_name", "fields"}
        missing = required - set(spec)
        if missing:
            raise ValueError(f"Missing required keys in spec: {', '.join(missing)}")
        if not str(spec["task_name"]).isidentifier():
            raise ValueError("'task_name' must be a valid identifier")
        if not isinstance(spec["fields"], list) or not spec["fields"]:
            raise ValueError("'fields' must be a non-empty list")

    # ---- Business-level checks ----
    seen_names: set[str] = set()
    for f in spec["fields"]:
        name = f["name"]
        if name in seen_names:
            raise ValueError(f"Duplicate field name in spec: {name}")
        seen_names.add(name)


# -----------------------------------------------------------------------------
# Public helpers
# -----------------------------------------------------------------------------

def generate_extension(spec_json: Path | str) -> Path:
    """Generate a new NWB extension from *spec_json*.

    Parameters
    ----------
    spec_json
        Path (or str) pointing to the JSON task specification.

    Returns
    -------
    Path
        The path to the generated ``*.extensions.yaml`` file.
    """

    spec_path = Path(spec_json).expanduser().resolve()
    if not spec_path.exists():
        raise FileNotFoundError(f"Task-spec JSON not found: {spec_path}")

    with spec_path.open("r", encoding="utf-8") as fp:
        spec: Dict[str, Any] = json.load(fp)

    # ------------------------------------------------------------------
    # BEST-PRACTICE VALIDATION (schema + business rules)
    # ------------------------------------------------------------------
    log.info({"event": "validating_spec", "path": str(spec_path)})
    try:
        _validate_spec(spec)
    except (ValueError, Exception) as e:
        log.error({"event": "spec_validation_failed", "error": str(e)})
        raise e

    task_name: str = spec["task_name"]
    fields: List[Dict[str, Any]] = spec["fields"]
    description: str = spec.get("description", "N/A")

    # ------------------------------------------------------------------
    # Render the YAML data-structure following NWB spec language.
    # ------------------------------------------------------------------
    yaml_dict: Dict[str, Any] = {
        "groups": [
            {
                "neurodata_type_def": task_name,
                "neurodata_type_inc": "LabMetaData",
                "doc": description,
                "attributes": [
                    {
                        "name": f["name"],
                        "dtype": _convert_dtype(f["type"]),
                        "doc": f.get("doc", "N/A"),
                    }
                    for f in fields
                ],
            }
        ]
    }

    # Destination: ndx_conelab/extensions/<TaskName>.extensions.yaml
    dest_yaml = EXTENSIONS_DIR / f"{task_name}.extensions.yaml"

    # Atomically write the extension file (protect against concurrent writers)
    log.info(
        {
            "event": "writing_extension_yaml",
            "neurodata_type": task_name,
            "path": str(dest_yaml),
        }
    )
    with _atomic_write(dest_yaml, "w", encoding="utf-8") as fp:
        yaml.safe_dump(yaml_dict, fp, sort_keys=False)

    # ------------------------------------------------------------------
    # Amend namespace file so PyNWB includes the new schema (atomic & locked)
    # ------------------------------------------------------------------
    rel_path_from_spec = os.path.relpath(dest_yaml, SPEC_DIR)
    lock_path = NAMESPACE_YAML.with_suffix(".lock")
    
    log.debug({"event": "acquiring_namespace_lock", "path": str(lock_path)})
    try:
        with FileLock(lock_path, timeout=5):
            log.debug({"event": "namespace_lock_acquired"})
            with NAMESPACE_YAML.open("r", encoding="utf-8") as fp:
                namespace_data: Dict[str, Any] = yaml.safe_load(fp)

            schema_list: List[Dict[str, str]] = namespace_data["namespaces"][0]["schema"]
            if not any(s.get("source") == rel_path_from_spec for s in schema_list):
                log.info(
                    {
                        "event": "amending_namespace",
                        "adding_source": rel_path_from_spec,
                    }
                )
                schema_list.append({"source": rel_path_from_spec})
                with _atomic_write(NAMESPACE_YAML, "w", encoding="utf-8") as fp:
                    yaml.safe_dump(namespace_data, fp, sort_keys=False)
            else:
                log.info(
                    {
                        "event": "namespace_unchanged",
                        "reason": "source already exists",
                        "source": rel_path_from_spec,
                    }
                )
    except Timeout:
        log.error(
            {
                "event": "namespace_lock_timeout",
                "path": str(lock_path),
                "timeout": 5,
            }
        )
        raise  # Re-raise so the caller knows the operation failed

    # ------------------------------------------------------------------
    # Reload namespace *in-process* so get_class() works immediately.  PyNWB
    # caches loaded namespaces by (name, version).  If the namespace is
    # already present we explicitly remove it from the internal map so that it
    # is re-parsed with the newly added extension source.
    # ------------------------------------------------------------------

    from pynwb import __TYPE_MAP  # type: ignore

    ns_keys = set()
    try:
        ns_keys = set(__TYPE_MAP.namespace_catalog.namespaces.keys())  # type: ignore[attr-defined]
    except Exception:
        pass

    if "conelab" in ns_keys:
        # This private API is stable within HDMF – we remove the namespace so
        # that the next load_namespaces call re-ingests it.
        del __TYPE_MAP.namespace_catalog.namespaces["conelab"]  # type: ignore[attr-defined]
        log.debug({"event": "purged_cached_namespace", "namespace": "conelab"})

    load_namespaces(str(NAMESPACE_YAML))
    log.info({"event": "namespace_reloaded", "path": str(NAMESPACE_YAML)})

    return dest_yaml


# -----------------------------------------------------------------------------
# CLI – ``ndx-conelab gen <spec.json>``
# -----------------------------------------------------------------------------

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ndx-conelab",
        description="Generate ConeLab NWB extension from task-spec JSON.",
    )
    # Accept optional "gen" subcommand for forward-compat but keep it simple
    parser.add_argument("args", nargs="*", help="[gen] <spec.json>")
    return parser


def cli() -> None:  # Entry-point declared in pyproject.toml
    argv = sys.argv[1:]
    if argv and argv[0] == "gen":
        argv = argv[1:]
    if len(argv) != 1:
        _build_arg_parser().print_help(sys.stderr)
        sys.exit(1)
    spec_path = Path(argv[0])
    try:
        dest = generate_extension(spec_path)
        print(f"✅ Extension generated → {dest}")
        log.info({"event": "cli_success", "source": str(spec_path), "dest": str(dest)})
    except Exception as e:
        print(f"❌ Error generating extension: {e}", file=sys.stderr)
        log.critical(
            {"event": "cli_failed", "source": str(spec_path), "error": str(e)}
        )
        sys.exit(1)


# -----------------------------------------------------------------------------
# Internals
# -----------------------------------------------------------------------------

def _convert_dtype(type_str: str) -> str:
    """Translate Python / JSON scalar types to NWB dtypes."""
    mapping = {
        "int": "int",
        "float": "float",
        "str": "text",
        "string": "text",
        "bool": "bool",
    }
    try:
        return mapping[type_str.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported field type for NWB spec: {type_str}") from exc 