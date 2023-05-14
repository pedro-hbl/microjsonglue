import boto3
import json

sqs = boto3.resource("sqs")
queue = sqs.get_queue_by_name(QueueName="fila-entrada-instancia-jsonglue")
ec2 = boto3.resource('ec2')


def user_data_instance():
    return '''
    #!/bin/bash sudo su cd /project cd controller/src/service python3 instanceService.py
    '''


def user_data_linguistic():
    return '''
    #!/bin/bash sudo su cd /project cd controller/src/service python3 linguisticService.py
    '''


def user_data_semantic():
    return '''
    #!/bin/bash sudo su cd /project cd controller/src/service python3 linguisticService.py
    '''


def process_message(message_body):
    print(f"processing message: {message_body}")
    machine = message_body['machine']
    if message_body['type'].__eq__('instance'):
        user_data = user_data_instance
    elif message_body['type'].__eq__('semantic'):
        user_data = user_data_semantic()
    else:
        user_data = user_data_linguistic()
    container = ec2.create_instances(ImageId='ami-0cb0653c330225024', MinCount=1, MaxCount=1,
                                     SecurityGroupIds=['sg-05d97533208be2ac4'], UserData=user_data,
                                     InstanceType=machine,
                                     SubnetId='subnet-0010dee3578bbd521')

    print('container criado com sucesso')
    print(container)
    pass


if __name__ == "__main__":
    while True:
        messages = queue.receive_messages()
        for message in messages:
            print('Dispatcher: varrendo mensagens')
            message_response = json.loads(message['Messages'][0]['Body'])
            process_message(message_response)
            message.delete()
