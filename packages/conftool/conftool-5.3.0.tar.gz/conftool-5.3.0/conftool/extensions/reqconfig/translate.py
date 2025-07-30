"""Translators for our expression DSL to various formats."""

import re
from typing import Dict, List, Optional

from sympy import to_dnf
from sympy.parsing.sympy_parser import parse_expr

from conftool.extensions.reqconfig.error import RequestctlError
from conftool.kvobject import Entity
from conftool.loader import Schema

from .schema import get_obj_from_slug


class DSLTranslator:
    """Abstract interface for a translator of our expression DSL."""

    pattern = "pattern@"
    ipblock = "ipblock@"
    # IPblocks implemented as ACLs
    acl_scopes = ["abuse"]
    custom_header_scopes = {"cloud": "X-Public-Cloud", "known-clients": "X-Known-Client"}
    # Translations.
    booleans = {"AND": None, "OR": None}
    parens = {"(": "(", ")": ")"}
    # the following translations are left blank here,as they change
    # Generic negation operator
    no = ""
    # Acl format string for matching ACLs
    acl = ""
    # Acl format string for non-matching ACLs
    no_acl = ""
    # Method selector
    method = ""
    # Url selector
    url = ""
    # Header selector prefix
    header_prefix = ""
    # Body selector. Set to None if body inspection is not supported.
    body: Optional[str] = ""
    # Equality operator. Sadly VSL doesn't have one so it will be overridden there.
    equality = "=="
    # Set to true if we need to escape backslashes
    escape_backslash = False

    def __init__(self, schema: Schema) -> None:
        self._pattern = schema.entities["pattern"]

    def from_expression(self, expression: List[str]) -> str:
        """Translate the expression."""
        translation = ""
        negation = False
        for token in expression:
            # detect negation
            if token.endswith(" NOT"):
                negation = True
                # TODO: use removesuffix once we're on python >= 3.9 only
                token = token[:-4]
            if token in self.booleans:
                translation += self.booleans[token]
            elif token in self.parens:
                if negation:
                    translation += f"{self.no}"
                    negation = False
                translation += self.parens[token]
            elif self._is_pattern(token):
                translation += self.from_pattern(token, negation)
                negation = False
            elif self._is_ipblock(token):
                translation += self.from_ipblock(token, negation)
                negation = False
        return translation

    def _is_pattern(self, token: str) -> bool:
        return token.startswith(self.pattern)

    def _is_ipblock(self, token: str) -> bool:
        return token.startswith(self.ipblock)

    def from_ipblock(self, ipblock: str, negation: bool) -> str:
        """Translate an ipblock to specific rules."""
        slug = ipblock.replace(self.ipblock, "")
        scope, value = slug.split("/")
        if scope in self.acl_scopes:
            if negation:
                return self.no_acl.format(value=value)
            else:
                return self.acl.format(value=value)
        elif scope in self.custom_header_scopes:
            oper = "~"
            if negation:
                oper = "!~"
            return f'{self.header_prefix}{self.custom_header_scopes[scope]} {oper} "^{value}$"'
        else:
            raise ValueError(f"scope '{scope}' is not currently supported")

    def _escape(self, expr: str) -> str:
        """Escape a regex, if needed."""
        if self.escape_backslash:
            return expr.replace("\\", "\\\\")
        else:
            return expr

    def from_pattern(self, pattern: str, negation: bool) -> str:
        """Translate a pattern to a DSL snippet."""
        output = []
        slug = pattern.replace(self.pattern, "")
        obj = get_obj_from_slug(self._pattern, slug)
        if obj.method:
            output.append(f'{self.method} {self.equality} "{obj.method}"')
        url_rule = self._url_match(
            self._escape(obj.url_path), obj.query_parameter, self._escape(obj.query_parameter_value)
        )
        if url_rule != "":
            output.append(url_rule)
        if obj.header:
            # Header is set?
            if obj.header_is_set:
                if obj.header_value:
                    # If there is a value, we need to match the header value
                    # and not the header itself.
                    output.append(
                        f'{self.header_prefix}{obj.header} ~ "{self._escape(obj.header_value)}"'
                    )
                else:
                    output.append(f"{self.header_prefix}{obj.header}")
            else:
                # header is absent
                output.append(f"{self.no}{self.header_prefix}{obj.header}")
        # Do not add a request_body filter to anything but POST.
        # If this inspection is not supported in the translation set self.body to None
        if obj.request_body and obj.method == "POST" and self.body is not None:
            output.append(f'{self.body} ~ "{obj.request_body}"')
        if len(output) > 1 or negation:
            joined = self.booleans["AND"].join(output)
            if negation:
                return f"{self.no}({joined})"
            else:
                return f"({joined})"
        else:
            return output.pop()

    def _url_match(self, url: str, param: str, value: str) -> str:
        """Return the query corresponding to the pattern."""
        if not any([url, param, value]):
            return ""
        out = f'{self.url} ~ "'
        if url != "":
            out += url
            if param != "":
                out += ".*"
        if param != "":
            out += f"[?&]{param}"
            if value != "":
                out += f"={value}"
        # close the quotes
        out += '"'
        return out


