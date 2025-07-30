"""

This driver will look at the following config files:

* /etc/etcd/etcdrc

* ~/.etcdrc

* what specified in the conftool configuration as driver_options =>
  etcd_config_file or /etc/conftool/etcdrc

read them as YAML files, and then pass every config switch found in there
to python-etcd.
"""

import json
import os

import etcd
import urllib3

from typing import Dict, List, Optional, Tuple

from conftool import configuration, drivers, yaml_safe_load, _log


def get_config(configfile):
    """Load the etcd configuration from the specified file, or from the default locations"""
    conf = {}
    # Find the home of the user we're sudoing as - if any.
    # By default, expanduser checks the HOME variable, which is not overwritten by sudo
    # if env_keep += HOME is set. So sudo confctl would end up reading the config files of the user
    # executing sudo and not those of the user it was sudoing to.
    run_as = os.environ.get("USER", "")
    user_home = os.path.expanduser("~{}".format(run_as))
    configfiles = ["/etc/etcd/etcdrc", os.path.join(user_home, ".etcdrc")]
    if configfile:
        configfiles.append(configfile)

    loaded_any = False
    for filename in configfiles:
        if os.path.exists(filename):
            conf.update(yaml_safe_load(filename, default={}))
            loaded_any = True
        else:
            _log.debug("Skipping nonexistent etcd config file: %s", filename)
    if not loaded_any:
        _log.warning("Could not load any etcd config out of %s", configfiles)
    return conf


class Driver(drivers.BaseDriver):
    """Driver for etcd v2"""

    def __init__(self, config: configuration.Config) -> None:
        super().__init__(config)
        configfile = config.driver_options.get("etcd_config_file", "/etc/conftool/etcdrc")
        driver_config = get_config(configfile)
        try:
            if config.driver_options.get("suppress_san_warnings", True):
                urllib3.disable_warnings(category=urllib3.exceptions.SubjectAltNameWarning)
        except AttributeError:
            _log.warning(
                "You are using a modern version of urllib3; "
                "please set suppress_san_warnings to false in your driver configuration."
            )

        self.client = etcd.Client(**driver_config)
        self._actor = None

    @drivers.wrap_exception(etcd.EtcdException)
    def is_dir(self, path: str) -> bool:
        p = self.abspath(path)
        try:
            res = self.client.read(p)
            return res.dir
        except etcd.EtcdKeyNotFound:
            return False

    @drivers.wrap_exception(etcd.EtcdException)
    def read(self, path: str) -> Optional[drivers.ObjectWireRepresentation]:
        key = self.abspath(path)
        res = self._fetch(key)
        return self._data(res)

    @drivers.wrap_exception(etcd.EtcdException)
    def write(self, path: str, value: Dict) -> Optional[drivers.ObjectWireRepresentation]:
        key = self.abspath(path)
        try:
            res = self._fetch(key, quorum=True)
        except drivers.NotFoundError:
            val = json.dumps(value)
            self.client.write(key, val, prevExist=False)
            return None
        try:
            old_value = json.loads(res.value)
        except json.JSONDecodeError as exc:
            raise drivers.BackendError(
                f"The kvstore contains malformed data at key {res.key}"
            ) from exc
        old_value.update(value)
        res.value = json.dumps(old_value)
        return self._data(self.client.update(res))

    def ls(self, path: str) -> List[Tuple[str, Optional[drivers.ObjectWireRepresentation]]]:
        objects = self._ls(path, recursive=False)
        fullpath = self.abspath(path) + "/"
        return [(el.key.replace(fullpath, ""), self._data(el)) for el in objects]

    def all_keys(self, path: str) -> List[List[str]]:
        # The full path we're searching in
        base_path = self.abspath(path) + "/"

        def split_path(p):
            """Strip the root path and normalize elements"""
            r = p.replace(base_path, "").replace("//", "/")
            return r.split("/")

        return [split_path(el.key) for el in self._ls(path, recursive=True) if not el.dir]

    def all_data(self, path: str) -> List[Tuple[str, drivers.ObjectWireRepresentation]]:
        base_path = self.abspath(path) + "/"
        return [
            (obj.key.replace(base_path, ""), self._data(obj).data)
            for obj in self._ls(path, recursive=True)
            if not obj.dir
        ]

    @property
    def actor(self) -> str:
        if self._actor is None:
            self._actor = self._get_actor()
        return self._actor

    def _get_actor(self) -> str:
        """Return the username of the actor"""
        # The username used to authenticate to the kv-store will be used as
        # fallback if the action has been performed as root.
        credentials = (
            self.client.username if self.client.username is not None else "unauthenticated"
        )
        actor = os.getenv("USER")
        if actor == "root":
            if os.getenv("SUDO_USER") in (None, "root"):
                return credentials
            return os.getenv("SUDO_USER")
        elif actor is None:
            return credentials
        return actor

    @drivers.wrap_exception(etcd.EtcdException)
    def _ls(self, path: str, recursive: bool) -> List[etcd.EtcdResult]:
        key = self.abspath(path)
        try:
            res = self.client.read(key, recursive=recursive)
        except etcd.EtcdException:
            raise ValueError("{} is not a directory".format(key))
        return [el for el in res.leaves if el.key != key]

    @drivers.wrap_exception(etcd.EtcdException)
    def delete(self, path: str) -> None:
        key = self.abspath(path)
        self.client.delete(key)

    def _fetch(self, key: str, **kwdargs) -> etcd.EtcdResult:
        try:
            return self.client.read(key, **kwdargs)
        except etcd.EtcdKeyNotFound:
            raise drivers.NotFoundError()

    def _data(
        self, etcdresult: Optional[etcd.EtcdResult]
    ) -> Optional[drivers.ObjectWireRepresentation]:
        if etcdresult is None or etcdresult.dir:
            return None
        try:
            metadata = drivers.ObjectWireMetadata(etcdresult.modifiedIndex)
            return drivers.ObjectWireRepresentation(json.loads(etcdresult.value), metadata)
        except json.JSONDecodeError as exc:
            raise drivers.BackendError(
                f"The kvstore contains malformed data at key {etcdresult.key}"
            ) from exc
