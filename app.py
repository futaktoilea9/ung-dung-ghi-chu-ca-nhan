from __future__ import annotations

import os
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

APP_TITLE = 'Ứng Dụng Ghi Chú Cá Nhân'
DATABASE = Path(os.environ.get('APP_DATABASE', Path(__file__).with_name('app.db')))
SCHEMA_SQL = "\nCREATE TABLE IF NOT EXISTS notes (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    title TEXT NOT NULL,\n    content TEXT NOT NULL,\n    tags TEXT DEFAULT '',\n    pinned INTEGER NOT NULL DEFAULT 0,\n    archived INTEGER NOT NULL DEFAULT 0,\n    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,\n    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP\n);\n"
SEED_CODE = "\nnotes = [\n    ('Kế hoạch tuần', 'Hoàn thiện 4 dự án Flask SQLite và cập nhật GitHub', 'work,github', 1, 0),\n    ('Ý tưởng sản phẩm', 'Dashboard theo dõi công việc cá nhân bằng SQLite', 'idea,product', 0, 0),\n    ('Checklist học tập', 'Ôn Flask routing, SQLite schema và pytest', 'learning,python', 0, 0),\n]\nconn.executemany('INSERT INTO notes(title, content, tags, pinned, archived) VALUES (?, ?, ?, ?, ?)', notes)\n"
ITEMS_SQL = 'SELECT id, title, content, tags, pinned, archived, updated_at FROM notes ORDER BY pinned DESC, updated_at DESC LIMIT ?'


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def scalar(sql: str, params: tuple[Any, ...] = ()) -> Any:
    with closing(get_connection()) as conn:
        return conn.execute(sql, params).fetchone()[0]


def query_all(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with closing(get_connection()) as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def execute(sql: str, params: tuple[Any, ...] = ()) -> int:
    with closing(get_connection()) as conn:
        cursor = conn.execute(sql, params)
        conn.commit()
        return int(cursor.lastrowid)


def init_db(seed: bool = True) -> None:
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with closing(get_connection()) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    if seed:
        seed_db()


def seed_db() -> None:
    with closing(get_connection()) as conn:
        table_count = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
        data_count = 0
        for table in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall():
            data_count += conn.execute(f"SELECT COUNT(*) FROM {table['name']}").fetchone()[0]
        if table_count and data_count:
            return
        exec(SEED_CODE, {'conn': conn})
        conn.commit()


def build_stats() -> dict[str, Any]:

    return {
        'notes': scalar('SELECT COUNT(*) FROM notes'),
        'pinned': scalar('SELECT COUNT(*) FROM notes WHERE pinned = 1'),
        'archived': scalar('SELECT COUNT(*) FROM notes WHERE archived = 1'),
        'active': scalar('SELECT COUNT(*) FROM notes WHERE archived = 0'),
    }


def latest_rows(limit: int = 20) -> list[dict[str, Any]]:
    return query_all(ITEMS_SQL, (limit,))


def create_app() -> Flask:
    app = Flask(__name__)
    init_db(seed=True)

    @app.get('/')
    def index():
        return render_template('index.html', title=APP_TITLE, stats=build_stats(), rows=latest_rows())

    @app.get('/health')
    def health():
        return jsonify({'status': 'ok', 'title': APP_TITLE, 'database': str(DATABASE)})

    @app.get('/api/stats')
    def api_stats():
        return jsonify(build_stats())

    @app.get('/api/items')
    def api_items():
        return jsonify(latest_rows(limit=int(request.args.get('limit', 20))))


    @app.post('/api/notes')
    def create_note():
        payload = request.get_json(force=True)
        row_id = execute(
            'INSERT INTO notes(title, content, tags, pinned) VALUES (?, ?, ?, ?)',
            (payload['title'], payload['content'], payload.get('tags', ''), int(payload.get('pinned', False))),
        )
        return jsonify({'id': row_id}), 201
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5003)), debug=True)
