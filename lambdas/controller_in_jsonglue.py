from dataclasses import dataclass
import sys
import boto3
import json
import time
from datetime import timedelta


def formatTime(t):
    s = t% 60
    t = t / 60
    m = t % 60
    t = t / 60
    h = t
    return "{:02d}".format(int(h)) + 'h' + "{:02d}".format(int(m)) + 'm' + "{:02d}".format(int(s)) + 's'

def lambda_handler(event, context):
    start = time.time()

    sqs_client = boto3.client('sqs')

    # processos permitidos: half(2 instancias), quarter(4 instancias), full(1 instancia)

    quantidadeDePodsSemantico = 1
    quantidadeDePodsInstancia = 2
    quantidadeDePodsLinguistico = 1

    tamanhoMaquinaSemantica = 't2.micro'
    tamanhoMaquinaInstancia = 't2.micro'
    tamanhoMaquinaLinguistica = 't2.micro'

    semantic_ranges = 0
    semantic_indexes = []

    filenum = 8
    filesPerPod = filenum / quantidadeDePodsInstancia

    message_body = {'FilesPerPod': 8, 'rangesPod1': [0, 4], 'rangesPod2': [4, 8]}
    # DISPARAR MENSAGENS COM METADADOS DE EXECUCAO

    for pods in range(quantidadeDePodsSemantico):
        message_body['type'] = 'semantic'
        message_body['machine'] = tamanhoMaquinaSemantica


        message_body['podNumberSemantic'] = pods + 1
        message_body_json = json.dumps(message_body)
        send_message = sqs_client.send_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/dispatcher-queue',
            DelaySeconds=0,
            MessageBody=message_body_json
        )
        semantic_ranges += 1
        print(send_message['MessageId'])

    instance_ranges = 0
    instance_indexes = []
    for pods in range(quantidadeDePodsInstancia):
        message_body['type'] = 'instance'
        message_body['machine'] = tamanhoMaquinaInstancia

        message_body['podNumberInstance'] = pods + 1
        message_body_json = json.dumps(message_body)
        send_message = sqs_client.send_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/dispatcher-queue',
            DelaySeconds=0,
            MessageBody=message_body_json
        )
        instance_ranges += 1
        print(send_message['MessageId'])

    linguistic_ranges = 0
    linguistic_indexes = []
    for pods in range(quantidadeDePodsLinguistico):
        message_body['type'] = 'linguistic'
        message_body['machine'] = tamanhoMaquinaLinguistica

        message_body['podNumberLinguistic'] = pods + 1
        message_body_json = json.dumps(message_body)
        send_message = sqs_client.send_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/dispatcher-queue',
            DelaySeconds=0,
            MessageBody=message_body_json
        )
        linguistic_ranges += 1
        print(send_message['MessageId'])

    print('Mensagens de Metadado enviadas com Sucesso!')

    return {
        'statusCode': 200,
        'body': 'Processamento Inicial executado com sucesso'
    }
