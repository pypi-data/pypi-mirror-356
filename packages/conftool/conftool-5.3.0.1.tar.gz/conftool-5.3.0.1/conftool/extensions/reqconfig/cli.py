"""
This is the cli interface for the reqconfig extension.
Given the interface is very different from the other *ctl commands,
We don't necessarily derive it from the base cli tools.
"""

import argparse
import logging
import pathlib
import sys
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple

import yaml
from wmflib.interactive import AbortError, ask_confirmation

from conftool import yaml_safe_load
from conftool.cli import ConftoolClient, tool
from conftool.drivers import BackendError
from conftool.extensions.reqconfig.translate import (
    VSLTranslator,
)
from conftool.kvobject import Entity

from . import api
from . import cleanup
from . import view
from .constants import ACTION_ENTITIES
from .schema import SYNC_ENTITIES
from .error import RequestctlError

logger = logging.getLogger("reqctl")

# Mapping of commands to entities. This is used to determine the entity type
# If the list is empty, the object type will be determined from the command line.
CMD_TO_ENTITY = {
    "validate": [],
    "apply": [],
    "delete": [],
    "sync": [],
    "dump": SYNC_ENTITIES,
    "load": SYNC_ENTITIES,
    "enable": ACTION_ENTITIES,
    "disable": ACTION_ENTITIES,
    "get": [],
    "vcl": ["action"],
    "log": ["action"],
    "find": ACTION_ENTITIES,
    "find-ip": ["ipblock"],
    "commit": ACTION_ENTITIES,
    "haproxycfg": ["haproxy_action"],
    "upgrade-schema": [],
    "cleanup": ACTION_ENTITIES,
}


SCOPE_TO_ENTITY = {
    "varnish": ["action"],
    "haproxy": ["haproxy_action"],
}


def is_obj_on_fs(client: ConftoolClient, path: str) -> Callable:
    """Check if an object is on the filesystem."""

    def _is_obj_on_fs(obj_type: str, slug: str) -> bool:
        on_disk: pathlib.Path = (
            pathlib.Path(path) / client.get(obj_type).base_path() / f"{slug}.yaml"
        )
        return on_disk.is_file()

    return _is_obj_on_fs


def _remove_enabled(_, changes: Dict[str, Any]) -> Dict[str, Any]:
    """Remove the enabled state from the changes."""
    try:
        del changes["enabled"]
    except KeyError:
        pass
    return changes


class EntityResourceDefinition:
    """Encapsulates an entity definition for dump and load operations."""

    def __init__(self, entity: Entity):
        self.entity = entity

    @property
    def type(self) -> str:
        """The type of the entity."""
        return api.get_object_type_from_entity(self.entity)

    @property
    def path(self) -> str:
        """The path of the entity."""
        return self.entity.pprint()

    @property
    def entity_data(self) -> Dict[str, Any]:
        """The entity data."""
        return self.entity._to_net()

    def metadata(self) -> Dict[str, Any]:
        return {"type": self.type, "path": self.path}

    def asdict(self) -> Dict[str, Any]:
        return {"metadata": self.metadata(), "data": self.entity_data}

    @staticmethod
    def from_dict(data: Dict[str, Any], api: api.RequestctlApi) -> "EntityResourceDefinition":
        entity = api.get(data["metadata"]["type"], data["metadata"]["path"])
        if entity is not None:
            return EntityResourceDefinition(entity)
        else:
            raise RequestctlError(f"Entity {data['metadata']['type']} not found.")


class RequestctlUpgradeSchema(tool.UpgradeSchemaCli):
    """Upgrade the schema for the reqconfig extension."""

    def _client(self) -> ConftoolClient:
        return api.client(self.args.config)


