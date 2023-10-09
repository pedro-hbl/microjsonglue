# Documentação -  microjsonglue 

> Este repositório contém o código fonte e manual para execução dos Serviços do MicroJSONGLUE na Cloud.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

* Você possui instalado a versão mais recente ou `python3.7`
* Instalar requirements.txt do projeto `pip3 install -r requirements.txt`

## 🚀 Simulando a execução na Cloud <microjsonglue>

Para executar o <microjsonglue> em ambiente de nuvem, siga estas etapas:

Acesse e crie uma conta na provedora(AWS):
```
Execute serviços de instância EC2 (AWS Fargate ou AWS EC2) através dos seguintes passos

- Etapa 1: faça login no Console de gerenciamento da AWS

- Etapa 2: selecione o serviço EC2(ou ECS/EKS a depender do caso de uso)

- Etapa 3: iniciar uma instância: Para iniciar uma instância, clique no botão “Iniciar instância” no painel do EC2. Isso o levará ao assistente “Iniciar instância”.

- Etapa 4: escolha uma AMI pública: No assistente “Iniciar instância”, você será solicitado a escolher uma AMI. Para iniciar uma AMI pública, clique na guia “Community AMIs” e pesquise a AMI que deseja iniciar. No nosso caso a AMI para o microjsonglue, será a de ID: ami-0a09b8ca39e355f02 (MicroJSONGlue)

- Etapa 5: configurar sua instância. Após selecionar a AMI, você será solicitado a configurar sua instância. Isso inclui a seleção do tipo de instância, a especificação do número de instâncias a serem executadas e a configuração de grupos de segurança e pares de chaves.

- Etapa 6: revise e execute sua instância. Depois de configurar sua instância, revise os detalhes e clique no botão “Iniciar” para iniciar sua instância.

- Etapa 7: acesse sua instância. Depois de iniciar sua instância, você poderá acessá-la usando SSH ou Área de Trabalho Remota. Para acessar sua instância usando SSH, você 
precisará usar o endereço IP público da instância e seu par de chaves.
```

## ☕ Entendendo o repositório do projeto <microjsonglue>

- A pasta /controller possui a camada de execução dos nós de serviços, estes que são: Instância(controller/out/service/instanceService.py), Semântico(controller/out/service/semanticService.py) e Linguístico(controller/out/service/linguisticService.py).

- A pasta /utils contém todas as funções auxiliares de processamento, que serão invocadas durante a execução dos serviços. Dentre elas, funções de comparação, geração de arquivos, módulo de normalização e movimentações de estruturas de dados.

- A pasta /lambdas contém o código fonte das lambdas de entrada de dados(configuração inicial do sistema) e response_adapter, que receberá os metadados de saída e devolver o grafo bipartido com um merge dos dados. Ambas podem ser executadas em ambiente local ou em cloud(AWS Lambda).

## 📫 Executando as Lambdas em ambiente cloud para o <microjsonglue>
- Pré-requisitos: Filas SQS disponíveis no ambiente. Para isso acesse no console AWS -> Serviço AWS SQS -> Criar Fila -> Tipo Padrão (Utilize uma para o dispatcher e outra para o joiner).

Para executar as lambdas, siga estas etapas:

1. faça login no Console de gerenciamento da AWS.
2. selecione o serviço AWS Lambda.
3. criar função.
4. para configuração basta selecionar a versão mais recente do python.
5. utilize o código fonte descrito na seção anterior e teste pelo console

