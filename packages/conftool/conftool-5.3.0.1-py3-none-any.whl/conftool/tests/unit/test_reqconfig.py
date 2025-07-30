import argparse
from unittest import mock

import pyparsing as pp
import pytest
from conftool import configuration, kvobject
from conftool.cli import ConftoolClient
from conftool.extensions.reqconfig import Requestctl, translate, SCHEMA, RequestctlError
from conftool.tests.unit import MockBackend
from wmflib.interactive import AbortError


@pytest.fixture
def schema():
    """Return the reqestctl schema with a mock backend"""
    mock_schema = ConftoolClient(config=configuration.Config(driver=""), schema=SCHEMA).schema
    # Now overload the backend.
    kvobject.KVObject.backend = MockBackend({})
    return mock_schema


@pytest.fixture
def requestctl():
    args = argparse.Namespace(debug=True, config=None, command="commit")

    # We need to patch the search function in validation so we can test the rest of the code
    def mock_search(*_):
        return True

    req = Requestctl(args)
    kvobject.KVObject.backend = MockBackend({})
    kvobject.KVObject.config = configuration.Config(driver="")
    req.api.expression_processor.set_search_func(mock_search)

    return req


@pytest.mark.parametrize(
    "to_parse,expected",
    [
        ("ipblock@cloud/gcp", ["ipblock@cloud/gcp"]),
        ("pattern@ua/requests", ["pattern@ua/requests"]),
        (
            "ipblock@cloud/gcp AND (pattern@ua/requests OR pattern@ua/curl)",
            ["ipblock@cloud/gcp", "AND", "(", "pattern@ua/requests", "OR", "pattern@ua/curl", ")"],
        ),
        (
            "ipblock@cloud/gcp AND NOT (pattern@ua/requests OR NOT pattern@ua/mediawiki)",
            [
                "ipblock@cloud/gcp",
                "AND NOT",
                "(",
                "pattern@ua/requests",
                "OR NOT",
                "pattern@ua/mediawiki",
                ")",
            ],
        ),
    ],
)
def test_grammar_good(requestctl, to_parse, expected):
    """Test grammar parses valid expressions."""
    assert requestctl.api.expression_processor.parse_as_list(to_parse) == expected


@pytest.mark.parametrize(
    "to_parse", ["pattern-ua/requests", "(pattern@query/nocache OR pattern@pages/wiki"]
)
def test_grammar_bad(requestctl, to_parse):
    """Test grammar rejects invalid expressions."""
    with pytest.raises(pp.ParseException):
        requestctl.api.expression_processor.parse_as_list(to_parse)


def test_grammar_missing_token(requestctl):
    """Test grammar rejects missing tokens."""

    def mock_search_fail_pattern(obj_type, slug):
        if obj_type == "pattern" and slug == "ua/pinkunicorn":
            return False
        return True

    with pytest.raises(
        pp.ParseException, match="The pattern ua/pinkunicorn is not present on the backend."
    ):
        requestctl.api.expression_processor.set_search_func(mock_search_fail_pattern)
        requestctl.api.expression_processor.parse_as_list(
            "ipblock@cloud/gcp AND pattern@ua/pinkunicorn"
        )


patterns = {
    "method/get": {"method": "GET"},
    "ua/unicorn": {"header": "User-Agent", "header_value": "^unicorn/", "header_is_set": True},
    "ua/curl": {"header": "User-Agent", "header_value": "^curl-\\w", "header_is_set": True},
    "ua/requests": {"header": "User-Agent", "header_value": "^requests", "header_is_set": True},
    "url/page_index": {"url_path": "^/w/index.php", "query_parameter": "title", "method": "GET"},
    "req/no_accept": {"header": "Accept", "header_is_set": False},
    "req/accept": {"header": "Accept", "header_is_set": True},
    "req/body": {"method": "POST", "request_body": "foo"},
}


def mock_get_pattern(entity, slug):
    """Mock a request for a specific pattern."""
    obj = entity(*slug.split("/"))
    obj.from_net(patterns[slug])
    return obj


## VCL TRANSLATION


