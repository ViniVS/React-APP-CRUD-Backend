# React-APP-CRUD-Backend

## Como funciona?

Serviços criados:
  - Bucket S3 (Escolhido para armazenar dados NoSQL)
  - Dynamo DB (Banco de dados não relacional)
  - Lambda Function (Para exercer todo tratamento dos dados que chegam)
    *Todos os parametros são passados como HEADER na URL de invocação*
    - userList:
      Busca todas as informações do banco de dados, e retorna body como lista de todos cadastrados
    - updateUser
      Busca o id do usuario requisitado no s3, e faz as devidas alterações, atualiza o arquivo S3 e DynamoDB
    - deleteUser
      Busca o id do usuario requisitado no s3, faz a deleção, atualiza o arquivo e DynamoDB
    - createUser
      Busca o ultimo id no s3, cria uma nova linha com as informações passadas, a atualização no dynamoDB é feita em cima do s3
      
  - API Gateway
    - Criei uma API Gateway como um portão de entrada para receber os dados, todos utilizam a função GET.
