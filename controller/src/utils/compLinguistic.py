import sys
sys.path.append('/project/controller/src/')
from utils import sin
from utils import sem
from utils import data
import os


def compLinguisticGraph(graph1, graph2, node_number1, node_number2, file1index, file2index):
    result = []
    tmpLinguistic = []
    aux = []
    # print("Processo " + str(os.getpid())+ " iniciando.")
    for x in range(0, node_number1):
        for y in range(0, node_number2):
            if graph1.nodes[x]['type'] == 'object' or graph2.nodes[y]['type'] == 'object':
                tmpLinguistic.extend([graph1.nodes[x]['name'], None, None])
                tmpLinguistic.extend([graph2.nodes[y]['name'], None, None])
                tmpLinguistic.append(None)
                result.append(tmpLinguistic)
                tmpLinguistic = []
            else:
                tmpLinguistic.append(sin.compJaroWink(graph1, graph2, x, y))
                tmpLinguistic.append('')
                tmpLinguistic.extend('')
                aux.extend([graph1.nodes[x]['name'], "", graph1.nodes[x]['orig']])
                aux.extend([graph2.nodes[y]['name'], "", graph2.nodes[y]['orig']])
                aux.extend(tmpLinguistic)
                result.append(aux)
                aux = []
                tmpLinguistic = []
    # print("Processo " + str(os.getpid())+ " terminou.")
    return [(file1index, file2index), result]
