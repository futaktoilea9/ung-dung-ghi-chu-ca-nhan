from pathlib import Path


def test_notes_project_has_runtime_guardrails():
    assert Path('README.md').exists()
    assert 'app.db' in Path('.gitignore').read_text(encoding='utf-8')