class VSLTranslator(DSLTranslator):
    """Translates expressions to VSL."""

    booleans = {"AND": " and ", "OR": " or "}
    parens = {"(": "(", ")": ")"}
    # the following translations are left blank here,as they change
    # Generic negation operator. Please note the needed trailing whitespace
    no = "not "
    # Acl format string for matching ACLs
    acl = 'VCL_acl ~ "^MATCH {value}.*"'
    # Acl format string for non-matching ACLs
    no_acl = 'VCL_acl ~ "^NO_MATCH {value}"'
    # Method selector
    method = "ReqMethod"
    # Url selector
    url = "ReqURL"
    # Header selector prefix
    header_prefix = "ReqHeader:"
    # Body selector
    body = None
    # escape backslash
    escape_backslash = True
    # No equal sign in VSL
    equality = "~"


class VCLTranslator(DSLTranslator):
    """Translates expressions to VSL."""

    booleans = {"AND": " && ", "OR": " || "}
    parens = {"(": "(", ")": ")"}
    # the following translations are left blank here,as they change
    # Generic negation operator.
    no = "!"
    # Acl format string for matching ACLs
    acl = 'std.ip(req.http.X-Client-IP, "192.0.2.1") ~ {value}'
    # Acl format string for non-matching ACLs
    no_acl = 'std.ip(req.http.X-Client-IP, "192.0.2.1") !~ {value}'
    # Method selector
    method = "req.method"
    # Url selector
    url = "req.url"
    # Header selector prefix
    header_prefix = "req.http."
    # Body selector is not supported in varnish minus,
    # but only in the non-free version via the bodyaccess vmod.
    body = None


class HAProxyDSLTranslator:
    """Translates expressions to HAProxy syntax."""

    def __init__(self, schema: Schema) -> None:
        self._acl_registry = HAProxyACLTranslator(schema)

    def acls_from_actions(self, actions: List[Entity]) -> str:
        """Translate an action to HAProxy configuration."""
        # First we need to collect all the patterns and ipblocks
        ipblocks = set()
        patterns = set()
        for action in actions:
            haproxy = HAProxyExpression(action.parsed_expression)
            for ipblock in haproxy.ipblocks:
                ipblocks.add(ipblock)
            for pattern in haproxy.patterns:
                patterns.add(pattern)
        # Now we have all the patterns and ipblocks, let's get the haproxy dsl for them
        acls = self._acl_registry.from_ipblocks(list(ipblocks)) + "\n"
        acls += self._acl_registry.from_patterns(list(patterns))
        return acls

    def reset_acl_registry(self) -> None:
        """Reset the patterns registry."""
        self._acl_registry.reset_registry()

    def from_expression(self, expression: List[str]) -> str:
        """Translate an expression to HAProxy configuration."""
        # Now we need to translate the expressions
        haproxy = HAProxyExpression(expression)
        try:
            return haproxy.haproxy_expression(self._acl_registry.registry)
        except KeyError as e:
            raise RequestctlError(
                f"Pattern '{e}' not found in the acl registry. "
                "Maybe you forgot to call .acls_from_actions() before calling this method"
            ) from e

    def symbolic_from_expression(self, expression: str) -> str:
        """Translate an expression to sympy symbolic format."""
        haproxy = HAProxyExpression(expression)
        return haproxy.symbolic_expression(self._acl_registry.registry)


