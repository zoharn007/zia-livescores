import boto3

dynamoClient = boto3.client('dynamodb')



key = {
    'name': {'S': 'hey'},
    'ID': {'S': '1'}
}

response = dynamoClient.get_item(TableName = 'users', Key = key)

user = response['Item']

print("Before editing:", user['name']['S'], user['pass']['S'], sep=' ')

user['pass']['S'] = "haha"

# user = {
#     'name': {'S' : 'hey'},
#     'ID': {'S': '1'},
#     'pass': {'S' : 'strr'}
# }

dynamoClient.put_item(Item=user, TableName='users')

dynamoClient.delete_item(TableName = 'users', Key = key)