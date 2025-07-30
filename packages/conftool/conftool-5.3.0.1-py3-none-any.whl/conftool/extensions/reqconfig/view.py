"""Views for requestctl."""

import json
import textwrap
from string import Template
from typing import Dict, List

import tabulate
import yaml
from conftool.extensions.reqconfig.translate import HAProxyExpression
from conftool.kvobject import Entity


def get(fmt: str) -> "View":
    """Factory method to get a view class.

    Typical use: reqconfig.view.get("json").render(data)
    """
    if fmt == "json":
        return JsonView
    elif fmt == "yaml":
        return YamlView
    elif fmt == "pretty":
        return PrettyView
    elif fmt == "vcl":
        return VCLView
    elif fmt == "vsl":
        return VSLView
    elif fmt == "haproxycfg":
        return HaProxyDSLView
    else:
        raise ValueError(f"Unsupported format '{format}'")


class View:
    """Abstract view interface"""

    @classmethod
    def render(cls, data: List[Entity], object_type: str) -> str:
        """Renders the view."""


class YamlView(View):
    """Yaml representation of our objects."""

    @classmethod
    def dump(cls, data: List[Entity]) -> Dict[str, Dict]:
        """Create a easily-human-readable dump of the data."""
        dump = {}
        for entity in data:
            asdict = entity.asdict()
            dump[entity.pprint()] = asdict[entity.name]
        return dump

    @classmethod
    def render(cls, data: List[Entity], _: str) -> str:
        return yaml.dump(cls.dump(data))


class JsonView(YamlView):
    """Json representation of our objects."""

    @classmethod
    def render(cls, data: List[Entity], _: str) -> str:
        return json.dumps(cls.dump(data))


class PrettyView(View):
    """Pretty-print information about the selected entitites."""

    headers = {
        "pattern": ["name", "pattern"],
        "ipblock": ["name", "cidrs"],
        "action": ["name", "action", "response", "throttle"],
    }

    @classmethod
    def render(cls, data: List[Entity], object_type: str) -> str:
        headers = cls.headers[object_type]
        tabular = []
        for entity in data:
            if object_type == "pattern":
                element = (entity.pprint(), cls.get_pattern(entity))
            elif object_type == "ipblock":
                element = (entity.pprint(), "\n".join(entity.cidrs))
            elif object_type == "action":
                element = (
                    textwrap.shorten(entity.pprint(), width=30),
                    textwrap.fill(entity.expression, width=30),
                    textwrap.shorten(f"{entity.resp_status} {entity.resp_reason}", width=20),
                    str(entity.do_throttle).lower(),
                )
            tabular.append(element)
        return tabulate.tabulate(tabular, headers, tablefmt="pretty")

    @classmethod
    def get_pattern(cls, entity: Entity) -> str:
        """String representation of a pattern"""
        out = []
        if entity.method:
            out.append(entity.method)
        if entity.url_path:
            out.append(f"url:{entity.url_path}")
        if entity.header:
            out.append(f"{entity.header}: {entity.header_value}")
        if entity.query_parameter:
            out.append(f"?{entity.query_parameter}={entity.query_parameter_value}")
        return "\n".join(out)


class VCLView(View):
    """Renders an action as VCL."""

    tpl_ban = Template(
        """
// FILTER $name
// $comment
// This filter is generated from data in $driver. To disable it, run the following command:
// sudo requestctl disable '$pprint'
if ($expression) {
    set req.http.X-Requestctl = req.http.X-Requestctl + ",$name";
    return (synth($status, "$reason"));
}
"""
    )
    tpl_throttle = Template(
        """
// FILTER $name
// $comment
// This filter is generated from data in $driver. To disable it, run the following command:
// sudo requestctl disable '$pprint'
if ($expression) {
    set req.http.X-Requestctl = req.http.X-Requestctl + ",$name";
    if ($throttle) {
        set req.http.Retry-After = $retry_after;
        return (synth($status, "$reason"));
    }
}
"""
    )
    tpl_log_only = Template(
        """
// FILTER $name
// $comment
// This filter is DISABLED. to enable it, run the following command:
// sudo requestctl enable '$pprint'
// The stanza below is only for logging purposes.
if ($expression) {
    set req.http.X-Requestctl = req.http.X-Requestctl + ",$name";
}
"""
    )
    header = """
// Set the header to the empty string if not present.
if (!req.http.X-Requestctl) {
    set req.http.X-Requestctl = "";
}
"""

    @classmethod
    def render(cls, data: List[Entity], object_type: str = "") -> str:
        out = [cls.header]
        for action in sorted(data, key=lambda k: k.name):
            # TODO: Check vcl_expression is there?
            substitutions = dict(
                name=action.name,
                comment=action.comment,
                pprint=action.pprint(),
                reason=action.resp_reason,
                status=action.resp_status,
                expression=action.vcl_expression,
                retry_after=max(1, action.throttle_duration),
                driver="etcd",  # TODO: get this from configuration
            )
            if not action.enabled and object_type == "commit":
                # If we get here, it's because the action has log_matching set to true
                # We only want to use the log action when committing.
                # Otherwise, we still want to show the full vcl output with the actions included.
                out.append(cls.tpl_log_only.substitute(substitutions))
            elif action.do_throttle:
                substitutions["throttle"] = cls.get_throttle(action)
                out.append(cls.tpl_throttle.substitute(substitutions))
            else:
                out.append(cls.tpl_ban.substitute(substitutions))
        return "\n".join(out)

    @classmethod
    def get_throttle(cls, action: Entity) -> str:
        """Throttle rule for an action."""
        key = f'"requestctl:{action.name}"'
        if action.throttle_per_ip:
            key = f'"requestctl:{action.name}:" + req.http.X-Client-IP'
        args = [
            key,
            str(action.throttle_requests),
            f"{action.throttle_interval}s",
            f"{action.throttle_duration}s",
        ]
        return f"vsthrottle.is_denied({', '.join(args)})"


