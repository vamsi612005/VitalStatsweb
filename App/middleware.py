import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_datetime = timezone.now()
        session_expiry = getattr(settings, 'SESSION_IDLE_TIMEOUT', 1800)  # Default to 30 minutes

        last_activity = request.session.get('last_activity')
        if last_activity:
            session_time = timezone.make_aware(datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f'))
            session_age = (current_datetime - session_time).total_seconds()
            if session_age > session_expiry:
                print(request.session.session_key)
                Session.objects.filter(pk=request.session.session_key).delete()
                request.session.flush()
                logout(request)
                messages.info(request, "Session Expired. Please log in again.")
                return render(request, "Login.html")

        request.session['last_activity'] = current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
