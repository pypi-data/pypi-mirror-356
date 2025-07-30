import argparse
import copy
import json
import os
import re
import shutil
import tempfile
from io import StringIO
from time import time
from unittest.mock import patch

from conftool import kvobject
import pytest
import yaml
from conftool.extensions import reqconfig
from conftool.extensions.reqconfig import api
from conftool.tests.integration import IntegrationTestBase

fixtures_base = os.path.realpath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, "fixtures", "reqconfig")
)
STEP0_PATH = os.path.join(fixtures_base, "step0")


class ReqConfigTestBase(IntegrationTestBase):
    """Test requestctl base."""

    @classmethod
    def setUpClass(cls):
        """method to run before the test suite runs."""
        super().setUpClass()
        cls.schema = reqconfig.get_schema(cls.get_config())

    def get_cli(self, *argv):
        """Get a requestctl instance from args."""
        args = reqconfig.parse_args(argv)
        return reqconfig.cli.Requestctl(args)

    def get(self, what, *tags):
        """Get a conftool object."""
        return self.schema.entities[what](*tags)


class ReqConfigTest(ReqConfigTestBase):
    """Test requestctl."""

    def setUp(self):
        """Method run before every test."""
        super().setUp()
        # Run sync.
        self.get_cli("load", "--reset", "--tree", STEP0_PATH).run()

    # Required as long as this class inherits from TestCase
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    @pytest.fixture(autouse=True)
    def caplog(self, caplog):
        self.caplog = caplog

    def test_load_apply_all(self):
        """Test syncing all properties."""
        # Now let's verify sync actually works.
        # We should have three actions defined now.
        all_actions = self.schema.entities["action"].all()
        assert len(all_actions) == 3
        # Same with haproxy, where we have three actions.
        all_haproxy = self.schema.entities["haproxy_action"].all()
        assert len(all_haproxy) == 3
        # These actions are not enabled, even if they are on disk.
        for obj in all_actions + all_haproxy:
            assert obj.enabled is False
        # Enable one
        self.get_cli("enable", "cache-text/requests_ua_api").run()
        assert self.get("action", "cache-text", "requests_ua_api").enabled is True
        # And disable it.
        self.get_cli("disable", "cache-text/requests_ua_api").run()
        assert self.get("action", "cache-text", "requests_ua_api").enabled is False
        # Now let's try to apply a bad object
        bad_expr_path = os.path.join(
            fixtures_base,
            "bad_expr",
            "request-actions",
            "cache-upload/enwiki_api_cloud.yaml",
        )
        with pytest.raises(reqconfig.cli.RequestctlError):
            self.get_cli(
                "apply", "action", "cache-upload/requests_ua_api", "-f", bad_expr_path
            ).run()

        assert self.get("action", "cache-upload", "requests_ua_api").exists is False
        # Now let's try to delete an object that is referenced by another one.
        with pytest.raises(reqconfig.cli.RequestctlError):
            self.get_cli("delete", "pattern", "cache-text/restbase").run()

        assert self.get("pattern", "cache-text", "restbase").exists is True
        # ok, let's retry with the expressions fixed as well.
        step2_path = os.path.join(fixtures_base, "step2")
        actions_step2 = os.path.join(step2_path, "request-actions")
        for action_path in "cache-text/enwiki_api_cloud", "cache-text/requests_ua_api":
            self.get_cli(
                "apply",
                "action",
                action_path,
                "-f",
                os.path.join(actions_step2, f"{action_path}.yaml"),
            ).run()

        self.get_cli("delete", "pattern", "cache-text/restbase").run()
        assert self.get("pattern", "cache-text", "restbase").exists is False

    def test_get(self):
        """Test requestctl get."""
        # Get a specific pattern
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.get_cli("get", "pattern", "cache-text/action_api", "-o", "json").run()
        json.loads(mock_stdout.getvalue())
        # now an ipblock, yaml format
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.get_cli("get", "ipblock", "cloud/aws", "-o", "yaml").run()
        yaml.safe_load(mock_stdout)
        # finally list all actions, pretty printed
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.get_cli("get", "action").run()
        self.assertRegex(mock_stdout.getvalue(), r"cache-text/requests_ua_api")
        self.assertRegex(mock_stdout.getvalue(), r"cache-text/enwiki_api_cloud")
        # get with a badly formatted path will result in an exception
        self.assertRaises(
            reqconfig.cli.RequestctlError,
            self.get_cli("get", "ipblock", "cloud-aws", "-o", "yaml").run,
        )
        # On the other hand if we're not finding anything, we return an empty dictionary.
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.get_cli("get", "ipblock", "cloud/not-existent", "-o", "yaml").run()
        self.assertEqual(yaml.safe_load(mock_stdout.getvalue()), {})

    def test_failures(self):
        """Test some failure mode for bad args."""
        args = [
            {"command": "unicorn", "action": "pink"},  # inexistent command
            {
                "command": "enable",
                "action": "something/not-here",
            },  # enable a non existent action.
        ]
        for test_case in args:
            test_case.update({"debug": False, "config": None, "object_type": "action"})
            args = argparse.Namespace(**test_case)
            with pytest.raises(reqconfig.cli.RequestctlError):
                rq = reqconfig.cli.Requestctl(args)
                rq.run()

    def test_dump_and_load(self):
        """Test requestctl dump and load cycle."""
        tmpdir = tempfile.mkdtemp()
        try:
            dumpfile = os.path.join(tmpdir, "dump.yaml")
            self.get_cli("dump", "-f", dumpfile).run()
            self.get_cli("load", "-f", dumpfile).run()
        finally:
            shutil.rmtree(tmpdir)

    def test_log(self):
        """Test the behaviour of requestctl log."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.get_cli("log", "cache-text/enwiki_api_cloud").run()
        log_out = mock_stdout.getvalue()
        # Check url matching
        self.assertRegex(
            log_out,
            r'(?m)\(\s*ReqURL ~ "/w/api.php" or ReqURL ~ "\^/api/rest_v1/"\s*\)',
        )
        self.assertRegex(log_out, r'(?m)ReqHeader:X-Public-Cloud ~ "\^aws\$"')

    def test_vcl(self):
        """Test the behaviour of requestctl vcl."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.get_cli("vcl", "cache-text/enwiki_api_cloud").run()
        vcl = mock_stdout.getvalue()
        self.assertRegex(vcl, r"(?m)sudo requestctl disable 'cache-text/enwiki_api_cloud'")
        self.assertRegex(vcl, r'(?m)\(req.url ~ "/w/api.php" \|\| req.url ~ "\^/api/rest_v1/"\)')
        self.assertRegex(vcl, r'(?m)req.http.X-Public-Cloud ~ "\^azure\$"')
        self.assertRegex(
            vcl,
            r'(?m)vsthrottle\.is_denied\("requestctl:enwiki_api_cloud", 5000, 30s, 300s\)',
        )
        self.assertRegex(
            vcl,
            r'(?m)set req\.http\.X-Requestctl = req\.http\.X-Requestctl \+ ",enwiki_api_cloud"',
        )
        self.assertRegex(vcl, r"(?m) set req\.http\.Retry-After = 300;")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.get_cli("vcl", "cache-text/bad_param_q").run()
        rule = mock_stdout.getvalue()
        assert rule.find('req.url ~ "[?&]q=\\w{12}" || req.method == "POST"') >= 0

    def test_commit(self):
        """Test the behaviour of requestctl commit."""
        # Test 1: enable a rule, commit, it should add the rule in the right place
        self.get_cli("enable", "cache-text/enwiki_api_cloud").run()
        self.get_cli("commit", "-b").run()
        global_vcl = self.schema.entities["vcl"]("cache-text", "global")
        assert global_vcl.exists
        # just to check it contains the rule we've just enabled.
        self.assertRegex(global_vcl.vcl, r'(?m)req.http.X-Public-Cloud ~ "\^azure\$"')
        # check rules for logging requests that have log_matching true
        dc1_vcl = self.schema.entities["vcl"]("cache-text", "dc1")
        self.assertRegex(
            dc1_vcl.vcl,
            r'(?m)set req\.http\.X-Requestctl = req\.http\.X-Requestctl \+ ",requests_ua_api"',
        )
        # Test 2: enable a second rule, disable the first (applied to different contexts), and the first vanishes the second is there.
        self.get_cli("disable", "-s", "varnish", "cache-text/enwiki_api_cloud").run()
        self.get_cli("enable", "cache-text/requests_ua_api").run()
        # Also enable an haproxy rule that matches the same pattern
        self.get_cli("enable", "-s", "haproxy", "cache-text/enwiki_api_cloud").run()
        self.get_cli("commit", "-b").run()
        global_vcl = self.schema.entities["vcl"]("cache-text", "global")
        for dc in ["dc1", "dc2"]:
            dc_vcl = self.schema.entities["vcl"]("cache-text", dc)
            self.assertRegex(dc_vcl.vcl, r"(?m)requests")
        assert global_vcl.vcl == ""
        # TODO: haproxy

    def test_commit_haproxy(self):
        """Test the behaviour of requestctl commit with haproxy_actions and haproxy_dsl."""

        # Some helper functions to avoid copy&paste
        def assertEqsinBadParamQ(self):
            eqsin_hap = self.schema.entities["haproxy_dsl"]("cache-text", "eqsin")
            assert eqsin_hap.exists
            self.assertRegex(eqsin_hap.dsl, r"(?m)# This filter is generated from data in etcd")
            self.assertRegex(
                eqsin_hap.dsl,
                r"(?m)http-request set-header x-requestctl .*req\.fhdr\(x-requestctl\).*hap:bad_param_q",
            )
            self.assertRegex(
                eqsin_hap.dsl,
                r"(?m)^http-request deny status 429 content-type text/plain string \"We don't like qs\" if cache-text_bad_param_q$",
            )
            return eqsin_hap

        def assertEnwikiApiCloud(self, hap, enabled):
            self.assertRegex(
                hap.dsl,
                r"(?m)^acl enwiki_api_cloud__too_high_now sc0_trackers\(httpreqrate\) ge 54321([ #]+.*)?$",
            )
            self.assertRegex(
                hap.dsl,
                r"(?m)http-request set-header x-requestctl .*req\.fhdr\(x-requestctl\).*hap:enwiki_api_cloud",
            )
            self.assertRegex(
                hap.dsl,
                r"(?m)http-request set-var-fmt\(req\..*enwiki_api_cloud__too_high_now",
            )
            self.assertRegex(
                hap.dsl,
                r"(?m)http-request set-var\(req\..*enwiki_api_cloud__too_high_now",
            )
            self.assertRegex(
                hap.dsl,
                r"(?m)http-request sc-(inc|add)-gpc\(1.*enwiki_api_cloud__too_high_now",
            )
            self.assertRegex(
                hap.dsl,
                r"(?m)debug\(enwiki_api_cloud,"
                + re.escape(self.get_config().requestctl().haproxy_ring_name)
                + r"\)",
            )
            if enabled:
                self.assertRegex(
                    hap.dsl,
                    r"(?m)^http-request deny status 429 .* if enwiki_api_cloud__too_high_recently",
                )
                self.assertRegex(hap.dsl, r"(?m)\"enforcement\":true[,}]")
            else:
                self.assertNotRegex(
                    hap.dsl,
                    r"(?m)^http-request deny status 429 content-type text/plain string .+ if enwiki_api_cloud__too_high_recently",
                )
                self.assertRegex(
                    hap.dsl,
                    r"(?m)# This filter is DISABLED",
                )
                self.assertRegex(hap.dsl, r"(?m)\"enforcement\":false[,}]")

        self.get_cli("enable", "-s", "haproxy", "cache-text/bad_param_q").run()
        self.get_cli("commit", "-b").run()
        # Now verify the haproxy side of things, again beginning from step0 state.
        self.assertSetEqual(
            set(d.name for d in self.schema.entities["haproxy_dsl"].all()),
            {"eqsin", "codfw"},
        )
        assertEqsinBadParamQ(self)

        # Enable a global rule, check that global ACLs propagated to per-site
        self.get_cli("enable", "cache-text/enwiki_api_cloud", "-s", "haproxy").run()
        self.get_cli("commit", "-b").run()
        self.assertSetEqual(
            set(
                d.name
                for d in self.schema.entities["haproxy_dsl"].query({"name": re.compile(".*")})
            ),
            {"eqsin", "codfw", "global"},
        )
        eqsin_hap = assertEqsinBadParamQ(self)
        assertEnwikiApiCloud(self, eqsin_hap, True)

        # Now verify the global state as well
        global_hap = self.schema.entities["haproxy_dsl"]("cache-text", "global")
        assert global_hap.exists
        assertEnwikiApiCloud(self, global_hap, True)

        step2_path = os.path.join(fixtures_base, "step2")
        self.get_cli("load", "--reset", "--tree", step2_path).run()
        self.get_cli("disable", "cache-text/enwiki_api_cloud", "-s", "haproxy").run()
        self.get_cli("commit", "-b").run()
        global_hap = self.schema.entities["haproxy_dsl"]("cache-text", "global")
        assert global_hap.exists
        assertEnwikiApiCloud(self, global_hap, False)

    def test_haproxy_commit_hyphens(self):
        self.get_cli("enable", "cache-text/names-with-hyphens", "-s", "haproxy").run()
        self.get_cli("commit", "-b").run()
        global_hap = self.schema.entities["haproxy_dsl"]("cache-text", "global")
        assert global_hap.exists
        # Assert we correctly translated back to where hyphens are allowed in haproxy config
        self.assertRegex(
            global_hap.dsl,
            r"(?m)^acl names-with-hyphens__too_high_now sc0_trackers\(httpreqrate\) ge 20([ #]+.*)?$",
        )
        self.assertRegex(
            global_hap.dsl,
            r"(?m) if ipblock_cloud_aws names-with-hyphens__too_high_now or ipblock_cloud_azure names-with-hyphens__too_high_now([ #]+.*)?$",
        )

    def test_commit_preserve_ordering(self):
        """Test that requestctl commit preserves order."""
        # Let's enable 2 rules in the same context, check that multiple commits won't change the output
        self.get_cli("enable", "cache-text/enwiki_api_cloud").run()
        self.get_cli("enable", "cache-text/bad_param_q").run()
        self.get_cli("commit", "-b").run()
        global_vcl = self.schema.entities["vcl"]("cache-text", "global")
        for _ in range(10):
            self.get_cli("commit", "-b").run()
            assert global_vcl.vcl == self.schema.entities["vcl"]("cache-text", "global").vcl

    def test_find(self):
        """Test finding objects"""
        no_data = self.get_cli("find", "enwiki_api_cloud")
        one_match = self.get_cli("find", "cloud/ovh")
        multi_match = self.get_cli("find", "cache-text/action_api")
        match_haproxy = self.get_cli("find", "-s", "haproxy", "cloud/aws")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            no_data.run()
            assert mock_stdout.getvalue() == "No entries found.\n"
            mock_stdout.truncate(0)
            one_match.run()
            self.assertIn(
                "action: cache-text/enwiki_api_cloud, expression: ( pattern@cache-text/action_api OR pattern@cache-text/restbase ) AND ( ipblock@cloud/aws OR ipblock@cloud/azure OR ipblock@cloud/ovh )\n",
                mock_stdout.getvalue(),
            )
            mock_stdout.truncate(0)
            multi_match.run()
            assert len(mock_stdout.getvalue().splitlines()) == 2
            # we now also have an haproxy_action that matches the pattern
            mock_stdout.truncate(0)
            match_haproxy.run()
            self.assertIn(
                "haproxy_action: cache-text/enwiki_api_cloud, expression: ipblock@cloud/aws OR ipblock@cloud/azure\n",
                mock_stdout.getvalue(),
            )

    def test_cleanup(self):
        """Test the cleanup command."""
        self.get_cli("enable", "cache-text/enwiki_api_cloud").run()
        # Let's change the last modified date to 31 days ago
        obj = self.get("action", "cache-text", "enwiki_api_cloud")
        obj.last_modified = int(time()) - 31 * 86400
        obj.write()
        # First, let's run the cleanup command
        self.get_cli("cleanup").run()
        # Now let's check that the object is disabled
        obj = self.get("action", "cache-text", "enwiki_api_cloud")
        assert obj.enabled is False
        assert obj.log_matching is True

    # Can't use @pytest.mark.parametrize because subclass of TestCase
    def test_find_ip_ok(self):
        """It should find all the IP blocks the given IP is part of."""
        self.get_cli("find-ip", "1.123.123.123").run()
        out, _ = self.capsys.readouterr()
        assert "IP 1.123.123.123 is part of ipblock cloud/aws" == out.strip()

    # Can't use @pytest.mark.parametrize because subclass of TestCase
    def test_find_ip_missing(self):
        """It should tell that the given IP is not part of any IP block."""
        self.get_cli("find-ip", "127.0.0.1").run()
        out, _ = self.capsys.readouterr()
        assert "IP 127.0.0.1 is not part of any ipblock in the datastore." == out.strip()

    def test_test_validate_bad_ip(self):
        bad_ip_path = os.path.join(fixtures_base, "bad_ip")
        self.get_cli("load", "--tree", bad_ip_path).run()
        # ensure we can load good addresses

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.get_cli("get", "ipblock", "cloud/invalid", "-o", "yaml").run()
        data = yaml.safe_load(mock_stdout.getvalue())
        # The following should all be removed
        # ['not an ip address', '1.1.1.1.1', 2001::db8::1']

        self.assertEqual(data["cloud/invalid"]["cidrs"], ["1.1.1.1", "2.2.2.2/8", "2001:db8::1"])

    def test_schema_fields(self):
        """Test schema fields."""
        obj = self.get("action", "cache-text", "requests_ua_api")
        self.assertIn("cache_miss_only", obj.field_names())
        cache_miss_only = obj.get_field("cache_miss_only")
        self.assertEqual(cache_miss_only.name, "cache_miss_only")
        self.assertEqual(cache_miss_only.type, "bool")
        self.assertEqual(cache_miss_only.docstring, "If you can enable this, please do so")
        self.assertEqual(cache_miss_only.default, True)
        self.assertIn("resp_reason", obj.field_names())
        resp_reason = obj.get_field("resp_reason")
        self.assertEqual(resp_reason.example, "Too Many Requests")

    def test_schema_upgrade(self):
        """Test schema upgrade."""
        # Now let's simulate a schema upgrade
        new_schema = copy.deepcopy(reqconfig.SCHEMA)
        new_schema["pattern"]["schema"]["new_field"] = {
            "type": "string",
            "default": "foobar!",
        }
        with patch("conftool.extensions.reqconfig.api.SCHEMA", new_schema):
            reqctl = self.get_cli("upgrade-schema", "pattern")
            reqctl.run()
            # Now let's verify the new field is there
            obj = self.get("pattern", "cache-text", "action_api")
            data = kvobject.KVObject.backend.driver.read(obj.key)
            assert data["new_field"] == "foobar!"

    def test_schema_upgrade_dry_run(self):
        """Test a schema upgrade dry run does not write to the backend."""
        new_schema = copy.deepcopy(reqconfig.SCHEMA)
        new_schema["pattern"]["schema"]["new_field"] = {
            "type": "string",
            "default": "foobar!",
        }
        with patch("conftool.extensions.reqconfig.api.SCHEMA", new_schema):
            reqctl = self.get_cli("upgrade-schema", "--dry-run", "pattern")
            reqctl.run()
            # Now let's verify the new field is not in the backend
            obj = self.get("pattern", "cache-text", "action_api")
            data = kvobject.KVObject.backend.driver.read(obj.key)
            assert "new_field" not in data

    def test_schema_upgrade_validation_error(self):
        """Test schema upgrade validation error."""
        new_schema = copy.deepcopy(reqconfig.SCHEMA)
        # Make a change that will make current objects with the method field invalid
        new_schema["pattern"]["schema"]["method"] = {"type": "bool", "default": False}
        with patch("conftool.extensions.reqconfig.api.SCHEMA", new_schema):
            reqctl = self.get_cli("upgrade-schema", "pattern")
            with self.assertRaises(reqconfig.cli.RequestctlError):
                reqctl.run()
            assert "cache-text/bad_body: " in self.caplog.text
            assert "cache-text/bad_param_q: " in self.caplog.text
            # Check no changes were made to the backend
            obj = self.get("pattern", "cache-text", "bad_body")
            data = kvobject.KVObject.backend.driver.read(obj.key)
            assert data["method"] == "POST"

    def test_schema_upgrade_force(self):
        """Test schema upgrade with force option."""
        new_schema = copy.deepcopy(reqconfig.SCHEMA)
        new_schema["pattern"]["schema"]["method"] = {"type": "bool", "default": False}
        with patch("conftool.extensions.reqconfig.api.SCHEMA", new_schema):
            reqctl = self.get_cli("upgrade-schema", "--force", "pattern")
            reqctl.run()
            # Now let's verify the new field is there
            obj = self.get("pattern", "cache-text", "bad_body")
            data = kvobject.KVObject.backend.driver.read(obj.key)
            assert data["method"] is False

    def test_get_dsl_haproxy_repeat(self):
        """Test that we can get the DSL for a haproxy action multiple times."""
        self.get_cli("enable", "-s", "haproxy", "cache-text/bad_param_q").run()
        # Let's instantiate the api.
        api_instance = api.RequestctlApi(api.client())
        # Now let's get the DSL for the haproxy action twice
        first = api_instance.get_dsl_diffs("haproxy_action")
        second = api_instance.get_dsl_diffs("haproxy_action")
        for cluster, dc in first.items():
            assert cluster in second
            for site, difftuple in dc.items():
                assert site in second[cluster]
                assert difftuple[1] == second[cluster][site][1]