class VSLView(View):
    """Outputs the varnishlog command to match requests corresponding to an action."""

    tpl_log = Template(
        """
You can monitor requests matching this action using the following command:
sudo varnishncsa -n frontend -g request \\
  -F '"%{X-Client-IP}i" %l %u %t "%r" %s %b "%{Referer}i" "%{User-agent}i" "%{X-Public-Cloud}i"' \\
  -q '$vsl and not VCL_ACL eq "MATCH wikimedia_nets"'
"""
    )

    @classmethod
    def render(cls, data: List[Entity], _: str = "") -> str:
        return cls.tpl_log.substitute(vsl=data[0].vsl_expression)


class HaProxyDSLView(View):
    """Renders an action as HaProxy configuration."""

    acl_header = "# ACLs generated for requestctl actions"

    fragment_header = """
# requestctl get haproxy_action $pprint
#   Description: $comment
#   Expression: $requestctl_expression
#   Action when enabled: $verb
$extra_header"""

    fragment_instructions_to_disable = """
# This filter is generated from data in $driver. To disable it, run the following command:
# sudo requestctl disable -s haproxy '$pprint'"""

    fragment_instructions_to_enable = """
# This filter is DISABLED. To enable it, run the following command:
# sudo requestctl enable -s haproxy '$pprint'
# The stanza below is only for logging purposes."""

    fragment_set_x_requestctl = """
$before_rule
http-request set-header x-requestctl "%[req.fhdr(x-requestctl),add_item(',',,' hap:$name')]" if $xrequestctl_marking_expression"""  # noqa: E501

    tpl_header_when_enabled = Template(
        fragment_header + fragment_instructions_to_disable + fragment_set_x_requestctl
    )

    fragment_do_action = """
http-request $verb if $expression"""

    tpl_action = Template(tpl_header_when_enabled.template + fragment_do_action)

    tpl_action_log_only = Template(
        fragment_header + fragment_instructions_to_enable + fragment_set_x_requestctl
    )

    # Specifically for per-ip concurrency enforcement.  The lines of the horror below do this:
    # 1. Produce a JSON-formatted event logging message into a temporary variable.
    #    (Be extremely careful about quoting when modifying the set-var-fmt line!)
    # 2. Use debug() to emit that message to the configured haproxy_ring_name.
    #    (This uses set-var on a dummy variable because it has to lol)
    # 3. Increment the corresponding general purpose counter object, for hysteresis/debouncing:
    #    we will log only one message per the defined period of the gpc_rate().
    fragment_log_excursion = """
# Log one debugging message only for the first limit excursion in any gpc_rate() period.
http-request set-var-fmt(req.dummy_$safe_name) '{"action":"hap:$safe_name","src":"%[src]","perip_concur": %[sc0_trackers(httpreqrate)],"enforcement":${enabled_jsonbool},"hapreqid":"%ID"}' if $log_excursion_expression
http-request set-var(req.dummy) var(req.dummy_$safe_name),debug(${safe_name},${haproxy_ring}) if $log_excursion_expression
http-request sc-inc-gpc(${gpcidx},0) if $log_excursion_expression"""  # noqa: E501

    @staticmethod
    def symbolics_all_of(*args) -> str:
        """Return a sympy string of the logical AND of all the arguments."""
        return "&".join(f"({a})" for a in args)

    @classmethod
    def render(cls, data: List[Entity], object_type: str) -> str:
        # Please note we're abusing the object_type parameter here
        # to import ACL definitions
        out = [cls.acl_header, object_type]
        for action in sorted(data, key=lambda k: k.name):
            safe_name = action.name.replace("/", "_")
            status = action.resp_status
            reason = action.resp_reason
            substitutions = dict(
                name=action.name,
                comment=action.comment,
                pprint=action.pprint(),
                reason=reason,
                status=status,
                requestctl_expression=" ".join(action.parsed_expression),
                expression=action.haproxy_expression,
                xrequestctl_marking_expression=action.haproxy_expression,
                driver="etcd",  # TODO: get this from configuration
                before_rule="",
                extra_header="",
                safe_name=safe_name,
                haproxy_ring=action.config.requestctl().haproxy_ring_name,
                enabled_jsonbool=str(action.enabled).lower(),
            )

            def add_extra_header(s: str) -> None:
                substitutions["extra_header"] += f"#   {s}"

            if action.bw_throttle:
                substitutions["before_rule"] = (
                    f"filter bwlim-out {safe_name} "
                    f"limit {action.bw_throttle_rate} period {action.bw_throttle_duration} key src"
                )
                substitutions["verb"] = f"set-bandwidth-limit {safe_name}"
            elif action.silent_drop:
                substitutions["verb"] = "silent-drop"
            else:
                substitutions["verb"] = (
                    f'deny status {status} content-type text/plain string "{reason}"'
                )

            if action.per_ip_concurrency:
                if not (action.enabled or action.log_matching):
                    pass

                add_extra_header("This action tracks per-IP concurrent requests.")

                # For per-ip concurrency enforcement, we need to build additional ACLs,
                # and we need a few different actions that trigger under different conditions.
                # Name the ACLs, then generate them into $before_rule.
                acl_too_high_now = f"{safe_name}__too_high_now"
                acl_too_high_recently = f"{safe_name}__too_high_recently"
                gpcidx = action.per_ip_concurrency_counter_index
                concur_limit = action.per_ip_concurrency_limit
                substitutions["gpcidx"] = gpcidx
                substitutions["concur_limit"] = concur_limit
                substitutions["before_rule"] = "\n".join(
                    [
                        (
                            f"acl {acl_too_high_now} sc0_trackers(httpreqrate) ge {concur_limit}"
                            "  # per-IP concurrent requests threshold"
                        ),
                        (
                            f"acl {acl_too_high_recently} sc_gpc_rate({gpcidx},0,httpreqrate) gt 0"
                            "  # iff we exceeded the threshold in the last rate period"
                        ),
                    ]
                )
                # Now we need to compute various derivative triggering conditions based upon
                # the user's input expression and the ACLs we just defined.

                def safe_name_to_sympy(s: str) -> str:
                    """sympy interprets - as subtraction"""
                    return HAProxyExpression.to_symbol([s])

                sympy_expressions = dict(
                    xrequestctl_marking_expression=cls.symbolics_all_of(
                        action.symbolic_expression, safe_name_to_sympy(acl_too_high_now)
                    ),
                    log_excursion_expression=cls.symbolics_all_of(
                        action.symbolic_expression,
                        safe_name_to_sympy(acl_too_high_now),
                        f"~{safe_name_to_sympy(acl_too_high_recently)}",
                    ),
                    expression=cls.symbolics_all_of(
                        action.symbolic_expression, safe_name_to_sympy(acl_too_high_recently)
                    ),
                )
                # Now convert those sympy expressions back into haproxy expressions.
                # Which we will then use in our actions.
                substitutions.update(
                    {
                        k: HAProxyExpression.normalize_symbolic_to_haproxy(v)
                        for k, v in sympy_expressions.items()
                    }
                )
                if action.enabled:
                    tpl = cls.tpl_header_when_enabled
                else:
                    tpl = cls.tpl_action_log_only
                tpl = Template(tpl.template + cls.fragment_log_excursion)
                if action.enabled:
                    tpl = Template(tpl.template + cls.fragment_do_action)
                out.append(tpl.substitute(substitutions))
            elif action.enabled:
                out.append(cls.tpl_action.substitute(substitutions))
            elif action.log_matching:
                out.append(cls.tpl_action_log_only.substitute(substitutions))
            else:
                # This should only happen when we're trying to see the produced
                # haproxy configuration.
                out.append(cls.tpl_action.substitute(substitutions))

        return "\n".join(out)
