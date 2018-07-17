# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings

from grpc_ssm import grpc_server


class Command(BaseCommand):
    help = 'GRCP Server'

    def handle(self, *args, **options):

        self.stdout.write("[info] GRPC_MAX_RECEIVE_MESSAGE_LENGTH: {0}".format(settings.GRPC_MAX_RECEIVE_MESSAGE_LENGTH))
        self.stdout.write("[info] GRPC_MAX_SEND_MESSAGE_LENGTH: {0}".format(settings.GRPC_MAX_SEND_MESSAGE_LENGTH))
        self.stdout.write("[info] Listening GRPC... Host: {0}, Port: {1}".format(
                          settings.GRCP_HOST, settings.GRCP_PORT))

        grpc_server.serve(
            host=settings.GRCP_HOST,
            port=settings.GRCP_PORT,
            max_workers=settings.GRCP_MAX_WORKERS,
            max_receive_message_length=settings.GRPC_MAX_RECEIVE_MESSAGE_LENGTH,
            max_send_message_length=settings.GRPC_MAX_SEND_MESSAGE_LENGTH)
