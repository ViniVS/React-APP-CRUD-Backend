import boto3
import csv
import io

s3 = boto3.client('s3')
bucket_name = 'crud-user' 
file_name = 'Userlist.csv'
dynamodb = boto3.resource('dynamodb')
table_name = 'userlist'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # obter o id da query string
    id = str(event['queryStringParameters']['id'])
    new_id = int(id)

    # obter o objeto S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)

    # ler o conteúdo do arquivo csv
    lines = obj['Body'].read().decode('utf-8').splitlines()

    # criar um arquivo temporário para armazenar as linhas atualizadas
    updated_lines = []

    delimiter = ';'
    
    # iterar sobre as linhas do arquivo csv
    for line in csv.reader(lines, delimiter=';'):
        # verificar se o primeiro elemento da linha é igual ao id
        if line[0] == id:
            # se sim, pular a linha e continuar para a próxima linha
            table.delete_item(
                Key={
                    'id': new_id
                }
            )
            continue

        # adicionar a linha ao arquivo temporário, exceto se for a linha a ser removida
        updated_lines.append(line)

    # converter as linhas atualizadas em uma string csv
    updated_csv = '\n'.join([delimiter.join(line) for line in updated_lines])

    # atualizar o arquivo no S3
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=updated_csv)

    return {
        'statusCode': 200,
        "headers":{
                    'Access-Control-Allow-Origin':'*',
                    'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods':'GET,OPTIONS'
        },
        'body': 'Linha removida com sucesso!'
    }