class HAProxyACLTranslator:
    """Translates patterns and ipblocks to HAProxy ACLs."""

    def __init__(self, schema: Schema) -> None:
        self._pattern = schema.entities["pattern"]
        self._patterns_registry: Dict[str, List[str]] = {}
        self._haproxy_path = Entity.config.requestctl().haproxy_path

    def from_ipblocks(self, ipblocks: List[str]) -> str:
        """Translate ipblocks to HAProxy ACLs."""
        out = []
        # Sort the ipblocks to ensure consistent output
        for ipblock in sorted(ipblocks):
            ipblock = ipblock.replace("ipblock@", "")
            scope, value = ipblock.split("/")
            fullpath = f"{self._haproxy_path}ipblocks.d/{scope}.map"
            out.append(f'acl ipblock_{scope}_{value} src,map_ip({fullpath}) -m str "{value}"')
        return "\n".join(out)

    def from_patterns(self, patterns: List[str]) -> str:
        """Translate patterns to HAProxy ACLs."""
        out = []
        # Some patterns may contain more than one ACL,
        # so we need to keep track of the ones we've already translated
        # for when we're going to refer to them when translating expressions.
        for pattern in sorted(patterns):
            if pattern in self._patterns_registry:
                continue
            acls = self._translate_pattern(pattern)
            out.extend(acls.values())
            self._patterns_registry[pattern] = list(acls.keys())
        return "\n".join(out)

    def reset_registry(self) -> None:
        """Reset the patterns registry."""
        self._patterns_registry = {}

    @property
    def registry(self) -> Dict[str, List[str]]:
        """Return the patterns registry."""
        return self._patterns_registry

    def _translate_pattern(self, pattern: str) -> Dict[str, str]:
        obj = get_obj_from_slug(self._pattern, pattern)
        acls = []
        if obj.method:
            acls.append(f"method {obj.method}")
        if obj.url_path:
            acls.append(f"path_reg {obj.url_path}")
        if obj.header:
            # We want first to check if the header is set or not, then check the value
            if obj.header_is_set:
                if obj.header_value:
                    # If there is a value, we need to match the full header, as hdr_reg actually
                    # matches on a list of entries, each created splitting the header by commas.
                    # So for instance, the expression hdr_reg(X-Header) -i ^foo would match both
                    # X-Header: foo and X-Header: bar, foo. We don't want that.
                    acls.append(f"req.fhdr({obj.header}) -m reg -i {obj.header_value}")
                else:
                    # no value set, we just check for existence of the header
                    acls.append(f"req.hdr({obj.header}) -m found")
            else:
                # Here we can use hdr_len, as we expect the value to be empty
                acls.append(f"hdr_len({obj.header}, 0)")

        if obj.query_parameter:
            # We want to support regex matching for query parameters
            # so we can't use urlp.
            if obj.query_parameter_value:
                acls.append(f"query -m reg -i {obj.query_parameter}={obj.query_parameter_value}")
            else:
                # If there's no value, we need to match a parameter from
                # beginning to end. Given "query" in haproxy removes the initial
                # question mark, we need to match the parameter from the beginning
                # of the query string or after an ampersand.
                begin_query = f"query -m reg ^{obj.query_parameter}"
                ampersand_query = f"query -m reg &{obj.query_parameter}"
                # ACLs combine rules with OR, so we need to combine the two
                acls.append(f"{{ {begin_query} }} {{ {ampersand_query} }}")
        if obj.request_body:
            # We don't want to match on req.body because it would require us
            # to do request buffering. So we raise an exception if we find a request
            # that includes a request body
            raise RequestctlError("Request body matching is not supported in HAProxy")
        # Now build the output
        safe_pattern = haproxy_safe_acl_name(pattern)
        # Single ACL
        if len(acls) == 1:
            return {safe_pattern: f"acl {safe_pattern} {acls[0]}"}
        # Multiple ACLs
        # In this case, we return a dictionary with the ACLs
        # indexed by a label that includes the pattern name and
        # an integer. So pattern foo will have labels foo_1, foo_2, etc.
        return_value = {}
        for idx, acl in enumerate(acls):
            label = f"{safe_pattern}_{idx+1}"
            return_value[label] = f"acl {label} {acl}"
        return return_value


def haproxy_safe_acl_name(name: str) -> str:
    """Return a safe name for an ACL."""
    return name.replace("/", "_").replace("@", "_")


