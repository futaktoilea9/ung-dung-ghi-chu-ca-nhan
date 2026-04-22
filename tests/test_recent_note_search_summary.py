from services.metrics import recent_note_search_summary


def test_recent_note_search_summary_contains_recent_queries():
    summary = recent_note_search_summary()
    assert len(summary['recent_queries']) >= 1
    assert summary['saved_notes'] >= 0
