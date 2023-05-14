import sys
import time

import boto3
import json
import os
import networkx as nx
from functools import partial

sys.path.append('/project/controller/src/')
from out.responseAdapter import printResults
from utils import compMonolith as cp
from utils import data as dt
from utils import grafo as gr
from utils.normalizationModules import removeSpaces, createRandomJSON1, loadNamingStd, auxMultipro, \
    cleanString, formatName, formatTime
import sqs_extended_client


class InstanceService:
    if __name__ == "__main__":
        import multiprocessing as mp

        filenum = 11

        filenameGlobal = []

        dir_path = r'/project/controller/src/data/schemas/'

        for path in os.scandir(dir_path):
            if path.is_file():
                filenameGlobal.append(path.name)

        print(filenameGlobal)
        startIndex = 0

        start = time.time()
        print('start time instance: ' + str(start))

        filename = []

        for file in range(11):
            filename.append(filenameGlobal[startIndex])
            startIndex += 1

        jstring = ""

        graphs_dict = {}  # holds the file name as key and graph as value,  the graph name will be the file name
        graphs_size = {}

        graphs_names = {}  # holds every name of every schema

        # APPEND DATA FILES

        dir_path_data = r'/project/controller/src/data/schemas/'
        filename_data = []
        for path in os.scandir(dir_path_data):
            if path.is_file():
                filename_data.append(path.name)
        data_index = 0
        # for file in range(4 - 0):
        #     filename.append(filename_data[data_index])
        #     data_index += 1
        # filenum += 4

        print('Filename: ')
        print(filename)

        print('Filenum: ')
        print(filenum)
        for x in range(0, filenum):
            print('Criando grafo com: ')
            print(filename[x])
            graphs_dict.update({filename[x]: nx.Graph()})
            graphs_size.update({filename[x]: 0})

        # MODULO DE NORMALIZACAO ( RODA EM TODOS OS PODS )

        node_number = 0
        do_normalization = True
        if do_normalization:
            for x in range(0, filenum):
                node_number = 0
                try:
                    print('Normalizando arquivo: ')
                    print(filename[x])
                    with open('/project/controller/src/data/schemas/' + filename[x], "r") as f:
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
                schemacomb = []
                for x in range(0, filenum - 1):
                    for y in range(x + 1, filenum - 1):
                        schemacomb.append((x, y))
                print('cpu count')
                print(mp.cpu_count())
                poolNew = mp.Pool(processes=mp.cpu_count())
                comp = [poolNew.apply_async(cp.compInstanceGraph, args=(
                    graphs_dict[filename[x]], graphs_dict[filename[y]], graphs_size[filename[x]],
                    graphs_size[filename[y]],
                    x, y)) for (x, y) in schemacomb]
                comp = [r.get() for r in comp]
                poolNew.close()
                poolNew.join()
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
                range_inicio_instancia = 0
                range_fim_instancia = 3
                inicio_second_range = 0
                for x in range(0, filenum-1):
                    for y in range(x + 1, filenum-1):
                        header.append(formatName(filename[x]))
                        # print(header)
                        header.append(formatName(filename[y]))

                        comp = cp.compGraph(graphs_dict[filename[x]], graphs_dict[filename[y]],
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

        print('formated time: ' + str(formatTime(end - start)))

        end_exec_time = formatTime(end - start)

        output_message_body = {'Full compInstance': full, 'matcherType': 'instance', 'executionTime': end_exec_time}
        print('Saida: ')
        print(output_message_body)
