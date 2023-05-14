import boto3
import json
import sys
from datetime import timedelta
import time
def lambda_handler(event, context):
    start = time.time()
    
    sqs_client = boto3.client('sqs')
    
    response_instance_data = []
    response_semantic_data = []
    response_linguistic_data = []
    responses = []
    execution_time_worst_case = 0.0
    execution_time_cases = []
    
    response = sqs_client.receive_message(
            QueueUrl="https://sqs.sa-east-1.amazonaws.com/837696339822/fila-saida-jsonglue",
            MaxNumberOfMessages=3, #Configuração 3-1-1 [Soma 5]
            WaitTimeSeconds=0,
        )
        
    print(f"Number of messages received: {len(response.get('Messages', []))}")
    for message in response.get("Messages", []):
        print('Adicionando body na lista de responses: ')
        print(message["Body"])
        responses += json.loads(message["Body"])
        
        
        if json.loads(messages['matcherType']) == "instance":
            response_instance_list += json.loads(message_body)["Full compInstance"]
            print('Response Instance:')
            print(response_linguistic_data)
            print('Tamanho dos dados para calculo do trafego')
            print(sys.getsizeof(response_instance_list))
        elif message_body == "semantic":
            response_semantic_data  += json.loads(message_body)["Full compSemantic"]
            print('Response Semantic:')
           print(response_linguistic_data)
        elif message_body == "linguistic":
            response_linguistic_data += json.dumps(message_body)["Full compLinguistic"]
            print('Response Linguistic:')
            print(response_linguistic_data)


    end = time.time()
    print('Tempo de execução do nó de integração: ' + str(timedelta(seconds=end - start)))


    

    return {
        'body': 'Processamento executado com sucesso'
    }

