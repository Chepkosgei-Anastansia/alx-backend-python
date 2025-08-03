import logging
from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("user_requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response



class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed time range (6PM to 9PM)
        self.start_time = time(18, 0, 0)  # 6:00 PM
        self.end_time = time(21, 0, 0)    # 9:00 PM

    def __call__(self, request):
        now = datetime.now().time()

        if not (self.start_time <= now <= self.end_time):
            return HttpResponseForbidden(
                "<h1>Access to the messaging app is restricted between 9:00 PM and 6:00 PM.</h1>"
            )

        return self.get_response(request)



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Track message timestamps by IP
        self.ip_message_log = defaultdict(list)
        self.time_window = timedelta(minutes=1)
        self.max_messages = 5

    def __call__(self, request):
        # Only rate-limit POSTs to /api/messages/
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean up old entries beyond 1 minute
            recent_timestamps = [
                t for t in self.ip_message_log[ip] if now - t < self.time_window
            ]
            self.ip_message_log[ip] = recent_timestamps

            # Check if limit exceeded
            if len(recent_timestamps) >= self.max_messages:
                return HttpResponseForbidden(
                    "<h3>Rate limit exceeded: Only 5 messages allowed per minute per IP.</h3>"
                )

            # Log this request
            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Gets the real client IP from headers or remote address.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
    


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define roles that are allowed
        self.allowed_roles = ['admin', 'moderator']

    def __call__(self, request):
        # Only check authenticated users
        if request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)
            restricted_paths = [
                "/api/messages/",
                "/api/conversations/",
                "/admin-only-endpoint/"
            ]

            # Apply restriction only to sensitive paths (optional)
            if any(request.path.startswith(p) for p in restricted_paths):
                if user_role not in self.allowed_roles:
                    return HttpResponseForbidden(
                        "<h3>Access denied: You must be an admin or moderator to access this resource.</h3>"
                    )

        return self.get_response(request)


