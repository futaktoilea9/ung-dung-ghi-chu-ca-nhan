from pathlib import Path


def test_project_documentation_exists():
    assert Path('README.md').exists()
    assert Path('docs').exists()


def test_runtime_database_is_ignored():
    assert 'app.db' in Path('.gitignore').read_text(encoding='utf-8')


def test_project_marker_2():
    assert 'Ứng Dụng Ghi Chú Cá Nhân'
