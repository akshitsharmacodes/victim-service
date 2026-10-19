from django.http import JsonResponse

from .models import UserActivity
from .pool import report_pool


def health(request):
    return JsonResponse({"status": "ok", "service": "victim-service"})


def top_pages(request):
    """Most viewed pages, computed with raw SQL through the reporting pool."""
    with report_pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT page, COUNT(*) AS views FROM analytics_useractivity "
            "GROUP BY page ORDER BY views DESC LIMIT 10"
        )
        rows = cursor.fetchall()
    return JsonResponse({"pages": [{"page": r[0], "views": r[1]} for r in rows]})


def metrics_summary(request):
    """Headline numbers computed with the ORM."""
    return JsonResponse({
        "status": "success",
        "total_events": UserActivity.objects.count(),
        "unique_users": UserActivity.objects.values("user_id").distinct().count(),
    })
