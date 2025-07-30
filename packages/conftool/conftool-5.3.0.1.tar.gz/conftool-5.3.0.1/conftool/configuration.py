import collections
from typing import List

from conftool import yaml_safe_load


class ConfigurationError(Exception):
    """Exception raised when we fail to load the configuration."""


def get(configfile: str) -> "Config":
    """
    Loads the config from file
    """
    try:
        config = yaml_safe_load(configfile, default={})
        return Config(**config)
    except Exception as exc:
        raise ConfigurationError(exc) from exc


ConfigBase = collections.namedtuple(  # type: ignore
    "Config",
    [
        "driver",
        "hosts",
        "namespace",
        "api_version",
        "pools_path",
        "driver_options",
        "tcpircbot_host",
        "tcpircbot_port",
        "cache_path",
        "read_only",
        "conftool2git_address",
        "extensions_config",
    ],
)


class ReqConfiguration:
    """Container for configuration of requestctl"""

    def __init__(self, **kwargs) -> None:
        if "haproxy_path" in kwargs:
            self.haproxy_path = kwargs["haproxy_path"]
        else:
            self.haproxy_path = "/etc/haproxy/"

        self.haproxy_reserved_slots: List[int] = kwargs.get("haproxy_reserved_slots", [0])
        self.haproxy_concurrency_slots: int = kwargs.get("haproxy_concurrency_slots", 10)
        self.haproxy_ring_name: str = kwargs.get("haproxy_ring_name", "reqctl-ring")
        self.varnish_acl_ipblocks: List[str] = kwargs.get("varnish_acl_ipblocks", ["abuse"])


class DbCtlConfiguration:
    """Container for configuration for dbctl."""

    def __init__(self, **kwargs) -> None:
        self.parsercache_min_pooled_sections: int = kwargs.get("parsercache_min_pooled_sections", 2)


class ExtensionsConfig:
    """Container for configuration of extensions"""

    def __init__(self, **kwargs) -> None:
        self.reqconfig = ReqConfiguration(**kwargs.get("reqconfig", {}))
        self.dbctlconfig = DbCtlConfiguration(**kwargs.get("dbctlconfig", {}))


class Config(ConfigBase):
    def __new__(
        cls,
        driver="etcd",
        hosts=["http://localhost:2379"],
        namespace="/conftool",
        api_version="v1",
        pools_path="pools",
        driver_options={},
        tcpircbot_host="",
        tcpircbot_port=0,
        cache_path="/var/cache/conftool",
        read_only=False,
        conftool2git_address="",
        extensions_config={},
    ):
        if pools_path.startswith("/"):
            raise ValueError("pools_path must be a relative path.")

        return super().__new__(
            cls,
            driver=driver,
            hosts=hosts,
            namespace=namespace,
            api_version=api_version,
            pools_path=pools_path,
            driver_options=driver_options,
            tcpircbot_host=tcpircbot_host,
            tcpircbot_port=int(tcpircbot_port),
            cache_path=cache_path,
            read_only=read_only,
            conftool2git_address=conftool2git_address,
            extensions_config=ExtensionsConfig(**extensions_config),
        )

    def requestctl(self) -> ReqConfiguration:
        """Get the configuration for requestctl."""
        return self.extensions_config.reqconfig

    def dbctl(self) -> DbCtlConfiguration:
        """Get the configuration for dbctl."""
        return self.extensions_config.dbctlconfig