@pytest.mark.parametrize(
    "req,expected",
    [
        # Simple and with cloud
        (
            "pattern@ua/requests AND ipblock@cloud/gcp",
            'req.http.User-Agent ~ "^requests" && req.http.X-Public-Cloud ~ "^gcp$"',
        ),
        # And/or combination with parentheses, abuse ipblock
        (
            "ipblock@abuse/unicorn AND (pattern@ua/curl OR pattern@ua/requests)",
            'std.ip(req.http.X-Client-IP, "192.0.2.1") ~ unicorn && (req.http.User-Agent ~ "^curl-\\w" || req.http.User-Agent ~ "^requests")',
        ),
        # With negative conditions
        (
            "(pattern@ua/curl AND NOT pattern@ua/requests) AND NOT ipblock@abuse/unicorn",
            '(req.http.User-Agent ~ "^curl-\\w" && !(req.http.User-Agent ~ "^requests")) && std.ip(req.http.X-Client-IP, "192.0.2.1") !~ unicorn',
        ),
        # Negative conditions with parentheses
        (
            "ipblock@abuse/unicorn AND NOT (pattern@ua/curl OR pattern@ua/requests)",
            'std.ip(req.http.X-Client-IP, "192.0.2.1") ~ unicorn && !(req.http.User-Agent ~ "^curl-\\w" || req.http.User-Agent ~ "^requests")',
        ),
    ],
)
def test_vcl_from_expression(requestctl, req, expected):
    """Test VCL translation from expression."""
    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        assert requestctl.api.expression_processor.parse_as_vcl(req) == expected


@pytest.mark.parametrize(
    "req, expected, negation",
    [
        ("method/get", 'req.method == "GET"', '!(req.method == "GET")'),
        ("ua/unicorn", 'req.http.User-Agent ~ "^unicorn/"', '!(req.http.User-Agent ~ "^unicorn/")'),
        (
            "url/page_index",
            '(req.method == "GET" && req.url ~ "^/w/index.php.*[?&]title")',
            '!(req.method == "GET" && req.url ~ "^/w/index.php.*[?&]title")',
        ),
        ("req/no_accept", "!req.http.Accept", "!(!req.http.Accept)"),
        ("req/accept", "req.http.Accept", "!(req.http.Accept)"),
        ("req/body", 'req.method == "POST"', '!(req.method == "POST")'),
    ],
)
def test_vcl_from_pattern(requestctl, req, expected, negation):
    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        tr = translate.VCLTranslator(requestctl.schema)
        assert tr.from_pattern(req, False) == expected
        assert tr.from_pattern(req, True) == negation


def test_vcl_from_expression_bad_ipblock(requestctl):
    """An unsupported ipblock raises a readable issue"""
    vcl = translate.VCLTranslator(requestctl.schema)
    with pytest.raises(ValueError, match="scope 'pinkunicorn' is not currently supported"):
        vcl.from_ipblock("ipblock@pinkunicorn/somevalue", False)


@pytest.mark.parametrize(
    "path,param,value,expected",
    [
        ("/url", "", "", "/url"),
        ("", "title", "", "[?&]title"),
        ("", "title", "El-P", "[?&]title=El-P"),
        ("/url", "foo", "bar", "/url.*[?&]foo=bar"),
    ],
)
def test_url_match(requestctl, path, param, value, expected):
    tr = translate.VCLTranslator(requestctl.schema)
    assert tr._url_match(path, param, value) == f'req.url ~ "{expected}"'


## VSL TRANSLATION
@pytest.mark.parametrize(
    "req,expected",
    [
        # Simple and with cloud
        (
            "pattern@ua/unicorn AND ipblock@cloud/gcp",
            'ReqHeader:User-Agent ~ "^unicorn/" and ReqHeader:X-Public-Cloud ~ "^gcp$"',
        ),
        # And/or combination with parentheses, abuse ipblock
        (
            "ipblock@abuse/unicorn AND (pattern@ua/unicorn OR pattern@url/page_index)",
            'VCL_acl ~ "^MATCH unicorn.*" and (ReqHeader:User-Agent ~ "^unicorn/" or (ReqMethod ~ "GET" and ReqURL ~ "^/w/index.php.*[?&]title"))',
        ),
        # With negative conditions
        (
            "(pattern@ua/curl AND NOT pattern@ua/requests) AND NOT ipblock@abuse/unicorn",
            '(ReqHeader:User-Agent ~ "^curl-\\\\w" and not (ReqHeader:User-Agent ~ "^requests")) and VCL_acl ~ "^NO_MATCH unicorn"',
        ),
        # Negative conditions with parentheses
        (
            "ipblock@abuse/unicorn AND NOT (pattern@ua/curl OR pattern@ua/requests)",
            'VCL_acl ~ "^MATCH unicorn.*" and not (ReqHeader:User-Agent ~ "^curl-\\\\w" or ReqHeader:User-Agent ~ "^requests")',
        ),
    ],
)
def test_vsl_from_expression(requestctl, req, expected):
    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        assert requestctl._vsl_from_expression(req) == expected


