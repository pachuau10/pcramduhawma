from django.utils.deprecation import MiddlewareMixin
from .models import VisitorLog, VisitorCount


class VisitorCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None

        ip = self.get_client_ip(request)
        session_key = request.session.session_key

        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        request.visitor_ip = ip

        if not request.session.get('visited', False):
            request.session['visited'] = True

            visitor_count = VisitorCount.load()
            visitor_count.total_visits += 1

            existing = VisitorLog.objects.filter(ip_address=ip).exists()
            if not existing:
                visitor_count.unique_visitors += 1

            visitor_count.save()

            VisitorLog.objects.create(
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                path=request.path[:500],
                referer=request.META.get('HTTP_REFERER', '')[:500],
                session_key=session_key,
            )

        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')
