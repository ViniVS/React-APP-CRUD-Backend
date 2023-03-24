import boto3
import csv
import io 
import uuid
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = 'userlist'
bucket_name = 'crud-user'
file_name = 'Userlist.csv'

def insert_user(varFirstName, varLastName, varEmail, varUserName, varCpfCnpj, varDate):

    # Update CSV file in S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    lines = obj['Body'].read().decode('utf-8').splitlines()
    updated_lines = []
    
    # Get last ID from CSV
    last_line = lines[-1]
    last_id = int(last_line.split(';')[0])
    new_id = last_id + 1
    
    # Append new user to CSV
    new_line = f'{new_id};{varCpfCnpj};{varDate};{varEmail};{varFirstName};{varLastName};{varUserName}'
    lines.append(new_line)
    updated_csv = '\n'.join(lines)
    
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=updated_csv)
    
    
        # Get CSV file from S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    body = obj['Body'].read().decode('utf-8')
    csv_reader = csv.reader(body.split('\n'), delimiter=';')
    # Skip header row
    next(csv_reader)
    for row1 in csv_reader:
        varDate = row1[2]
        print(row1)
    date_str = varDate
    date_obj = datetime.strptime(date_str, "%d%m%Y")
    varDate = date_obj.strftime("%Y-%m-%d")
    
    # Format and insert users into DynamoDB
    table = dynamodb.Table('userlist')
    for row in csv_reader:
        new_id= int(row[0])+ 1,
        varCpfCnpj= row[1],
        varDate= varDate,
        varEmail= row[3],
        varFirstName= row[4],
        varLastName= row[5],
        varUserName= row[6]

        
    table.put_item(
        Item={
            'id': new_id,
            'cpfCnpj': varCpfCnpj,
            'date': varDate,
            'email': varEmail,
            'firstName': varFirstName,
            'lastName': varLastName,
            'userName': varUserName
        }
    )
    return {
        'statusCode': 200,
        "headers":{
                    'Access-Control-Allow-Origin':'*',
                    'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods':'GET,OPTIONS'
        },
        'body': 'Linhas criadas com sucesso!'
    }
    

def get_last_id():
    table = dynamodb.Table(table_name)
    response = table.scan(Select='COUNT')
    return response['Count']
    


def lambda_handler(event, context):
    varFirstName = event['queryStringParameters']['varFirstName']
    varLastName = event['queryStringParameters']['varLastName']
    varEmail = event['queryStringParameters']['varEmail']
    varUserName = event['queryStringParameters']['varUserName']
    varCpfCnpj = event['queryStringParameters']['varCpfCnpj']
    varDate = event['queryStringParameters']['varDate']
    
    return insert_user(varFirstName, varLastName, varEmail, varUserName, varCpfCnpj, varDate)