@pytest.mark.parametrize(
    "req, expected, negation",
    [
        ("method/get", 'ReqMethod ~ "GET"', 'not (ReqMethod ~ "GET")'),
        (
            "ua/unicorn",
            'ReqHeader:User-Agent ~ "^unicorn/"',
            'not (ReqHeader:User-Agent ~ "^unicorn/")',
        ),
        (
            "url/page_index",
            '(ReqMethod ~ "GET" and ReqURL ~ "^/w/index.php.*[?&]title")',
            'not (ReqMethod ~ "GET" and ReqURL ~ "^/w/index.php.*[?&]title")',
        ),
        ("req/no_accept", "not ReqHeader:Accept", "not (not ReqHeader:Accept)"),
        ("req/accept", "ReqHeader:Accept", "not (ReqHeader:Accept)"),
        ("req/body", 'ReqMethod ~ "POST"', 'not (ReqMethod ~ "POST")'),
    ],
)
def test_vsl_from_pattern(requestctl, req, expected, negation):
    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        tr = translate.VSLTranslator(requestctl.schema)
        assert tr.from_pattern(req, False) == expected
        assert tr.from_pattern(req, True) == negation


## HAProxy Translation
@pytest.mark.parametrize(
    "req,expected",
    [
        # Simple and with cloud
        # Please note that the order of the ACLs is alphabetica in AND or OR conditions
        # but this is decided by the sympy dnf resolver, not by the translator.
        # So it might change with different versions of sympy.
        (
            "pattern@ua/requests AND ipblock@cloud/gcp",
            "ipblock_cloud_gcp pattern_ua_requests",
        ),
        # And/or combination with parentheses
        (
            "ipblock@abuse/unicorn AND (pattern@ua/curl OR pattern@ua/requests)",
            "ipblock_abuse_unicorn pattern_ua_curl or ipblock_abuse_unicorn pattern_ua_requests",
        ),
        # With negative conditions, all ANDs
        (
            "(pattern@ua/curl AND NOT pattern@ua/requests) AND NOT ipblock@abuse/unicorn",
            "pattern_ua_curl !ipblock_abuse_unicorn !pattern_ua_requests",
        ),
        # Negative conditions with parentheses
        (
            "ipblock@abuse/unicorn AND NOT (pattern@ua/curl OR pattern@ua/requests)",
            "ipblock_abuse_unicorn !pattern_ua_curl !pattern_ua_requests",
        ),
        # Negative OR condition within parentheses
        # This is tricky, because here pattern@url/page_index is composed of multiple patterns.
        # So this really isn't A AND (B OR NOT C) but A AND (B OR NOT(C AND D AND E))
        # Which translates to A AND (B OR !C OR !D OR !E)
        (
            "ipblock@abuse/unicorn AND (pattern@ua/curl OR NOT pattern@url/page_index)",
            "ipblock_abuse_unicorn pattern_ua_curl or ipblock_abuse_unicorn !pattern_url_page_index_1 or ipblock_abuse_unicorn !pattern_url_page_index_2 or ipblock_abuse_unicorn !pattern_url_page_index_3",
        ),
    ],
)
def test_haproxy_from_expression(requestctl, req, expected):
    """Test HAProxy translation from expression."""
    # Simulate the acl registry here
    registry = {
        "ua/requests": ["pattern_ua_requests"],
        "ua/curl": ["pattern_ua_curl"],
        "url/page_index": [
            "pattern_url_page_index_1",
            "pattern_url_page_index_2",
            "pattern_url_page_index_3",
        ],
    }

    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        with mock.patch(
            "conftool.extensions.reqconfig.translate.HAProxyACLTranslator.registry",
            new_callable=mock.PropertyMock,
            return_value=registry,
        ):
            assert requestctl.api.expression_processor.parse_as_haproxy(req) == expected


