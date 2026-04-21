import tempfile
from pathlib import Path

import app as app_module


def test_health_stats_and_items(monkeypatch):
    tmp = tempfile.TemporaryDirectory()
    monkeypatch.setattr(app_module, 'DATABASE', Path(tmp.name) / 'test.db')
    flask_app = app_module.create_app()
    flask_app.config.update(TESTING=True)
    client = flask_app.test_client()

    health = client.get('/health')
    assert health.status_code == 200
    assert health.get_json()['status'] == 'ok'

    stats = client.get('/api/stats')
    assert stats.status_code == 200
    assert stats.get_json()

    items = client.get('/api/items')
    assert items.status_code == 200
    assert isinstance(items.get_json(), list)
    assert len(items.get_json()) > 0
    tmp.cleanup()
