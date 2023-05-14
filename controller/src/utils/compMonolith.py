import sys
sys.path.append('/project/controller/src/')
from utils import sin
from utils import sem
from utils import data
import os


def compGraph(graph1, graph2, node_number1, node_number2, file1index, file2index):
    result = []
    tmpInstance = []
    aux = []
    # print("Processo " + str(os.getpid())+ " iniciando.")
    for x in range(0, node_number1):
        for y in range(0, node_number2):
            if graph1.nodes[x]['type'] == 'object' or graph2.nodes[y]['type'] == 'object':
                tmpInstance.extend([graph1.nodes[x]['name'], None, None])
                tmpInstance.extend([graph2.nodes[y]['name'], None, None])
                tmpInstance.append(None)
                result.append(tmpInstance)
                tmpInstance = []
            else:
                tmpInstance.append(sin.compJaroWink(graph1, graph2, x, y))
                tmpInstance.append(sem.wupSim(graph1, graph2, x, y))
                tmpInstance.extend([data.compData(graph1, graph2, x, y)])
                aux.extend([graph1.nodes[x]['name'], graph1.nodes[x]['comp'], graph1.nodes[x]['orig']])
                aux.extend([graph2.nodes[y]['name'], graph2.nodes[y]['comp'], graph2.nodes[y]['orig']])
                aux.extend(tmpInstance)
                result.append(aux)
                aux = []
                tmpInstance = []
    # print("Processo " + str(os.getpid())+ " terminou.")
    return [(file1index, file2index), result]