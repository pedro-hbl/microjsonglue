import sys
sys.path.append('/project/controller/src/')
from utils import sin
from utils import sem
from utils import data
import os

def compSemanticGraph(graph1, graph2, node_number1, node_number2, file1index, file2index):
    result = []
    tmpSemantic = []
    aux = []
    # print("Processo " + str(os.getpid())+ " iniciando.")
    for x in range(0, node_number1):
        for y in range(0, node_number2):
            if graph1.nodes[x]['type'] == 'object' or graph2.nodes[y]['type'] == 'object':
                tmpSemantic.extend([graph1.nodes[x]['name'], None, None])
                tmpSemantic.extend([graph2.nodes[y]['name'], None, None])
                tmpSemantic.append(None)
                result.append(tmpSemantic)
                tmpSemantic = []
            else:
                tmpSemantic.append('')
                tmpSemantic.append(sem.wupSim(graph1, graph2, x, y))
                tmpSemantic.extend('')
                aux.extend([graph1.nodes[x]['name'], graph1.nodes[x]['comp'], graph1.nodes[x]['orig']])
                aux.extend([graph2.nodes[y]['name'], graph2.nodes[y]['comp'], graph2.nodes[y]['orig']])
                aux.extend(tmpSemantic)
                result.append(aux)
                aux = []
                tmpSemantic = []
    # print("Processo " + str(os.getpid())+ " terminou.")
    return [(file1index, file2index), result]
