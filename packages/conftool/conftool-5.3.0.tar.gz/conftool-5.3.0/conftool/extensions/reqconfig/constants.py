"""Constants used across requestctl."""

# Actions are special entities, we will need to check them constantly
ACTION_ENTITIES = ["action", "haproxy_action"]
ACTION_TO_DSL = {"action": "vcl", "haproxy_action": "haproxy_dsl"}
