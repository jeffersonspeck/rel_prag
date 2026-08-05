import sys

from clients import heritage_system, navigation_system


class _Response:
    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict[str, str]:
        return {"status": "ok"}


def _capture_payload(monkeypatch, module) -> dict:
    captured = {}

    def fake_post(url, *, json, timeout):
        captured.update({"url": url, "json": json, "timeout": timeout})
        return _Response()

    monkeypatch.setattr(module.httpx, "post", fake_post)
    monkeypatch.setattr(sys, "argv", [module.__file__])
    module.main()
    return captured["json"]


def test_external_clients_submit_only_the_api_contract(monkeypatch):
    navigation = _capture_payload(monkeypatch, navigation_system)
    heritage = _capture_payload(monkeypatch, heritage_system)

    expected_fields = {"ontology_id", "entity_id", "policy_id", "descriptor_values"}
    assert set(navigation) == expected_fields
    assert set(heritage) == expected_fields
    assert navigation["policy_id"] == "navigation-v1"
    assert heritage["policy_id"] == "preservation-v1"