@pytest.mark.parametrize(
    "req, expected",
    [
        ("method/get", "acl method_get method GET"),
        ("ua/unicorn", "acl ua_unicorn req.fhdr(User-Agent) -m reg -i ^unicorn/"),
        (
            "url/page_index",
            """acl url_page_index_1 method GET
acl url_page_index_2 path_reg ^/w/index.php
acl url_page_index_3 { query -m reg ^title } { query -m reg &title }""",
        ),
        (
            "req/no_accept",
            "acl req_no_accept hdr_len(Accept, 0)",
        ),
        (
            "req/accept",
            "acl req_accept req.hdr(Accept) -m found",
        ),
    ],
)
def test_haproxy_from_pattern(requestctl, req, expected):
    """Translating a pattern yields the expected ACL."""
    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        ha = translate.HAProxyACLTranslator(requestctl.schema)
        assert ha.from_patterns([req]) == expected


def test_haproxy_from_ipblock(requestctl):
    """Translating an ipblock yields the expected ACL."""
    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        ha = translate.HAProxyACLTranslator(requestctl.schema)
        assert (
            ha.from_ipblocks(["ipblock@cloud/gcp"])
            == 'acl ipblock_cloud_gcp src,map_ip(/etc/haproxy/ipblocks.d/cloud.map) -m str "gcp"'
        )
        assert (
            ha.from_ipblocks(["abuse/unicorn"])
            == 'acl ipblock_abuse_unicorn src,map_ip(/etc/haproxy/ipblocks.d/abuse.map) -m str "unicorn"'
        )


def test_haproxy_req_body(requestctl):
    """Test that request body matching is not supported in HAProxy"""
    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        ha = translate.HAProxyACLTranslator(requestctl.schema)
        with pytest.raises(
            RequestctlError, match="Request body matching is not supported in HAProxy"
        ):
            out = ha.from_patterns(["req/body"])


def test_haproxy_multiple_patterns(requestctl):
    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        ha = translate.HAProxyACLTranslator(requestctl.schema)
        out = ha.from_patterns(["method/get", "ua/unicorn", "ua/requests", "method/get"])
        assert out == "\n".join(
            [
                "acl method_get method GET",
                "acl ua_requests req.fhdr(User-Agent) -m reg -i ^requests",
                "acl ua_unicorn req.fhdr(User-Agent) -m reg -i ^unicorn/",
            ]
        )


def test_haproxy_validate_change(requestctl):
    """Test that validation passes good changes."""
    obj = requestctl.api.get("haproxy_action", "test/foo")
    obj.expression = "ipblock@cloud/gcp"
    # Simulate the acl registry here
    registry = {
        "ua/requests": ["pattern_ua_requests"],
    }

    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        with mock.patch(
            "conftool.extensions.reqconfig.translate.HAProxyACLTranslator.registry",
            new_callable=mock.PropertyMock,
            return_value=registry,
        ):
            # Fixing a broken object is valid
            obj.bw_throttle = True
            obj.slient_drop = True
            requestctl.api.validate(obj, {"silent_drop": False})
            # Changing expression is allowed as well
            obj.silent_drop = False
            requestctl.api.validate(obj, {"expression": "pattern@ua/requests"})


@pytest.mark.parametrize(
    "to_set, change",
    [
        ("bw_throttle", {"silent_drop": True}),
        ("bw_throttle", {"per_ip_concurrency": True}),
        ("per_ip_concurrency", {"expression": "pattern@ua/requests"}),
    ],
)
def test_haproxy_validate_change_fail(requestctl, to_set, change):
    """Test that validation catches errors in changes."""
    obj = requestctl.api.get("haproxy_action", "test/foo")
    obj.expression = "ipblock@cloud/gcp"
    # Simulate the acl registry here
    registry = {
        "ua/requests": ["pattern_ua_requests"],
    }

    with mock.patch("conftool.extensions.reqconfig.translate.get_obj_from_slug") as get_obj:
        get_obj.side_effect = mock_get_pattern
        with mock.patch(
            "conftool.extensions.reqconfig.translate.HAProxyACLTranslator.registry",
            new_callable=mock.PropertyMock,
            return_value=registry,
        ):
            setattr(obj, to_set, True)
            with pytest.raises(RequestctlError):
                requestctl.api.validate(obj, change)


## END TRANSLATION TESTS
