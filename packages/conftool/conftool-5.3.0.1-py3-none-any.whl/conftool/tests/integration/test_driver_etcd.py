from unittest import mock

import etcd

from conftool import drivers
from conftool.drivers.etcd import Driver
from conftool.tests.integration import IntegrationTestBase
from conftool.kvobject import KVObject


class EtcdDriverTest(IntegrationTestBase):

    def setUp(self):
        super().setUp()
        self.driver: Driver = KVObject.backend.driver
        self.client: etcd.Client = self.driver.client

    def client_write(self, key: str, value: str, **kwargs):
        self.client.write(self.driver.abspath(key), value, **kwargs)

    def test_is_dir(self):
        self.client_write("a/key", "{}")
        # A key that does not exist returns false.
        self.assertFalse(self.driver.is_dir("nope"))
        # A key that corresponds to a directory returns true.
        self.assertTrue(self.driver.is_dir("a"))
        # A key that corresponds to a node returns false.
        self.assertFalse(self.driver.is_dir("a/key"))

    def test_all_keys(self):
        # Build a hierarchy of KV pairs.
        self.client_write("a/key", '{"value": 1}')
        self.client_write("a/b/key", '{"value": 2}')
        self.client_write("a/b/c/key", '{"value": 3}')
        # Add an empty leaf directory.
        self.client_write("a/b/c/d", None, dir=True)
        # An all_keys on the root of the above hierarchy returns all
        # non-directory leaf key-segment lists.
        self.assertCountEqual(
            self.driver.all_keys("a"),
            [
                ["key"],
                ["b", "key"],
                ["b", "c", "key"],
            ],
        )

    def test_all_keys_returns_empty_on_non_directory(self):
        # An all_keys on a non-directory returns an empty list.
        # TODO: Should this raise ValueError?
        self.client_write("a/key", "{}")
        self.assertEqual(self.driver.all_keys("a/key"), [])

    def test_all_keys_fails_on_non_existent_key(self):
        # An all_keys on a non-existent key raises ValueError.
        # TODO: Should this raise NotFoundError?
        with self.assertRaises(ValueError):
            self.driver.all_keys("nope")

    def test_all_data(self):
        # Build a hierarchy of KV pairs.
        self.client_write("a/key", '{"value": 1}')
        self.client_write("a/b/key", '{"value": 2}')
        self.client_write("a/b/c/key", '{"value": 3}')
        # Add an empty leaf directory.
        self.client_write("a/b/c/d", None, dir=True)
        # An all_data on the root of the above hierarchy returns key value pairs
        # for all non-directory leaves.
        self.assertCountEqual(
            self.driver.all_data("a"),
            [
                ("key", {"value": 1}),
                ("b/key", {"value": 2}),
                ("b/c/key", {"value": 3}),
            ],
        )

    def test_all_data_returns_empty_on_non_directory(self):
        # An all_data on a non-directory returns an empty list.
        # TODO: Should this raise ValueError?
        self.client_write("a/key", "{}")
        self.assertEqual(self.driver.all_data("a/key"), [])

    def test_all_data_fails_on_non_existent_key(self):
        # An all_data on a non-existent key raises ValueError.
        # TODO: Should this raise NotFoundError?
        with self.assertRaises(ValueError):
            self.driver.all_data("nope")

    def test_all_data_fails_on_malformed_data(self):
        # An all_data on a path containing malformed data raises BackendError.
        self.client_write("a/key", "definitely not json")
        with self.assertRaises(drivers.BackendError):
            self.driver.all_data("a")

    def test_write_and_read(self):
        # A write initially returns None, as the key does not yet exist.
        self.assertIsNone(self.driver.write("a/key", {"x": 1}))
        # A read returns the expected value.
        self.assertEqual(self.driver.read("a/key").data, {"x": 1})
        # A subsequent write will update the stored object.
        self.assertEqual(self.driver.write("a/key", {"y": 2}).data, {"x": 1, "y": 2})
        # ... and a read will see the expected updated valued as well.
        self.assertEqual(self.driver.read("a/key").data, {"x": 1, "y": 2})

    def test_read_returns_none_on_directory(self):
        # A read on a directory returns None.
        # TODO: Should this raise ValueError?
        self.client_write("a", None, dir=True)
        self.assertIsNone(self.driver.read("a"))

    def test_read_fails_on_non_existent_key(self):
        # A read for a non-existent key raises NotFoundError.
        with self.assertRaises(drivers.NotFoundError):
            self.driver.read("nope")

    def test_read_fails_on_malformed_data(self):
        # A read raises BackendError if the value is malformed.
        self.client_write("a/key", "definitely not json")
        with self.assertRaises(drivers.BackendError):
            self.driver.read("a/key")

    def test_write_fails_on_malformed_data(self):
        # An update-write (key exists) leaks JSONDecodeError if the existing
        # value is malformed (which we detect here via ValueError).
        # TODO: Should this raise BackendError?
        self.client_write("a/key", "definitely not json")
        with self.assertRaises(ValueError):
            self.driver.write("a/key", {})

    def test_write_fails_on_directory(self):
        # A write on a directory leaks TypeError.
        # TODO: Should this raise ValueError?
        self.client_write("a", None, dir=True)
        with self.assertRaises(TypeError):
            self.driver.write("a", {})

    def test_write_fails_on_non_writable_path(self):
        # A write on a non-writable path (traverses b, which is a node) raises
        # BackendError.
        self.client_write("a/b", "{}")
        with self.assertRaises(drivers.BackendError):
            self.driver.write("a/b/key", {})

    def test_write_fails_on_conflict(self):
        # A write raises BackendError when it encounters a write conflict.
        read = etcd.Client.read

        def read_with_confict(key, **kwdargs):
            try:
                return read(self.client, key, **kwdargs)
            finally:
                # Make a write to the same key that interleaves between the
                # read and subsequent write. The value written is arbitrary.
                self.client.write(key, "{}")

        with mock.patch("etcd.Client.read", wraps=read_with_confict):
            # A write to a non-existent key is atomic, raising BackendError on
            # conflict.
            with self.assertRaises(drivers.BackendError):
                self.driver.write("a/key", {"value": 1})
            # A write to an existing key is atomic, raising BackendError on
            # conflict. Note the key exists due to the previouse conflicting
            # write.
            with self.assertRaises(drivers.BackendError):
                self.driver.write("a/key", {"value": 2})

    def test_delete(self):
        self.client_write("a/key", "{}")
        self.driver.delete("a/key")
        # Confirm that the key is gone.
        with self.assertRaises(etcd.EtcdKeyNotFound):
            self.client.read(self.driver.abspath("a/key"))

    def test_delete_fails_on_non_existent_key(self):
        # A delete on a non-existent key raises BackendError.
        # TODO: Should this raise NotFoundError?
        with self.assertRaises(drivers.BackendError):
            self.driver.delete("nope")

    def test_delete_fails_on_directory(self):
        # A delete on a directory raises BackendError.
        # TODO: Should this raise ValueError?
        self.client_write("a", None, dir=True)
        with self.assertRaises(drivers.BackendError):
            self.driver.delete("a")

    def test_ls(self):
        def extract_kv_data(listing):
            return [(k, v if v is None else v.data) for k, v in listing]

        # Build a hierarchy of KV pairs.
        self.client_write("a/key", '{"value": 1}')
        self.client_write("a/b/key", '{"value": 2}')
        self.client_write("a/b/c/key", '{"value": 3}')
        # An ls on each level of the hierarchy should return only the immediate
        # children, including child directories.
        self.assertCountEqual(
            extract_kv_data(self.driver.ls("a")),
            [
                ("key", {"value": 1}),
                ("b", None),
            ],
        )
        self.assertCountEqual(
            extract_kv_data(self.driver.ls("a/b")),
            [
                ("key", {"value": 2}),
                ("c", None),
            ],
        )
        self.assertEqual(
            extract_kv_data(self.driver.ls("a/b/c")),
            [
                ("key", {"value": 3}),
            ],
        )

    def test_ls_returns_empty_on_empty_directory(self):
        # An ls on an empty directory returns an empty list.
        self.client_write("a", None, dir=True)
        self.assertEqual(self.driver.ls("a"), [])

    def test_ls_returns_empty_on_non_directory(self):
        # An ls on a non-directory returns an empty list.
        # TODO: Should this raise ValueError?
        self.client_write("a/key", "{}")
        self.assertEqual(self.driver.ls("a/key"), [])

    def test_ls_fails_on_non_existent_key(self):
        # An ls on a non-existent key raises ValueError.
        # TODO: Should this raise NotFoundError?
        with self.assertRaises(ValueError):
            self.driver.ls("nope")

    def test_ls_fails_on_malformed_data(self):
        # An ls on a path containing malformed data raises BackendError.
        self.client_write("a/key", "definitely not json")
        with self.assertRaises(drivers.BackendError):
            self.driver.ls("a")
