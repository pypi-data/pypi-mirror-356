from typing import Optional

from django.http import HttpRequest
from django_hawk.middleware import HawkResponseMiddleware as BaseHawkResponseMiddleware
from mohawk import Receiver


class HawkResponseMiddleware(BaseHawkResponseMiddleware):
    def get_receiver(self, request: HttpRequest) -> Optional["Receiver"]:
        drf_auth = getattr(request, "auth", None)
        if isinstance(drf_auth, Receiver):
            return drf_auth
        return None
