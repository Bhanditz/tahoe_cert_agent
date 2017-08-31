from subprocess import CalledProcessError, STDOUT, Popen, PIPE
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import validators.domain
from .permissions import APIKeyPermission
from django.conf import settings


log = logging.getLogger(__name__)


class DomainActivateView(APIView):
    permission_classes = (APIKeyPermission,)

    def post(self, request, format=None):
        domain = request.data.get('domain')
        if not domain or not validators.domain(domain):
            return Response("Please enter a valid domain", status=status.HTTP_400_BAD_REQUEST)

        log.debug("Calling ansible script for domain {}".format(domain))

        try:
            process = Popen(settings.ANSIBLE_CMD, stdout=PIPE, stderr=STDOUT, shell=True)
            for line in iter(process.stdout.readline, ''):
                log.debug(line)
        except CalledProcessError as e:
            log.error(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_202_ACCEPTED)

domain_activate = DomainActivateView.as_view()
