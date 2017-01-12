# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings

from grpc_ssm import grpc_server

class Command(BaseCommand):
    help = 'GRCP Server'

    def handle(self, *args, **options):

        self.stdout.write("Starting GRPC...")

        grpc_server.serve(settings.GRCP_HOST, settings.GRCP_PORT,
                          settings.GRCP_MAX_WORKERS)
