# once the new user was created, the user will need to 
# change the temporary password to a new password before 
# using cognito to get the temporoty credentials

import boto3

# required parameters
user_name = "xxxx"
# the temporary password sent with invitation email
password = 'xxxx'
# new password to be set with the user
password_new = "xxxx"
# the client id can be retrieved from AWS console -> Amazon Cognito -> User pools -> [UserPoolName] -> App integration -> App client list
# or AWS cli: aws cognito-idp list-user-pool-clients --user-pool-id [user pool id]  --region [aws region code]
client_id = '3gsq1mhah23uk97h3s6jxxxxxx'
region_name = 'us-east-1'

provider_client = boto3.client('cognito-idp', region_name=region_name)

# use python sdk (boto3) to change user password(use temporary password login and then use the returned session token to change to new password)
auth_data = { 'USERNAME': user_name , 'PASSWORD': password }

# use temporary password to login first to get the session token with initiate_auth action
# golang sdk: https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/cognitoidentityprovider#Client.InitiateAuth
# aws api: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_InitiateAuth.html 
response = provider_client.initiate_auth(
    AuthFlow='USER_PASSWORD_AUTH', 
    AuthParameters=auth_data, 
    ClientId=client_id
)

session = response['Session']

# then use the returned session token to change to new password with respond_to_auth_challenge action
# golang sdk: https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/cognitoidentityprovider#Client.RespondToAuthChallenge
# aws api: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RespondToAuthChallenge.html
response = provider_client.respond_to_auth_challenge(
    ClientId=client_id,
    ChallengeName='NEW_PASSWORD_REQUIRED',
    Session=session,
    ChallengeResponses={
        "NEW_PASSWORD": password_new,
        "USERNAME": user_name
    }
)

print(response)