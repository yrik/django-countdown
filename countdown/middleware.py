from datetime import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response


class CountdownMiddleware(object):
    def process_response(self, request, response):

        if request.path in settings.COUNTDOWN_EXCLUDE_URLS:
            return response

        if settings.COUNTDOWN_TARGET_DATE > datetime.now():

            # Allow to login in admin part
            # Allow access to all authentificated users
            if request.path.startswith(reverse('admin:index')) or \
                                    request.user.is_authenticated():
                return response

            td = settings.COUNTDOWN_TARGET_DATE - datetime.now()
            return render_to_response("countdown/countdown.html", {
                    'countdown_sec': td.seconds % 60,
                    'countdown_min': (td.seconds / 60) % 60,
                    'countdown_hour': (td.seconds / (60 * 60) % 24),
                    'countdown_day': (td.days),
                    'STATIC_URL': settings.STATIC_URL,
                })
        else:
            return response
