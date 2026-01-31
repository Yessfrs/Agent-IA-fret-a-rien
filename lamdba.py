from http import HTTPStatus
import boto3

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
table = dynamodb.Table('intereted_informations')

def lambda_handler(event,context):
    try:
        action_group=event['actionGroup']
        function = event['function']
        message_version = event.get('messageVersion',1)
        parameters = event.get('parameters',[])
        
        CustomerName = None
        CustomerEmail = None
        for param in parameters:
            if param['name'] == 'CustomerName':
                CustomerName = param['value']
            if param['name'] == 'CustomerEmail':
                CustomerEmail = param['value']
        item = {
            'CustomerName':CustomerName,
            'CustomerEmail':CustomerEmail
        }
        table.put_item(Item=item)
        print('Item saved successfully.')
        response_body = {
            'TEXT': {
                'body': f'The function {function} was called successfully with parameters: {parameters}'
            }
        }
        action_response = {
            'actionGroup': action_group,
            'function':function,
            'functionResponse': {
                'responseBody': response_body
            }
        }
        response = {
            'response': action_response,
            'messageVersion': message_version
        }
        return response
    except KeyError as e:
        print(f'Missing required field: {str(e)}')
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body':f'Error: {str(e)}'
        }
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body':'Internal Server Error'
        }
            
            