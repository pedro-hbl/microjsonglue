from colorama import Fore, Back, Style

import boto3
import json


def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')

    response_list = []

    for message_received in sqs_client.receive_message(
            QueueUrl='https://sqs.sa-east-1.amazonaws.com/837696339822/fila-saida-jsonglue',
            MaxNumberOfMessages=6,
    ):
        response_list.append(json.loads(message_received['Messages'][0]['Body']))

    print('Mensagens de Metadado recebidas com Sucesso!')

    print(response_list)

    linguistic_response = []

    semantic_response = []

    instance_response = []

    for i in range(0, 6):
        if 'Full compSemantic' in response_list[i]:
            semantic_response.append(response_list[i])
        elif 'Full compInstance' in response_list[i]:
            instance_response.append(response_list[i])
        elif 'Full compLinguist' in response_list[i]:
            linguistic_response.append(response_list[i])

    # neste ponto as listas de resultado ja estarao populadas

    print(semantic_response)

    print(instance_response)

    print(linguistic_response)

    # group_node1_results(semantic_response, instance_response, linguistic_response)

    # group_node2_results(semantic_response, instance_response, linguistic_response)

    return {
        'statusCode': 200,
        'body': 'Processamento Inicial executado com sucesso'
    }


def printResults(full):
    print('\n')
    for filecomp in full:
        print("             ==================        Schema " + Back.BLACK + Fore.WHITE + filecomp[
            0] + Style.RESET_ALL + ' vs Schema ' + Back.BLACK + Fore.WHITE + filecomp[
                  1] + Style.RESET_ALL + '       ==================\n')
        # print("========        Schema " + filecomp[0] + ' vs Schema ' + filecomp[1] + '       ========\n')
        for comparison in filecomp[2]:
            printAux(comparison)
            print("             ", end="")
            print(comparison[:3], end='')
            print('      -      ', end='')
            print(comparison[3:6], '\n')
            print("            ", comparison[6:len(comparison)])
            print('\n')
        print('\n\n')
        print("Press the <ENTER> key to continue...")
        input()


def printAux(comparison):
    print('               Form' + (' ' * (len(comparison[0]))), end='')
    print('Sem' + (' ' * (len(str(comparison[1])) + 1)), end='')
    print('Orig' + (' ' * (len(str(comparison[2])) + 13)), end='')
    print('Form' + (' ' * (len(comparison[3]))), end='')
    print('Sem' + (' ' * (len(str(comparison[4])) + 1)), end='')
    print('Orig')

#
# def group_node1_results(semantic_response, instance_response, linguistic_response):
#     group_results
