import os
import sys

import jsongenerator as jg


def createRandomJSON1(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('../../../jsonSchemaMatching/documents') == False: os.system('mkdir documents')
    pth = 'D:/artigo/documents/caso1-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc2(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise


def createRandomJSON2(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('../../../jsonSchemaMatching/documents') == False: os.system('mkdir documents')
    pth = 'D:/artigo/documents/caso2-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc5(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise

def createRandomJSON3(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('../../../jsonSchemaMatching/documents') == False: os.system('mkdir documents')
    pth = 'D:/artigo/documents/caso3-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc3(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise

def createRandomJSON4(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('../../../jsonSchemaMatching/documents') == False: os.system('mkdir documents')
    pth = 'D:/artigo/documents/caso4-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc4(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise

def createRandomJSON5(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('../../../jsonSchemaMatching/documents') == False: os.system('mkdir documents')
    pth = 'D:/artigo/documents/caso5-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc2(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise


def createRandomJSON6(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('../../../jsonSchemaMatching/documents') == False: os.system('mkdir documents')
    pth = 'D:/artigo/documents/caso6-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc5(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise

def createRandomJSON7(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('../../../jsonSchemaMatching/documents') == False: os.system('mkdir documents')
    pth = 'D:/artigo/documents/caso7-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc3(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise

def createRandomJSON8(qnt): # Creates 'qnt' JSON files in documents/ folder
    if os.path.isdir('../../../jsonSchemaMatching/documents') == False: os.system('mkdir documents')
    pth = 'D:/artigo/documents/caso8-file.json'
    if os.path.isfile(pth) == True: os.system('rm '+pth)
    try:
        with open(pth, "w") as f:
            f.write(jg.createDoc4(qnt))
    except:
        print('Erro ao salvar documento JSON em '+ pth + ' .')
        raise


if (__name__ == "__main__"):
    createRandomJSON1(125000)
    createRandomJSON2(125000)
    createRandomJSON3(125000)
    createRandomJSON4(125000)
    createRandomJSON5(125000)
    createRandomJSON6(125000)
    createRandomJSON7(125000)
    createRandomJSON8(125000)
    sys.exit()