import sys
import time
import networkx as nx
from datetime import timedelta

sys.path.append('/project/controller/src/')

import boto3
import json
import os
import multiprocessing as mp
from functools import partial
from out.responseAdapter import printResults
from utils import compLinguistic as cl
from utils.normalizationModules import removeSpaces, createRandomJSON1, loadNamingStd, auxMultipro, \
    cleanString, formatName, formatTime
from utils import data as dt
from utils import grafo as gr
import sqs_extended_client


class LinguisticService:
    if __name__ == "__main__":
        sqs_client = boto3.client('sqs')
        sqs_client.large_payload_support = 'jsonglue-sqs-larger-messages'
        sqs_client.always_through_s3 = True
        start = time.time()
        arguments = sys.argv

        response = sqs_client.receive_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-linguistica-jsonglue',
            MaxNumberOfMessages=1,
        )

        message_response = json.loads(response['Messages'][0]['Body'])

        filenum = int(message_response['FilesPerPod']) + 1

        if message_response['podNumberLinguistic'] == 1:
            fileRanges = message_response['rangesPod1']
        else:
            fileRanges = message_response['rangesPod2']

        filenameGlobal = []

        dir_path = r'/project/controller/src/data/schemas/'

        for path in os.scandir(dir_path):
            if path.is_file():
                filenameGlobal.append(path.name)

        print(filenameGlobal)
        startIndex = fileRanges[0]

        start = time.time()

        filename = []
        filenum = 9

        # APPEND SCHEMAS

        for file in range(8):
            filename.append(filenameGlobal[startIndex])
            startIndex += 1

        print(filename)
        print(filenum)
        jstring = ""

        graphs_dict = {}  # holds the file name as key and graph as value,  the graph name will be the file name
        graphs_size = {}

        graphs_names = {}  # holds every name of every schema

        for x in range(0, filenum-1):
            graphs_dict.update({filename[x]: nx.Graph()})
            graphs_size.update({filename[x]: 0})

        # MODULO DE NORMALIZACAO ( RODA EM TODOS OS PODS )

        node_number = 0
        for x in range(0, filenum-1):
            node_number = 0
            try:
                with open('/project/controller/src/data/schemas/' + filename[x], "r") as f:
                    jstring = f.read()
                jstring = removeSpaces(jstring)
                final = gr.Pro(jstring, 0, 0, 0, graphs_dict.get(filename[x]))
                graphs_size.update({filename[x]: final[3]})
            except FileNotFoundError:  # Ja foi verificado, mas vale deixar aqui ainda
                print("Arquivo %s nao encontrado." % filename[x])  # Ja criou o filename no dict


        std = loadNamingStd()

        controller_leitura_multiprocessada = False

        if controller_leitura_multiprocessada:
            cores = mp.cpu_count()
            files = len(filename)
            if files > cores:
                pool1 = mp.Pool(cores)
            else:
                pool1 = mp.Pool(files)

            print('Leitura multiprocessada iniciada.')

            for i in filename:
                x = partial(dt.applyData2Graph, graph=graphs_dict[i], nodes=graphs_size[i])
                pool1.apply_async(auxMultipro, args=(i, graphs_dict[i], graphs_size[i]), callback=x)

            pool1.close()
            pool1.join()

            print('Leitura multiprocessada encerrada.')

        else:
            print('Leitura sequencial iniciada.')
            for i in filename:
                print('Arquivo', i, 'iniciado.')
                a = dt.returnDataList(i, graphs_dict[i], graphs_size[i])
                if a == None:
                    dt.applyData2Graph(a, graphs_dict[i], graphs_size[i])
                else:
                    b = dt.returnAver(a)
                    c = dt.buildHist(b)
                    d = dt.normData(c)
                    dt.applyData2Graph(d, graphs_dict[i], graphs_size[i])
                print('Arquivo', i, 'encerrado.')
            print('Leitura sequencial encerrada')

        for i in filename:
            k = graphs_size[i]
            for j in range(0, k):
                graphs_dict[i].nodes[j]['orig'] = graphs_dict[i].nodes[j]['name']
                tmp = cleanString(graphs_dict[i].nodes[j]['name'])
                # graphs_dict[i].nodes[j]['name'] = cleanString(graphs_dict[i].nodes[j]['name'])
                names = tmp.split()
                for x in range(0, len(names)):
                    new = std.get(names[x])
                    if new == None:
                        continue
                    else:
                        names[x] = new
                graphs_dict[i].nodes[j]['name'] = ' '.join(names)

        full = []
        header = []
        comp = []

        if (filenum == 1):
            print("Nao foi passado nenhum arquivo ou os arquivos nao existem.")
        elif (filenum > 2):  # TODO verificar se Jaro-winkler e instance based inicia aqui
            print('\nComparacao de schemas iniciada.')
            controller_leitura_multiprocessada = False
            if controller_leitura_multiprocessada:
                pool = mp.Pool(mp.cpu_count())
                schemacomb = []
                for x in range(0, filenum - 1):
                    for y in range(x + 1, filenum - 1):
                        schemacomb.append((x, y))
                comp = [pool.apply_async(cl.compLinguisticGraph, args=(
                    graphs_dict[filename[x]], graphs_dict[filename[y]], graphs_size[filename[x]],
                    graphs_size[filename[y]], x,
                    y)) for (x, y) in schemacomb]
                comp = [r.get() for r in comp]
                pool.close()
                pool.join()
                for i in comp:  # TODO reescrever usando formatName
                    file1 = filename[i[0][0]]
                    file2 = filename[i[0][1]]
                    a1 = file1.rfind('/', 0)
                    a2 = file2.rfind('/', 0)
                    if a1 == -1:
                        header.append(file1)
                    else:
                        header.append(file1[a1 + 1:len(file1)])
                    if a2 == -1:
                        header.append(file2)
                    else:
                        header.append(file2[a2 + 1:len(file2)])
                    header.append(i[1])
                    full.append(header)
                    header = []
            else:
                for x in range(0, filenum - 1):
                    for y in range(x + 1, filenum - 1):
                        header.append(formatName(filename[x]))
                        header.append(formatName(filename[y]))
                        comp = cl.compLinguisticGraph(graphs_dict[filename[x]], graphs_dict[filename[y]],
                                                      graphs_size[filename[x]],
                                                      graphs_size[filename[y]], x, y)
                        header.append(comp[1])
                        full.append(header)
                        header = []
        else:
            print("Apenas um arquivo foi recebido")

        end = time.time()
        print('end time instance: ' + str(end))

        print('formated time: ' + str(formatTime(end - start)))

        end_exec_time = formatTime(end - start)

        output_message_body = {'Full compLinguistic': full, 'matcherType': 'linguistic', 'executionTime': end_exec_time}

        output_message_body_json = json.dumps(output_message_body)

        #print(output_message_body_json)
        print('timeDelta: ' + str(timedelta(seconds=end - start)))

        print('Tamanho do objeto sin: ')
        print(sys.getsizeof(output_message_body_json))


        send_message = sqs_client.send_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-saida-jsonglue',
            DelaySeconds=0,
            MessageAttributes={
                'Header': {
                    'DataType': 'String',
                    'StringValue': 'objectSize: ' + str(sys.getsizeof(output_message_body_json))
                }
            },
            MessageBody=output_message_body_json
        )
