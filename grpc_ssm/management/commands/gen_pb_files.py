# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from grpc.tools import protoc


class Command(BaseCommand):
    help = 'Generate PB Files'

    def handle(self, *args, **options):

        PATH_PB_FILES = 'grpc_ssm'

        try:
            protoc.main((
                '',
                '--proto_path={0}'.format(PATH_PB_FILES),
                '--python_out={0}'.format(PATH_PB_FILES),
                '--grpc_python_out={0}'.format(PATH_PB_FILES),
                '{0}/opac.proto'.format(PATH_PB_FILES)
            ))
        except Exception as e:
            msg = "Error found when generating PB files. Exception: %s"
            self.stdout.write(msg, str(e))
            raise e
