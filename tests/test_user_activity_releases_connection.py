from django.test import Client


def test_user_activity_report_returns_connection_to_pool(fake_report_pool):
    """Regression test for the incident: every request must give its pooled connection back."""
    client = Client()
    for _ in range(5):
        assert client.get("/api/reports/user-activity/").status_code == 200
    stats = fake_report_pool.stats()
    assert stats["in_use"] == 0, f"{stats['in_use']} report connection(s) were never returned to the pool"
    assert stats["opened"] == 1
