import sys
import time
from datetime import timedelta
import boto3
import json
import os
import networkx as nx
from functools import partial

sys.path.append('/project/controller/src/')
from out.responseAdapter import printResults
from utils import compInstance as cp
from utils import data as dt
from utils import grafo as gr
from utils.normalizationModules import removeSpaces, createRandomJSON1, loadNamingStd, \
    cleanString, formatName, formatTime
import sqs_extended_client
import multiprocessing as mp


def auxMultipro(a, x, y):
    b = dt.returnDataList(a, x, y)
    c = dt.returnAver(b)
    d = dt.buildHist(c)
    e = dt.normData(d)
    return e


class InstanceService:
    if __name__ == "__main__":
        sqs_client = boto3.client('sqs')
        sqs_client.large_payload_support = 'jsonglue-sqs-larger-messages'
        sqs_client.always_through_s3 = True
        arguments = sys.argv

        response = sqs_client.receive_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-entrada-instancia-jsonglue',
            MaxNumberOfMessages=1,
        )

        message_response = json.loads(response['Messages'][0]['Body'])

        print(message_response)

        filenum = int(message_response['FilesPerPod']) + 1
        filenum = 3

        if message_response['podNumberInstance'] == 1:
            fileRanges = message_response['rangesPod1']
        else:
            fileRanges = message_response['rangesPod2']

        filenameGlobal = []

        dir_path = r'/project/controller/src/data/test-case-50000/'

        for path in os.scandir(dir_path):
            if path.is_file():
                filenameGlobal.append(path.name)

        print(filenameGlobal)
        startIndex = 0

        start = time.time()
        print('start time instance: ' + str(start))

        filename = []

        # for file in range(5):
        #     filename.append(filenameGlobal[startIndex])
        #     startIndex += 1

        jstring = ""

        graphs_dict = {}  # holds the file name as key and graph as value,  the graph name will be the file name
        graphs_size = {}

        graphs_names = {}  # holds every name of every schema

        # APPEND DATA FILES

        dir_path_data = r'/project/controller/src/data/test-case-50000/'
        filename_data = []
        for path in os.scandir(dir_path_data):
            if path.is_file():
                filename_data.append(path.name)
        data_index = 0
        # for file in range(4 - 0):
        #     filename.append(filename_data[data_index])
        #     data_index += 1
        # filenum += 4

        # filename = ['caso5-file.json', 'caso4-file.json', 'caso5-file.json', 'caso4-file.json']
        filename = ['caso7-file.json', 'caso8-file.json']
        filenum = 3

        print('Filename: ')
        print(filename)
        print('Filenum: ')
        print(filenum)
        for x in range(0, filenum - 1):
            print('Criando grafo com: ')
            print(filename[x])
            graphs_dict.update({filename[x]: nx.Graph()})
            graphs_size.update({filename[x]: 0})

        # MODULO DE NORMALIZACAO ( RODA EM TODOS OS PODS )

        node_number = 0
        do_normalization = True
        if do_normalization:
            for x in range(0, filenum - 1):
                node_number = 0
                try:
                    print('Normalizando arquivo: ')
                    print(filename[x])
                    with open('/project/controller/src/data/test-case-50000/' + filename[x], "r") as f:
                        jstring = f.read()
                    jstring = removeSpaces(jstring)
                    final = gr.Pro(jstring, 0, 0, 0, graphs_dict.get(filename[x]))
                    graphs_size.update({filename[x]: final[3]})
                    print('graphs size')
                    print(graphs_size)
                except FileNotFoundError as e:  # Ja foi verificado, mas vale deixar aqui ainda
                    print(e)
                    print("Arquivo %s nao encontrado." % filename[x])

        std = loadNamingStd()

        controller_leitura_multiprocessada = True

        if controller_leitura_multiprocessada:
            cores = mp.cpu_count()
            files = len(filename)
            if files > cores:
                pool1 = mp.Pool(6)
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
                print(filename)
                print('Arquivo', i, 'iniciado.')
                a = dt.returnDataList(i, graphs_dict[i], graphs_size[i])
                if a is None:
                    dt.applyData2Graph(a, graphs_dict[i], graphs_size[i])
                else:
                    b = dt.returnAver(a)
                    c = dt.buildHist(b)
                    d = dt.normData(c)
                    # print('DADO ANTES DE SER INSERIDO')
                    # print(a)
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
        elif (filenum > 2):
            print('\nComparacao de schemas iniciada.')
            controller_leitura_multiprocessada = False
            if controller_leitura_multiprocessada:
                pool = mp.Pool(mp.cpu_count())
                schemacomb = []
                for x in range(0, filenum - 1):
                    for y in range(x + 1, filenum - 1):
                        schemacomb.append((x, y))
                comp = [pool.apply_async(cp.compInstanceGraph, args=(
                    graphs_dict[filename[x]], graphs_dict[filename[y]], graphs_size[filename[x]],
                    graphs_size[filename[y]], x,
                    y)) for (x, y) in schemacomb]
                comp = [r.get() for r in comp]
                pool.close()
                pool.join()
                for i in comp:
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
                for x in range(0, 2):
                    for y in range(x + 1, filenum - 1):
                        # if x == 0 and y == 1:
                        #     continue
                        header.append(formatName(filename[x]))
                        # print(header)
                        header.append(formatName(filename[y]))

                        comp = cp.compInstanceGraph(graphs_dict[filename[x]], graphs_dict[filename[y]],
                                                    graphs_size[filename[x]],
                                                    graphs_size[filename[y]], x, y)
                        header.append(comp[1])
                        full.append(header)
                        header = []
        else:
            print("Apenas um arquivo foi recebido")

        # print("Printando dados\n")
        # [print(i, end='\n\n') for i in dt.returnDataList(filename[0], graphs_dict[filename[0]], graphs_size[filename[0]])]

        end = time.time()
        print('end time instance: ' + str(end))

        print('formated time: ' + str(formatTime(end - start)))

        end_exec_time = formatTime(end - start)

        print('timeDelta: ' + str(timedelta(seconds=end - start)))
        size = sys.getsizeof(full)
        output_message_body = {'Full compInstance': full, 'matcherType': 'instance', 'executionTime': end_exec_time,
                               'metadataSize': size}
        print('Type da saida: ')
        print(type(output_message_body))
        print(output_message_body)

        output_message_body_json = json.dumps(output_message_body)
        print('Type body json: ')
        print(type(output_message_body_json))
        print(output_message_body_json)
        send_message = sqs_client.send_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-saida-jsonglue',
            DelaySeconds=0,
            MessageAttributes={
                'Header': {
                    'DataType': 'String',
                    'StringValue': 'FileRanges: ' + str(fileRanges)
                }
            },
            MessageBody=output_message_body_json
        )
