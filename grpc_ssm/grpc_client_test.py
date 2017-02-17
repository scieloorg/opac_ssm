#coding: utf-8
#!/usr/bin/env python

import os
import time
import grpc

import opac_pb2

SLEEP_TIME = 5

def run():
    ###########################################################################
    # Connect wiht grpc Asset Service
    ###########################################################################

    channel = grpc.insecure_channel('localhost:5000')

    stubAsset = opac_pb2.AssetServiceStub(channel)

    ###########################################################################
    # Teste asset.add_asset
    ###########################################################################

    print("Obtendo o arquivo para ser enviado pelo GRPC")

    file = open('sample.txt', 'rb')

    filename = os.path.basename(getattr(file, 'name', None))

    meta = '{"foo": "bar", "pickles": "blaus"}' # String

    print("Envida os metadados %s como param metadata." % meta)

    task = stubAsset.add_asset(opac_pb2.Asset(file=file.read(), filename=filename,
                                         type="txt", metadata=meta,
                                         bucket="Bucket Sample"))

    ###########################################################################
    # Teste asset.get_task_state
    ###########################################################################

    print("ID da task: %s" % task.id)

    task_state = stubAsset.get_task_state(opac_pb2.TaskId(id=task.id))

    print("Verificando o estado da task: %s" % task_state)

    print("Dormindo por %s segundos..." % SLEEP_TIME)

    time.sleep(SLEEP_TIME) # sleep 10 seconds

    task_state = stubAsset.get_task_state(opac_pb2.TaskId(id=task.id))

    print("Agora vou verificando o estado da task: %s, %s" % (task.id, task_state))

    ###########################################################################
    # Teste asset.get_asset_info
    ###########################################################################

    task_info = stubAsset.get_asset_info(opac_pb2.TaskId(id=task.id))

    print("Informações da url do asset: %s" % task_info)

    ###########################################################################
    # Teste asset.get_asset
    ###########################################################################

    asset = stubAsset.get_asset(opac_pb2.TaskId(id=task.id))

    print("Retornando os dados do Asset: ")

    print((task.id, task_state.state, task_info.url, task_info.url_path, asset))

    ###########################################################################
    # Teste asset.update_asset
    ###########################################################################

    print("Atualizando um asset com o uuid %s" % task.id)

    meta = '{"foo": "updated", "pickles": "updated"}'

    stubAsset.update_asset(opac_pb2.Asset(uuid=asset.uuid, metadata=meta))

    print("Dormindo por %s segundos..." % SLEEP_TIME)

    time.sleep(SLEEP_TIME)

    print("Verificando se uma asset existe pelo uuid: %s" % asset.uuid)

    asset_exists = stubAsset.exists_asset(opac_pb2.TaskId(id=asset.uuid))

    print(asset_exists.exist)

    print("Recuperando os dados do asset com id: %s" % asset.uuid)

    asset = stubAsset.get_asset(opac_pb2.TaskId(id=asset.uuid))

    print(asset)

    ###########################################################################
    # Teste asset.remove_asset
    ###########################################################################

    print("Removendo um asset com o uuid %s" % task.id)

    stubAsset.remove_asset(opac_pb2.TaskId(id=asset.uuid))

    print("Dormindo por %s segundos..." % SLEEP_TIME)

    time.sleep(SLEEP_TIME)

    print("Recuperando os dados do asset com id: %s" % asset.uuid)

    print("Verificando se uma asset existe pelo uuid: %s" % asset.uuid)

    asset_exists = stubAsset.exists_asset(opac_pb2.TaskId(id=asset.uuid))

    print(asset_exists.exist)

    stubBucket = opac_pb2.BucketServiceStub(channel)

    print("Adicionando um novo bucket")

    task = stubBucket.add_bucket(opac_pb2.BucketName(name="Bucket 007"))

    time.sleep(SLEEP_TIME)

    task_state = stubBucket.get_task_state(opac_pb2.TaskId(id=task.id))

    print("Verificando o estado da task: %s" % task_state)

    print("Atualizando um bucket")

    task = stubBucket.update_bucket(opac_pb2.BucketName(name="Bucket 007", new_name="Bucket 008"))

    time.sleep(SLEEP_TIME)

    print("Removendo um bucket")

    task = stubBucket.remove_bucket(opac_pb2.BucketName(name="Bucket 008"))

    time.sleep(SLEEP_TIME)

    print("Verificando se existe um bucket")

    bucket_exists = stubBucket.exists_bucket(opac_pb2.BucketName(name="Bucket 008"))

    print(bucket_exists.exist)

    print("Atualizando um bucket que não existe")

    task = stubBucket.update_bucket(opac_pb2.BucketName(name="Bucket 009", new_name="Bucket 008"))

    time.sleep(SLEEP_TIME)

    print("Atualizando um bucket para um bucket já existente")

    task = stubBucket.add_bucket(opac_pb2.BucketName(name="Bucket 008"))

    task = stubBucket.add_bucket(opac_pb2.BucketName(name="Bucket 009"))

    time.sleep(SLEEP_TIME)

    task = stubBucket.update_bucket(opac_pb2.BucketName(name="Bucket 008", new_name="Bucket 009"))

    print("Removendo um bucket")

    task = stubBucket.remove_bucket(opac_pb2.BucketName(name="Bucket 008"))

    time.sleep(SLEEP_TIME)

    print("Removendo um bucket")

    task = stubBucket.remove_bucket(opac_pb2.BucketName(name="Bucket 009"))

    time.sleep(SLEEP_TIME)

    task = stubBucket.remove_bucket(opac_pb2.BucketName(name="Bucket Sample"))

if __name__ == '__main__':
    run()
