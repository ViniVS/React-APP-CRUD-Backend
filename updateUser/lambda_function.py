import boto3
import csv
import io 
import uuid
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb') 
bucket_name = 'crud-user' 
file_name = 'Userlist.csv'



def lambda_handler(event, context):
    id = str(event['queryStringParameters']['id'])
    varFirstName = event['queryStringParameters']['varfirstName']
    varLastName = event['queryStringParameters']['varlastName']
    varEmail = event['queryStringParameters']['varEmail']
    varUserName = event['queryStringParameters']['varUserName']
    varCpfCnpj = event['queryStringParameters']['varCpfCnpj']
    varDate = event['queryStringParameters']['varDate']
    date_str = varDate
    date_obj = datetime.strptime(date_str, "%d%m%Y")
    varDate = date_obj.strftime("%Y-%m-%d")
    
    new_id = int(id)

    # buscar o item correspondente ao ID informado no DynamoDB
    #try:
    response = dynamodb.get_item(
        TableName='userlist',
        Key={
            'id': {'N': str(new_id)}
        }
    )
    item = response['Item']
    '''    
    except:
        return {
            'statusCode': 500,
            'body': 'Erro ao buscar item no DynamoDB'
        }
    '''
    # atualizar os campos correspondentes com as novas informações
    item['firstName'] = {'S': varFirstName} if varFirstName != '' else item['firstName']
    item['lastName'] = {'S': varLastName} if varLastName != '' else item['lastName']
    item['email'] = {'S': varEmail} if varEmail != '' else item['email']
    item['userName'] = {'S': varUserName} if varUserName != '' else item['userName']
    item['cpfCnpj'] = {'S': varCpfCnpj} if varCpfCnpj != '' else item['cpfCnpj']
    item['date'] = {'S': varDate} if varDate != '' else item['date']



        # atualizar o item no DynamoDB
        #try:
    response = dynamodb.put_item(TableName='userlist',Item=item)
    

    file_obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = file_obj['Body'].read().decode('utf-8')
    
    # Fazer as substituições nos dados do usuário correspondente ao ID
    file_lines = file_content.split('\n')
    for i in range(len(file_lines)):
        if file_lines[i].startswith(str(id)):
            user_data = file_lines[i].split(';')
            if varFirstName:
                user_data[1] = varFirstName
            if varLastName:
                user_data[2] = varLastName
            if varEmail:
                user_data[3] = varEmail
            if varUserName:
                user_data[4] = varUserName
            if varCpfCnpj:
                user_data[5] = varCpfCnpj
            if varDate:
                user_data[6] = varDate
            file_lines[i] = ';'.join(user_data)
            break
    
    # Atualizar o arquivo CSV no S3
    new_file_content = '\n'.join(file_lines)
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=new_file_content)
    return {
        'statusCode': 200,
        "headers":{
                    'Access-Control-Allow-Origin':'*',
                    'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods':'GET,OPTIONS'
        },
        'body': 'Atualizado com sucesso!'
    }