class Requestctl:
    """Cli tool to interact with the dynamic banning of urls."""

    def __init__(self, args: argparse.Namespace) -> None:
        if args.debug:
            lvl = logging.DEBUG
        else:
            lvl = logging.INFO
        logging.basicConfig(
            level=lvl,
            format="%(asctime)s - %(name)s "
            "(%(module)s:%(funcName)s:%(lineno)d) - %(levelname)s - %(message)s",
        )
        self.args = args
        # Now let's load the schema
        self.client = api.client(self.args.config)

        self.schema = self.client.schema

        # Load the right entities
        self.classes = {obj: self.client.get(obj) for obj in self.object_types}
        # If we only have one entity, we can use it directly
        if len(self.classes) == 1:
            self.cls = list(self.classes.values())[0]
        else:
            self.cls = None
        if "git_repo" in self.args and self.args.git_repo is not None and self.cls is not None:
            self.base_path: Optional[pathlib.Path] = (
                pathlib.Path(self.args.git_repo) / self.cls.base_path()
            )
        else:
            self.base_path = None
        # Load the parsing grammar. If the command is validate, use on-disk check of existence for
        # patterns.
        # Otherwise, check on the datastore.
        self.api = api.RequestctlApi(self.client)
        # We never sync enabled from disk
        self.api.set_hook("validate", _remove_enabled)

    @property
    def object_types(self) -> List[str]:
        """The object type we're operating on."""
        if self.args.command not in CMD_TO_ENTITY:
            raise RequestctlError(
                f"Command {self.args.command} not listed in Requestctl.CMD_TO_ENTITY"
            )
        # If we don't have forced values for the specific command, we expect an object type
        # to be passed in the command line.
        if not CMD_TO_ENTITY[self.args.command]:
            return [self.args.object_type]

        # To make things more user-friendly, we sometimes allow selecting a "scope" of objects
        if "scope" in self.args and self.args.scope in SCOPE_TO_ENTITY:
            return SCOPE_TO_ENTITY[self.args.scope]
        # Otherwise we return the values from the mapping
        return CMD_TO_ENTITY[self.args.command]

    def run(self):
        """Runs the action defined in the cli args."""
        try:
            command = getattr(self, self.args.command.replace("-", "_"))
        except AttributeError as e:
            raise RequestctlError(f"Command {self.args.command} not implemented") from e

        # TODO: add support to let a custom exit code surface, for example for
        # "failed successfully" operations
        command()

    def apply(self):
        """Apply a change to an object.

        Raises: RequestctlError in case of errors."""
        file_path = pathlib.Path().cwd() / str(self.args.file)
        if not file_path.is_file():
            raise RequestctlError(f"File {file_path} does not exist or is not a file.")
        obj = self.api.get(self.args.object_type, self.args.object_path)
        from_disk = yaml_safe_load(file_path, {})
        with self.api.hook("write_confirmation", self._write_confirmation_hook()):
            try:
                self.api.write(obj, from_disk)
            except RequestctlError as e:
                logger.error("Error parsing %s, skipping: %s", obj.pprint(), e)
                raise
            except BackendError as e:
                logger.error("Error writing to etcd for %s: %s", obj.pprint(), e)
                raise RequestctlError("Error writing to etcd, details are in the logged error.")

    def delete(self):
        """Delete an object.

        Raises: RequestctlError in case of errors."""
        obj = self.api.get(self.args.object_type, self.args.object_path)
        with self.api.hook("delete_confirmation", self._delete_confirmation_hook()):
            try:
                self.api.delete(obj)
            except RequestctlError as e:
                logger.error("Error deleting %s: %s", obj.pprint(), e)
                raise
            except BackendError as e:
                logger.error("Error deleting %s from etcd: %s", obj.pprint(), e)
                raise RequestctlError("Error deleting from etcd, details are in the logged error.")

    def dump(self):
        """Dump an object type."""
        everything = []
        for cls in self.classes:
            objects = self.api.all(cls)
            for object in objects:
                everything.append(EntityResourceDefinition(object).asdict())
        with open(self.args.file, "w") as f:
            f.write(yaml.safe_dump_all(everything))

    def load(self):
        """Load objects from a file."""
        sync_first = set(SYNC_ENTITIES) - set(ACTION_ENTITIES)
        # If reset is given, remove all objects first, starting from actions
        # and then the rest.
        # Given we're not removing the translated objects, we can safely
        # perform this action as long as no one tries to commit() in the meantime
        if self.args.reset:
            if sys.stdout.isatty():
                print("WARNING: This will delete all non-derived objects.")
                print(
                    "ONLY use this option if you're reloading a full dump "
                    "and you know what you are doing."
                )
                ask_confirmation("Do you want to proceed?")
            for obj_type in ACTION_ENTITIES:
                for obj in self.api.all(obj_type):
                    self.api.delete(obj)
            for obj_type in sync_first:
                for obj in self.api.all(obj_type):
                    self.api.delete(obj)

        if self.args.tree:
            tree = pathlib.Path(self.args.tree)
            # We fail early if we can't load base objects like patterns or ipblocks
            # as we assume they might be used by others and cause cascading failures
            for object_type in sync_first:
                if not self._load_subtree(object_type, tree):
                    raise RequestctlError(f"Failed to load {object_type} objects from {tree}")
            for object_type in ACTION_ENTITIES:
                if not self._load_subtree(object_type, tree):
                    logger.error(f"Failed to load {object_type} objects from {tree}")
        else:
            all_objects_by_type = {}
            with open(self.args.file, "r") as f:
                for obj in yaml.safe_load_all(f):
                    entity = EntityResourceDefinition.from_dict(obj, self.api)
                    if entity.type not in all_objects_by_type:
                        all_objects_by_type[entity.type] = []
                    all_objects_by_type[entity.type].append(entity)
            for object_type in sync_first:
                if not self._load_list(all_objects_by_type.get(object_type, [])):
                    raise RequestctlError(
                        f"Failed to load {object_type} objects from {self.args.file}"
                    )
            for object_type in ACTION_ENTITIES:
                if not self._load_list(all_objects_by_type.get(object_type, [])):
                    logger.error(f"Failed to load {object_type} objects from {self.args.file}")

    def enable(self):
        """Enable an action."""
        self._enable(True)

    def disable(self):
        """Disable an action."""
        self._enable(False)

    def get(self):
        """Get an object, or an entire class of them, print them out."""
        # We should only call this when a class is selected
        if self.cls is None:
            raise RequestctlError(
                "No object type selected for getting. This is a bug, please report it."
            )
        self._pprint(self._get())

    def log(self):
        """Print out the varnishlog command corresponding to the selected action."""
        objs = self._get(must_exist=True)
        objs[0].vsl_expression = self._vsl_from_expression(objs[0].expression)
        print(view.get("vsl").render(objs, "action"))

    def find(self):
        """Find actions that correspond to the searched pattern."""
        matches = self.api.find_in_actions(self.args.search_string)
        for action in matches:
            object_type = api.get_object_type_from_entity(action)
            print(f"{object_type}: {action.pprint()}, expression: {action.expression}")
        if not matches:
            print("No entries found.")

    def find_ip(self):
        """Find if the given IP is part of any IP block on disk."""
        matches = self.api.find_in_ipblocks(self.args.ip)
        for ipblock in matches:
            print(f"IP {self.args.ip} is part of ipblock {ipblock.pprint()}")

        if not matches:
            print(f"IP {self.args.ip} is not part of any ipblock in the datastore.")

    def upgrade_schema(self):
        """Upgrade the schema to the latest version."""
        if not RequestctlUpgradeSchema(self.args).run_action(""):
            raise RequestctlError("Schema upgrade failed.")

    def cleanup(self):
        """Clean up the objects in the datastore."""
        maint = cleanup.RequestctlMaintenance(
            self.client,
            dry_run=self.args.dry_run,
            enabled_days=self.args.enabled_days,
            log_matching_days=self.args.log_matching_days,
            disabled_days=self.args.disabled_days,
        )
        maint.run()

    def vcl(self):
        """Print out the VCL for a specific action."""
        objs = self._get(must_exist=True)
        print(self.api.get_dsl_for(objs, show_disabled=True))

    def haproxycfg(self):
        """Print out the haproxy config for a specific action."""
        haproxy_actions = self._get(must_exist=True)
        print(self.api.get_dsl_for(haproxy_actions, show_disabled=True))

    def commit(self):
        """Commit the enabled actions to the DSLs, asking confirmation with a diff."""
        # All the actions that are not disabled or without log_matching, organized by
        # cluster and type
        batch: bool = self.args.batch
        if not batch:
            print("### Varnish VCL changes ###")

        self._commit_vcl(batch)
        if not batch:
            print("### HAProxy DSL changes ###")
        self._commit_haproxy(batch)

    # End public interface
    def _load_subtree(self, object_type: str, root_path: pathlib.Path) -> bool:
        """Load objects of a specific object type from a dir tree."""
        success = True
        write_hook = self._write_confirmation_hook()
        self.cls = self.client.get(object_type)
        for tag, fpath in self._get_files_for_object_type(root_path, object_type):
            obj, from_disk = self._entity_from_file(tag, fpath)
            with self.api.hook("write_confirmation", write_hook):
                try:
                    self.api.write(obj, from_disk)
                except RequestctlError as e:
                    success = False
                    logger.error("Error parsing %s, skipping: %s", obj.pprint(), e)
                except BackendError as e:
                    logger.error("Error writing to etcd for %s: %s", obj.pprint(), e)
                    success = False
        return success

    def _load_list(self, objects: List[EntityResourceDefinition]) -> bool:
        success = True
        with self.api.hook("write_confirmation", self._write_confirmation_hook()):
            for entity in objects:
                try:
                    self.api.write(entity.entity, entity.entity_data)
                except RequestctlError as e:
                    success = False
                    logger.error("Error parsing %s, skipping: %s", entity.path, e)
                except BackendError as e:
                    logger.error("Error writing to etcd for %s: %s", entity.path, e)
                    success = False
        return success

    def _commit_vcl(self, batch: bool):
        diffs = self.api.get_dsl_diffs("action")
        for cluster, entries in diffs.items():
            for name, data in entries.items():
                dsl, diff = data
                if not batch and not self._confirm_diff(diff):
                    continue
                dsl_obj = self.client.get("vcl")(cluster, name)
                # If the dsl is empty, we need to nullify the vcl
                if not dsl:
                    if dsl_obj.exists:
                        dsl_obj.vcl = ""
                        dsl_obj.write()
                else:
                    # If the dsl is not empty, we need to write it
                    dsl_obj.vcl = dsl
                    dsl_obj.write()

    def _commit_haproxy(self, batch: bool):
        diffs = self.api.get_dsl_diffs("haproxy_action")
        for cluster, entries in diffs.items():
            for name, data in entries.items():
                dsl, diff = data
                if not batch and not self._confirm_diff(diff):
                    continue
                dsl_obj = self.client.get("haproxy_dsl")(cluster, name)
                # If the dsl is empty, we need to remove the dsl. However,
                # in the case of HAProxy, we need to remove the object alltogether
                # so that the fallback global configuration will be picked up
                # instead.
                if not dsl:
                    if dsl_obj.exists:
                        dsl_obj.delete()
                else:
                    # If the dsl is not empty, we need to write it
                    dsl_obj.dsl = dsl
                    dsl_obj.write()

    def _get_files_for_object_type(
        self, root_path: pathlib.Path, obj_type: str
    ) -> Generator[Tuple[str, pathlib.Path], None, None]:
        """Gets files in a directory that can contain objects."""
        entity_path: pathlib.Path = root_path / self.client.get(obj_type).base_path()
        if not pathlib.Path.exists(entity_path):
            return None
        for tag_path in entity_path.iterdir():
            # skip files in the root dir, including any hidden dirs and the special
            # .. and . references
            if not tag_path.is_dir() or tag_path.parts[-1].startswith("."):
                continue
            tag = tag_path.name
            for fpath in tag_path.glob("*.yaml"):
                yield (tag, fpath)

    def _confirm_diff(self, diff: str) -> bool:
        """Confirm if a change needs to be carried on or not."""
        if not diff:
            return False
        print(diff)
        try:
            ask_confirmation("Ok to commit these changes?")
        except AbortError:
            return False
        return True

    def _get(self, must_exist: bool = False) -> List[Entity]:
        """Get an object, or all of them, return them as a list."""
        objs = []
        has_path = "object_path" in self.args and self.args.object_path

        for cls in self.classes:
            if has_path:
                obj = self.api.get(cls, self.args.object_path)
                if obj.exists:
                    objs.append(obj)
            else:
                objs.extend(self.api.all(cls))
        if must_exist and has_path and not objs:
            raise RequestctlError(
                f"{list(self.classes.keys())} '{self.args.object_path}' not found."
            )

        return objs

    def _enable(self, enable: bool):
        """Ban a type of request."""
        for cls in self.classes:
            obj = self.api.get(cls, self.args.action)
            if obj is not None and obj.exists:
                # we need to remove the validation hook for this operation
                with self.api.hook("validate", lambda _, x: x):
                    self.api.update(cls, self.args.action, {"enabled": enable})
            else:
                continue

            # Printing this unconditionally *might* be confusing, as there's nothing to commit if
            # enabling an already-enabled action. So we could check first, with action.changed(),
            # but it probably isn't worth the extra roundtrip.
            print("Remember to commit the change with: sudo requestctl commit")
            return

        # If we got here, the action was not found.
        raise RequestctlError(f"{self.args.action} does not exist, cannot enable/disable.")

    def _pprint(self, entities: List[Entity]):
        """Pretty print the results."""
        # VCL and VSL output modes are only supported for "action"
        # Also, pretty mode is disabled for all but patterns and ipblocks.
        # Actions should be supported, but is temporarily disabled
        #  while we iron out the issues with old versions of tabulate
        output_config = {
            "action": {"allowed": ["vsl", "vcl", "yaml", "json"], "default": "yaml"},
            "haproxy_action": {"allowed": ["yaml", "json", "haproxycfg"], "default": "json"},
            "vcl": {"allowed": ["yaml", "json"], "default": "json"},
            "haproxy_dsl": {"allowed": ["yaml", "json"], "default": "json"},
        }
        # We need output and object type to determine the output format
        if not all([self.args.output, self.args.object_type]):
            raise RequestctlError("Cannot use pprint without output and object type.")
        out = self.args.output
        object_type = self.args.object_type
        if object_type in output_config:
            conf = output_config[object_type]
            if out not in conf["allowed"]:
                out = conf["default"]
        print(view.get(out).render(entities, object_type))

    def _entity_from_file(self, tag: str, file_path: pathlib.Path) -> Tuple[Entity, Optional[Dict]]:
        """Get an entity from a file path, and the corresponding data to update."""
        from_disk = yaml_safe_load(file_path, {})
        entity_name = file_path.stem
        if self.cls is None:
            raise RequestctlError(
                "No entity selected when trying to load from disk."
                "Please ensure self.cls is set before calling this method."
                "This is a bug in the code. If you see this message, please report it."
            )
        entity = self.cls(tag, entity_name)
        return (entity, from_disk)

    def _write_confirmation_hook(self) -> Callable:
        def _object_diff(entity: Entity, to_load: Dict[str, Any]) -> bool:
            """Asks for confirmation of changes if needed."""
            # find the object type from the entity
            obj_type = api.get_object_type_from_entity(entity).capitalize()
            if entity.exists:
                changes = entity.changed(to_load)
                action = "modify"
                msg = f"{obj_type} {entity.pprint()} will be changed:"
            else:
                action = "create"
                changes = to_load
                msg = f"{obj_type} will be created:"
            # If there is no changes, we bail out early
            if not changes:
                return False

            if self.args.interactive:
                print(msg)
                for key, value in changes.items():
                    print(f"{entity.name}.{key}: '{getattr(entity, key)}' => {value}")
                try:
                    ask_confirmation(f"Do you want to {action} this object?")
                except AbortError:
                    return False
            return True

        return _object_diff

    def _delete_confirmation_hook(self) -> Callable:
        def _delete_confirmation(entity: Entity) -> bool:
            """Ask for confirmation before deleting an object."""
            if self.args.interactive:
                try:
                    ask_confirmation(f"Proceed to delete {entity.pprint()}?")
                except AbortError:
                    return False
            return True

        return _delete_confirmation

    def _vsl_from_expression(self, expression: str) -> str:
        parsed = self.api.expression_processor.parse_as_list(expression)
        vsl = VSLTranslator(self.client.schema)
        return vsl.from_expression(parsed)
