try:
    from diagram_to_iac.tools.sec_utils import load_yaml_secrets
except Exception:  # noqa: BLE001
    load_yaml_secrets = None

if load_yaml_secrets:
    try:
        load_yaml_secrets()
    except Exception:  # noqa: BLE001
        pass
