"""This extension generates the requestctl tool."""

from argparse import ArgumentParser, Namespace
from typing import Any
import logging
import sys


from .cli import Requestctl, SCOPE_TO_ENTITY
from .error import RequestctlError
from .schema import SCHEMA, SYNC_ENTITIES

# public api
from .schema import get_schema  # noqa: F401


def strictly_positive_int(value: Any) -> int:
    """Check if the value is a strictly positive integer."""
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise ValueError
    except ValueError:
        raise ValueError(f"{value} is not a strictly positive integer")
    return ivalue


def parse_args(args) -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(
        "requestctl",
        description="Tool to control/ratelimit/ban web requests dynamically",
    )
    parser.add_argument(
        "--config", "-c", help="Configuration file", default="/etc/conftool/config.yaml"
    )
    parser.add_argument("--debug", action="store_true")
    command = parser.add_subparsers(help="Command to execute", dest="command")
    command.required = True
    # Apply command. Modifies or creates an object in the datastore
    # Example: requesctl apply action cache-text/block_cloud -f action.yaml
    apply = command.add_parser("apply", help="Apply an object definition to the datastore.")
    apply.add_argument("object_type", help="What object type to apply", choices=SYNC_ENTITIES)
    apply.add_argument(
        "object_path",
        help="The full name of the object, including tags, e.g. cache-text/block_cloud",
    )
    apply.add_argument(
        "-f", "--file", help="The relative path of file to read the object from", required=True
    )
    apply.add_argument(
        "--interactive", "-i", help="Interactively apply objects if needed.", action="store_true"
    )
    # Delete command. Deletes an object from the datastore
    # Example: requestctl delete action cache-text/block_cloud
    delete = command.add_parser("delete", help="Delete an object from the datastore.")
    delete.add_argument("object_type", help="What object type to delete", choices=SYNC_ENTITIES)
    delete.add_argument(
        "object_path",
        help="The full name of the object, including tags, e.g. cache-text/block_cloud",
    )
    delete.add_argument(
        "--interactive", "-i", help="Interactively delete objects if needed.", action="store_true"
    )
    # Load command
    # Loads multiple objects from files in the format of requestctl dump's output
    # into the datastore. Can be used to load a single file or a directory of files,
    # with the --tree flag. In that case, it will expect files to be organized in a filesyste
    # tree structure, with the object type as the first directory, and the object tags and names
    # below that, so the same format as the git tree created by conftool2git.
    # Example: requestctl load -f /path/to/dump.yaml
    # Example: requestctl load --tree -f /path/to/dumps/dir
    load = command.add_parser("load", help="Load objects from a dump file into the datastore.")
    load.add_argument(
        "--interactive",
        "-i",
        help="Interactively sync objects if needed.",
        action="store_true",
    )
    load.add_argument(
        "--reset",
        action="store_true",
        help="Delete all non-derived objects before loading. DANGER: This action is irreversible.",
    ),
    file_or_tree = load.add_mutually_exclusive_group(required=True)
    file_or_tree.add_argument("-f", "--file", help="The file to load objects from")
    file_or_tree.add_argument("-t", "--tree", help="Load objects from a directory tree")

    # Dump command. Dumps the datastore to a file that can be used with load.
    dump = command.add_parser(
        "dump",
        help="Dumps the content of the datastore to a format that can be used by load.",
    )
    dump.add_argument("-f", "--file", help="The file to write the dump to", required=True)

    # Enable command. Enables a request action.
    enable = command.add_parser("enable", help="Turns on a specific action")
    enable.add_argument(
        "--scope",
        "-s",
        help="What system to search the action for",
        choices=SCOPE_TO_ENTITY.keys(),
        default="varnish",
    )
    enable.add_argument("action", help="Action to enable")
    # Disable command. Disables a request action
    disable = command.add_parser("disable", help="Turns off a specific action")
    disable.add_argument(
        "--scope",
        "-s",
        help="What object type to disable",
        choices=SCOPE_TO_ENTITY.keys(),
        default="varnish",
    )
    disable.add_argument("action", help="Action to enable")
    # Commit command. Actually compiles the enabled actions to VCL.
    commit = command.add_parser("commit", help="Actually write your changes to the edges.")
    commit.add_argument(
        "--batch",
        "-b",
        help="Does not ask for confirmation before committing",
        action="store_true",
    )
    # Get command
    # Gets either all or one specific object from the datastore, outputs in various formats
    # Examples:
    # requestctl get action
    # requestctl get action cache-text/block_cloud
    # requestctl get action cache-text/block_cloud -o yaml
    get = command.add_parser("get", help="Get an object")
    get.add_argument("object_type", help="What objects to get", choices=SCHEMA.keys())
    get.add_argument("object_path", help="The full name of the object", nargs="?", default="")
    get.add_argument(
        "-o",
        "--output",
        help="Choose the format for output: pretty, json, yaml. "
        "Pretty output is disabled for actions at the moment.",
        choices=["pretty", "json", "yaml"],
        default="pretty",
    )
    # Log command. Outputs a typical varnishncsa command to log the selected action
    log = command.add_parser("log", help="Get the varnishncsa to log requests matching an object.")
    log.add_argument(
        "object_path",
        help="The full name of the object",
    )
    # vcl command. Outputs the VCL for the selected action.
    vcl = command.add_parser(
        "vcl", help="Get the varnish VCL that will be generated by this action."
    )
    vcl.add_argument(
        "object_path",
        help="The full name of the object",
    )
    # haproxycfg command. Outputs the haproxy configuration for the selected action.
    haproxycfg = command.add_parser(
        "haproxycfg",
        help="Get the haproxy configuration that will be generated by this haproxy_action.",
    )
    haproxycfg.add_argument(
        "object_path",
        help="The full name of the object",
    )
    # find command. Returns the actions that include a specific pattern/ipblock
    find = command.add_parser("find", help="Find which actions include a specific pattern/ipblock")
    # Scope is none by default, as we might want to search both varnish and haproxy actions.
    find.add_argument(
        "--scope",
        "-s",
        help="What system to search the action for",
        choices=SCOPE_TO_ENTITY.keys(),
    )
    find.add_argument(
        "search_string",
        help="The string to search in the expression. Must be in the format <scope>/<name>."
        "No regex matching or partial string match is performed.",
    )
    # find-ip command. Returns all the ipblocks and IP belongs to, if any
    find_ip = command.add_parser(
        "find-ip",
        help="Find if an IP is part of any CIDR of any ipblock definitions on disk.",
    )
    find_ip.add_argument(
        "ip",
        help="The IP address to search for.",
    )
    # upgrade-schema command. Upgrades the schema of the objects.
    upgrade_schema = command.add_parser(
        "upgrade-schema",
        help="Upgrades the schema of the objects.",
    )
    upgrade_schema.add_argument(
        "--dry-run",
        help="Do not write to the backend, just validate all objects with the new schema.",
        action="store_true",
    )
    upgrade_schema.add_argument(
        "--force",
        action="store_true",
        help="Write to the backend even if there are validation errors.",
    )
    upgrade_schema.add_argument(
        "object_type", help="What object type to upgrade", choices=SCHEMA.keys()
    )

    # Cleanup command. Cleans up the objects in the datastore.
    cleanup = command.add_parser(
        "cleanup",
        help="Cleans up the objects in the datastore.",
    )
    cleanup.add_argument(
        "--dry-run",
        help="Do not write to the backend, just validate all objects with the new schema.",
        action="store_true",
    )
    cleanup.add_argument(
        "--enabled-days",
        type=strictly_positive_int,
        help="The number of days to wait before disabling an enabled rule.",
        default=30,
    )
    cleanup.add_argument(
        "--log-matching-days",
        type=strictly_positive_int,
        help="The number of days to wait before disabling a rule that is in logging mode.",
        default=60,
    )
    cleanup.add_argument(
        "--disabled-days",
        type=strictly_positive_int,
        help="The number of days to wait before deleting a disabled rule.",
        default=180,
    )

    return parser.parse_args(args)


def main():
    """Run the tool."""
    logger = logging.getLogger("reqctl")
    options = parse_args(sys.argv[1:])
    rq = Requestctl(options)
    try:
        # TODO: add support to let a custom exit code surface, for example for
        # "failed successfully" operations
        rq.run()
    except RequestctlError as e:
        logger.error(e)
        sys.exit(1)
