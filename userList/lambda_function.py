import boto3
from datetime import datetime
import json
import logging
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("userlist")
    items = table.scan()['Items']
    # Obtendo todos os items do DynamoDB
    list = []
    for i in range(len(items)):
        item = items[i]
        list.append(item)
    
    print(list)
    
    new_list = []
    for item in list:
        item['id'] = str(item['id'])  # Converter o valor de 'id' em string
        new_list.append(item)
    
    print(new_list)
    
    logger.info("\nChanging for website\n")
    
    jsondumps= json.dumps(new_list) 
    status = json.loads(jsondumps)
    
    # Retornando para o front end todos os usuarios por uma lista no DynamoDB
    return {
        'statusCode': 200,
        "headers": {
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Headers':'*',
            'Access-Control-Allow-Methods':'GET,OPTIONS'
        },
        'body': json.dumps(status)
    }
    