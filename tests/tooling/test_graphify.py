"""Unit tests for _shared/scripts/graphify.py."""

import sqlite3
import pytest
from pathlib import Path
from _shared.scripts.graphify import generate_graph


def test_generate_graph(tmp_path):
    repo_root = Path.cwd()
    out_dir = tmp_path / "graphify-out"
    output_md = tmp_path / "ARCHITECTURE.md"

    stats = generate_graph(repo_root, out_dir, output_md)

    assert stats["total_domains"] == 9
    assert stats["total_agents"] == 100
    assert stats["total_nodes"] > 700
    assert stats["total_edges"] > 700

    # Verify SQLite DB
    db_path = Path(stats["sqlite_path"])
    assert db_path.exists()
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    domains_count = cur.execute("SELECT COUNT(*) FROM nodes WHERE type = 'Domain'").fetchone()[0]
    agents_count = cur.execute("SELECT COUNT(*) FROM nodes WHERE type = 'Agent'").fetchone()[0]
    tables_count = cur.execute("SELECT COUNT(*) FROM nodes WHERE type = 'BigQueryTable'").fetchone()[0]
    
    assert domains_count == 9
    assert agents_count == 100
    assert tables_count >= 390
    
    conn.close()

    # Verify JSON graph
    json_path = Path(stats["json_path"])
    assert json_path.exists()
