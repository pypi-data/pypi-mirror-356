from typing import Dict

from conftool import configuration
from conftool.cli import ConftoolClient
from conftool.kvobject import Entity
from conftool.loader import Schema

from .error import RequestctlError

# requestctl has its own schema and we don't want to have to configure it.
empty_string = {"type": "string", "default": ""}
empty_list = {"type": "list", "default": []}
empty_cidr_list = {"type": "cidr_list", "default": []}
bool_false = {"type": "bool", "default": False}
SCHEMA: Dict = {
    "ipblock": {
        "path": "request-ipblocks",
        "tags": ["scope"],
        "schema": {
            "cidrs": empty_cidr_list,
            "comment": empty_string,
        },
    },
    "pattern": {
        "path": "request-patterns",
        "tags": ["scope"],
        "schema": {
            "method": empty_string,
            "request_body": empty_string,
            "url_path": empty_string,
            "header": empty_string,
            "header_value": empty_string,
            "header_is_set": bool_false,
            "query_parameter": empty_string,
            "query_parameter_value": empty_string,
        },
    },
    "action": {
        "path": "request-actions",
        "tags": ["cluster"],
        "schema": {
            "enabled": bool_false,
            "priority": {
                "type": "int",
                "default": 100,
                "docstring": ("lower number means higher priority, 0-255, 0 is highest priority"),
            },
            "last_modified": {
                "type": "int",
                "default": 0,
                "docstring": "last modified time in epoch seconds",
            },
            "created": {
                "type": "int",
                "default": 0,
                "docstring": "created time in epoch seconds",
            },
            "keep": {
                **bool_false,
                "docstring": (
                    "If true, this rule will not be deleted by the cleanup process."
                    " This is useful for rules that are not used but should be kept"
                    " for reference."
                ),
            },
            "cache_miss_only": {
                **bool_false,
                "default": True,
                "docstring": "If you can enable this, please do so",
            },
            "comment": empty_string,
            "expression": empty_string,
            "resp_status": {"type": "int", "default": 429},
            "resp_reason": {**empty_string, "example": "Too Many Requests"},
            "sites": empty_list,
            "do_throttle": bool_false,
            "throttle_requests": {
                "type": "int",
                "default": 500,
                "docstring": "number of requests allowed in the throttle_interval",
            },
            "throttle_interval": {
                "type": "int",
                "default": 30,
                "docstring": "token-bucket interval, in seconds",
            },
            "throttle_duration": {
                "type": "int",
                "default": 1000,
                "docstring": (
                    "Optional (can be 0) number of seconds to continue denying requests"
                    " after throttle_requests is reached, but after throttle_interval"
                    " has elapsed"
                ),
            },
            "throttle_per_ip": {
                **bool_false,
                "docstring": "If false, one token bucket per CDN server",
            },
            "log_matching": bool_false,
        },
    },
    "vcl": {
        "path": "request-vcl",
        "tags": ["cluster"],
        "schema": {
            "vcl": empty_string,
        },
    },
    "haproxy_action": {
        "path": "request-haproxy-actions",
        "tags": ["cluster"],
        "schema": {
            "enabled": bool_false,
            "comment": empty_string,
            "priority": {
                "type": "int",
                "default": 100,
                "docstring": ("lower number means higher priority, 0-255, 0 is highest priority"),
            },
            "last_modified": {
                "type": "int",
                "default": 0,
                "docstring": "last modified time in epoch seconds",
            },
            "created": {
                "type": "int",
                "default": 0,
                "docstring": "created time in epoch seconds",
            },
            "keep": {
                **bool_false,
                "docstring": (
                    "If true, this rule will not be deleted by the cleanup process."
                    " This is useful for rules that are not used but should be kept"
                    " for reference."
                ),
            },
            "expression": empty_string,
            "resp_status": {"type": "int", "default": 429},
            "resp_reason": empty_string,
            "sites": empty_list,
            "silent_drop": bool_false,
            "bw_throttle": bool_false,
            "bw_throttle_rate": {"type": "int", "default": 100000},
            "bw_throttle_duration": {"type": "int", "default": 1000},
            "per_ip_concurrency": bool_false,
            "per_ip_concurrency_limit": {"type": "int", "default": 50},
            "per_ip_concurrency_counter_index": {"type": "int", "default": -1, "hidden": True},
            "log_matching": bool_false,
        },
    },
    "haproxy_dsl": {
        "path": "request-haproxy-dsl",
        "tags": ["cluster"],
        "schema": {
            "dsl": empty_string,
        },
    },
}
SYNC_ENTITIES = sorted(set(SCHEMA.keys()) - {"vcl", "haproxy_dsl"})


def get_schema(conf: configuration.Config) -> Schema:
    """Get the schema for requestctl."""
    return ConftoolClient(config=conf, schema=SCHEMA, irc_logging=False).schema


def get_obj_from_slug(entity: Entity, slug: str) -> Entity:
    """Get an object given a string slug."""
    try:
        tag, name = slug.split("/")
    except ValueError as e:
        raise RequestctlError(f"{slug} doesn't contain a path separator") from e
    return entity(tag, name)