class HAProxyExpression:
    """Representation of a requestctl expression for haproxy."""

    dsl_to_symbol = {"AND": "&", "OR": "|", "AND NOT": "& ~", "OR NOT": "| ~"}
    ipblock_label = "ipblock@"
    pattern_label = "pattern@"

    def __init__(self, expression: List[str]):
        self.expression = expression

    @property
    def patterns(self) -> List[str]:
        """Return the patterns in the expression."""
        return [
            token.replace(self.pattern_label, "")
            for token in self.expression
            if token.startswith(self.pattern_label)
        ]

    @property
    def ipblocks(self) -> List[str]:
        """Return the ipblocks in the expression."""
        return [
            token.replace(self.ipblock_label, "")
            for token in self.expression
            if token.startswith(self.ipblock_label)
        ]

    def symbolic_expression(self, patterns_registry: Dict[str, List[str]]) -> str:
        """Return the symbolic expression."""
        return self.to_symbol(self.expanded_expression(patterns_registry))

    def haproxy_expression(self, patterns_registry: Dict[str, List[str]]) -> str:
        """Return the HAProxy expression."""
        # Step 1: expand all patterns and convert the expression to a symbolic format
        symbolic = self.symbolic_expression(patterns_registry)
        # Step 2: resolve all parentheses and distribute and over or
        # using sympy
        try:
            dnf = self.normalize_symbolic(symbolic)
        except SyntaxError as e:
            raise RequestctlError(f"Error parsing expression '{self.expression}': {e}") from e
        # Step 3: convert the dnf to a HAProxy dsl expression
        return self.symbol_to_haproxy(str(dnf))

    def expanded_expression(self, patterns: Dict[str, List[str]]) -> List[str]:
        """Expand the patterns in the expression."""
        parsed_expr = []
        for token in self.expression:
            if token.startswith("pattern@"):
                acls = patterns[token.replace("pattern@", "")]
                if len(acls) == 1:
                    parsed_expr.append(acls[0])
                elif len(acls) > 1:
                    parsed_expr.append("(")
                    for acl in acls:
                        parsed_expr.append(acl)
                        parsed_expr.append("AND")
                    # Remove the trailing AND
                    parsed_expr.pop()
                    parsed_expr.append(")")
            elif token.startswith("ipblock@"):
                parsed_expr.append(haproxy_safe_acl_name(token))
            else:
                parsed_expr.append(token)

        return parsed_expr

    @staticmethod
    def normalize_symbolic_to_haproxy(symbolic_expr: str) -> str:
        """Convert a symbolic expression to a HAProxy expression."""
        return HAProxyExpression.symbol_to_haproxy(
            HAProxyExpression.normalize_symbolic(symbolic_expr)
        )

    @staticmethod
    def normalize_symbolic(symbolic_expr: str) -> str:
        """Returns the disjunctive normal form of a symbolic expression."""
        parsed = parse_expr(symbolic_expr)
        return str(to_dnf(parsed, True))

    @staticmethod
    def to_symbol(expression: List[str]) -> str:
        """Convert a list of tokens to a symbolic expression."""
        output = ""
        for token in expression:
            if token in HAProxyExpression.dsl_to_symbol:
                output += f" {HAProxyExpression.dsl_to_symbol[token]} "
            else:
                # "-" gets interpeted as a subtraction operator
                output += token.replace("-", "AAAA")
        return output

    @staticmethod
    def symbol_to_haproxy(symbolic_expr: str) -> str:
        """Convert a symbolic expression to a HAProxy expression."""
        # Re-convert AAAA to -
        haproxy_expr = symbolic_expr.replace("AAAA", "-")
        # We need to replace the symbols with the HAProxy ones
        # In haproxy AND is implicit
        haproxy_expr = re.sub(r"\s*&\s*", " ", haproxy_expr)
        # OR is or
        haproxy_expr = haproxy_expr.replace("|", "or")
        # No parentheses in HAProxy
        haproxy_expr = haproxy_expr.replace("(", " ").replace(")", " ")
        # NOT is ! in HAProxy
        haproxy_expr = re.sub(r"~\s*", "!", haproxy_expr)
        haproxy_expr = haproxy_expr.replace(r"~\s*", "!")
        # Normalize spaces
        haproxy_expr = re.sub(r"\s+", " ", haproxy_expr)
        haproxy_expr = haproxy_expr.strip()
        return haproxy_expr
