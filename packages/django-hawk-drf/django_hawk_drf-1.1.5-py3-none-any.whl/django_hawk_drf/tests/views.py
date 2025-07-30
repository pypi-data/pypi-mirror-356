from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django_hawk_drf.authentication import HawkAuthentication


class ExampleViewSet(ViewSet):
    authentication_classes = (HawkAuthentication,)
    permission_classes = ()

    def list(self, request):
        return Response([])
