"""Integration tests for conftool2git."""

import asyncio
import logging
import os
import pathlib
import shutil
import sys
import tempfile
import time

import pygit2

import pytest
import yaml

from conftool.extensions import reqconfig
from conftool.cli import conftool2git

from conftool.tests.integration import IntegrationTestBase

# For the sake of simplicity, we will do an initial
# sync of the data of requestctl step0 data
fixtures_base = os.path.realpath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, "fixtures", "reqconfig")
)
STEP0_PATH = os.path.join(fixtures_base, "step0")


@pytest.mark.skipif(sys.version_info < (3, 11), reason="async tests require python 3.11")
class TestConftool2Git(IntegrationTestBase):
    """Integration tests for conftool2git."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.schema = reqconfig.get_schema(cls.get_config())

    @staticmethod
    def requestctl(args):
        """Run requestctl with the given arguments."""
        args = reqconfig.parse_args(args)
        return reqconfig.cli.Requestctl(args).run()

    def setUp(self):
        super().setUp()
        # Run sync.
        self.requestctl(["load", "--tree", STEP0_PATH])
        self.base_path = tempfile.mkdtemp()
        self.repo_path = self.base_path + "/repo"
        os.makedirs(self.repo_path)
        self.repo = pygit2.init_repository(self.repo_path, False)
        if sys.version_info >= (3, 11):
            queue = asyncio.Queue()
            self.log_handler = conftool2git.AuditLogHandler(self.repo_path, queue, False)
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        super().tearDown()
        self.repo.free()
        shutil.rmtree(self.base_path)

    def test_first_sync(self):
        """Test that the initial sync works."""
        asyncio.run(self.log_handler.startup_sync())
        repo = pathlib.Path(self.repo_path)
        action = repo / "request-actions" / "cache-text" / "bad_param_q.yaml"
        assert action.is_file()
        with action.open() as f:
            action = yaml.safe_load(f)
        assert action["enabled"] is False
        assert action["do_throttle"] is True

    def test_sync_element_modified(self):
        """Test that elements modified are reproduced in a sync."""
        asyncio.run(self.log_handler.startup_sync())
        # Now let's enable one action
        self.requestctl(["enable", "cache-text/bad_param_q"])
        # Sync again
        asyncio.run(self.log_handler.startup_sync())

        repo = pathlib.Path(self.repo_path)
        action = repo / "request-actions" / "cache-text" / "bad_param_q.yaml"
        assert action.is_file()
        with action.open() as f:
            action = yaml.safe_load(f)
        assert action["enabled"] is True
        assert action["do_throttle"] is True

    @pytest.mark.skip(reason="This test works locally but fails in CI. Will need to invesitgate.")
    def test_sync_element_deleted(self):
        """Test that elements deleted are removed when syncing."""
        asyncio.run(self.log_handler.startup_sync())
        # Now let's delete one action
        new_step0 = os.path.join(self.base_path, "step0")
        shutil.copytree(
            STEP0_PATH,
            new_step0,
        )
        os.remove(os.path.join(new_step0, "request-actions", "cache-text", "bad_param_q.yaml"))
        self.requestctl(["load", "--reset", "--tree", new_step0])
        # Sync again
        asyncio.run(self.log_handler.startup_sync())
        # Check that the action is gone
        repo = pathlib.Path(self.repo_path)
        action = repo / "request-actions" / "cache-text" / "bad_param_q.yaml"
        assert not action.is_file()

    def test_sync_created(self):
        """Test that elements created are added in a sync."""
        asyncio.run(self.log_handler.startup_sync())
        # Now let's create one action
        new_step0 = os.path.join(self.base_path, "step0")
        shutil.copytree(
            STEP0_PATH,
            new_step0,
        )
        with open(
            os.path.join(new_step0, "request-actions", "cache-text", "new_action.yaml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("expression: ipblock@cloud/aws\n")
        self.requestctl(["load", "--tree", new_step0])
        # Sync again
        asyncio.run(self.log_handler.startup_sync())
        # Check that the action is there
        repo = pathlib.Path(self.repo_path)
        action = repo / "request-actions" / "cache-text" / "new_action.yaml"
        assert action.is_file()
        with action.open() as f:
            action = yaml.safe_load(f)
        assert action["expression"] == "ipblock@cloud/aws"

    def test_audit_handling_modify(self):
        """Test handling a modification."""
        # First, sync the data
        asyncio.run(self.log_handler.startup_sync())
        repo = pathlib.Path(self.repo_path)
        obj_path = repo / "request-actions" / "cache-text" / "bad_param_q.yaml"
        with obj_path.open() as f:
            action = yaml.safe_load(f)
        assert action["enabled"] is False
        # Now let's enable one action
        self.requestctl(["enable", "cache-text/bad_param_q"])
        # Now let's simulate this emitted an audit log message
        audit_log_msg = {
            "ecs.version": "1.11.0",
            "@timestamp": "2024-09-16T07:23:53.977580+00:00",
            "log.level": "info",
            "event.action": "write",
            "event.dataset": "conftool.audit",
            "event.module": "conftool",
            "event.kind": "event",
            "event.outcome": "success",
            "user.name": "godzilla",
            "service.type": "action",
            "service.name": "request-actions/cache-text/bad_param_q",
            "host.hostname": "pinkunicorn",
        }
        expected_time = int(
            time.mktime(time.strptime("2024-09-16T07:23:53.977580+00:00", "%Y-%m-%dT%H:%M:%S.%f%z"))
        )
        asyncio.run(self.log_handler.process_audit_log_entry(audit_log_msg))
        assert obj_path.is_file()
        # Verify it's a well formed yaml file
        with obj_path.open() as f:
            action = yaml.safe_load(f)
        # Let's verify the object we've now modified
        assert action["enabled"] is True

        # now let's check the latest commit
        commit = self.repo[self.repo.head.target]
        assert commit.message == "Commit of write for request-actions/cache-text/bad_param_q.yaml"
        assert commit.author.name == "godzilla"
        assert commit.author.email == "root+godzilla@wikimedia.org"
        assert commit.author.time == expected_time

    def test_audit_handling_delete(self):
        """Test removing an object."""
        asyncio.run(self.log_handler.startup_sync())
        audit_log_msg = {
            "ecs.version": "1.11.0",
            "@timestamp": "2024-09-16T07:23:53.977580+00:00",
            "log.level": "info",
            "event.action": "delete",
            "event.dataset": "conftool.audit",
            "event.module": "conftool",
            "event.kind": "event",
            "event.outcome": "success",
            "user.name": "godzilla",
            "service.type": "action",
            "service.name": "request-actions/cache-text/bad_param_q",
            "host.hostname": "pinkunicorn",
        }

        expected_time = int(
            time.mktime(time.strptime("2024-09-16T07:23:53.977580+00:00", "%Y-%m-%dT%H:%M:%S.%f%z"))
        )
        asyncio.run(self.log_handler.process_audit_log_entry(audit_log_msg))
        repo = pathlib.Path(self.repo_path)
        obj_path = repo / "request-actions" / "cache-text" / "bad_param_q.yaml"
        assert not obj_path.exists()
        # now let's check the latest commit
        commit = self.repo[self.repo.head.target]
        assert commit.message == "Commit of delete for request-actions/cache-text/bad_param_q.yaml"
        assert commit.author.name == "godzilla"
        assert commit.author.email == "root+godzilla@wikimedia.org"
        assert commit.author.time == expected_time

    def test_audit_handling_error(self):
        """Test handling a non-existing object."""
        asyncio.run(self.log_handler.startup_sync())
        current_commit = self.repo.head.target
        audit_log_msg = {
            "ecs.version": "1.11.0",
            "@timestamp": "2024-09-16T07:23:53.977580+00:00",
            "log.level": "info",
            "event.action": "write",
            "event.dataset": "conftool.audit",
            "event.module": "conftool",
            "event.kind": "event",
            "event.outcome": "error",
            "user.name": "godzilla",
            "service.type": "action",
            "service.name": "request-actions/cache-text/non_existent",
            "host.hostname": "pinkunicorn",
        }
        asyncio.run(self.log_handler.process_audit_log_entry(audit_log_msg))
        # We should not have created any commit
        assert self.repo.head.target == current_commit
