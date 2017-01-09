# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

import grpc

from grpc_ssm import opac_pb2


class Command(BaseCommand):
    help = 'GRCP Client'

    def handle(self, *args, **options):

        channel = grpc.insecure_channel('localhost:5000')

        stub = opac_pb2.AssetServiceStub(channel)

        asset = stub.add_asset(opac_pb2.Asset(file=open('abcd_sample.txt', 'rb').read(), type="txt", metadata="CC-BY"))

        print(asset)
