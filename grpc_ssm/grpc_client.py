#!/usr/bin/env python

import os
import time
import grpc

import opac_pb2

SLEEP_TIME = 10

def run():
    channel = grpc.insecure_channel('localhost:5000')

    stub = opac_pb2.AssetServiceStub(channel)

    print("Obtendo o arquivo para ser enviado pelo GRPC")

    file = open('sample.txt', 'rb')

    filename = os.path.basename(getattr(file, 'name', None))

    meta = '{"foo": "bar", "pickles": "blaus"}' # String

    print("Envida os metadados %s para como param metadata." % meta)

    task = stub.add_asset(opac_pb2.Asset(file=file.read(), filename=filename,
                                            type="txt", metadata=meta))

    print("ID da task: %s" % task.id)

    task_state = stub.get_task_state(opac_pb2.TaskId(id=task.id))

    print("Verificando o estado da task: %s" % task_state)

    print("Dormindo por %s segundos..." % SLEEP_TIME)

    time.sleep(SLEEP_TIME) # sleep 10 seconds

    print("Agora vou verificando o estado da task: %s" % task.id)

    task_info = stub.get_asset_info(opac_pb2.TaskId(id=task.id))

    print("Informações da url do asset: %s" % task_info)

    asset = stub.get_asset(opac_pb2.TaskId(id=task.id))

    print("Retornando os dados do Asset: ")

    print((task.id, task_state.state, task_info.url, task_info.url_path, asset))

if __name__ == '__main__':
    run()
