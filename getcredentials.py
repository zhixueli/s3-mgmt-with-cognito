# the script below demonstate the scenario for a cognito user to
# get the aws temporary credentials for using aws services, 3 steps:
# 1. login with user/password
# 2. get identiry id
# 3. get aws temporary credentials

import boto3

# required parameters
user_name = "xxxx"
password = "xxxx"
# the client id can be retrieved from AWS console -> Amazon Cognito -> User pools -> [UserPoolName] -> App integration -> App client list
# or AWS cli: aws cognito-idp list-user-pool-clients --user-pool-id [user pool id]  --region [aws region code]
client_id = '3rp94lm9nqj0uv39kb2pxxxxxx'
# the identity pool id can be retrieved from AWS console -> Amazon Cognito -> Identity pools -> [IdentityPoolName] -> Identity pool overview
# or AWS cli: aws cognito-identity list-identity-pools --region [aws region code]
identity_pool_id='us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx'
# the user pool id can be retrieved from AWS console -> Amazon Cognito -> User pools -> [UserPoolName] -> User pool overview
# or AWS cli: aws cognito-idp list-user-pools --region [aws region code]
user_pool_id = 'us-east-1_xxxxxxxxx'
region_name = 'us-east-1'
account_id = "123456789012"

auth_data = { 'USERNAME': user_name , 'PASSWORD': password }
provider_client = boto3.client('cognito-idp', region_name=region_name)

# use user/password to login first to get the id token with initiate_auth action
# golang sdk: https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/cognitoidentityprovider#Client.InitiateAuth
# aws api: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_InitiateAuth.html 
resp = provider_client.initiate_auth(
    AuthFlow='USER_PASSWORD_AUTH', 
    AuthParameters=auth_data, 
    ClientId=client_id
)

user_token = resp['AuthenticationResult']['IdToken']
#print('user_token:', user_token)

# use the id token to get the cognito identity id with get_id action
# golang sdk: https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/cognitoidentity#Client.GetId
# aws api: https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_GetId.html
identity_client = boto3.client('cognito-identity',region_name=region_name)
response = identity_client.get_id(
    AccountId=account_id,
    IdentityPoolId=identity_pool_id,
    Logins={
        'cognito-idp.'+region_name+'.amazonaws.com/'+user_pool_id: user_token
    }
)

identity_id = response['IdentityId']
#print('identity_id:', identity_id)

# use the cognito identity id to get the aws temporary credentials with get_credentials_for_identity action
# golang sdk: https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/cognitoidentity#Client.GetCredentialsForIdentity
# aws api: https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_GetCredentialsForIdentity.html
response = identity_client.get_credentials_for_identity(
    IdentityId=identity_id,
    Logins={
        'cognito-idp.'+region_name+'.amazonaws.com/'+user_pool_id: user_token
    }
)

#print(response)

# use aws temporary credentials to access amazon s3 service
s3_client = boto3.client(
    's3',
    aws_access_key_id=response['Credentials']['AccessKeyId'],
    aws_secret_access_key=response['Credentials']['SecretKey'],
    aws_session_token=response['Credentials']['SessionToken']
)

# delete object
response = s3_client.delete_object(
    Bucket='[bucke_name]',
    Key=user_name + '/' + '[file_name]'
)

print(response)

# put object
response = s3_client.put_object(
    Body='[file_name]',
    Bucket='[bucke_name]',
    Key=user_name + '/' + '[file_name]'
)

print(response)

# list objects in given path
response = s3_client.list_objects(
    Bucket='[bucke_name]',
    Prefix=user_name + '/'
)

print(response)