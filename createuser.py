# create a new user in given cognito user pool
# and cognito will send the invitation (with user name and temp password) email

import boto3

# required parameters
user_name = "xxxx"
email = 'someone@company.com'
region_name = 'us-east-1'
# the user pool id can be retrieved from AWS console -> Amazon Cognito -> User pools -> [UserPoolName] -> User pool overview
# or AWS cli: aws cognito-idp list-user-pools --region [aws region code]
user_pool_id = 'us-east-1_xxxxxxxxx'

provider_client = boto3.client('cognito-idp', region_name=region_name)

# use python sdk (boto3) to create user
# golang sdk:https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/cognitoidentityprovider#Client.AdminCreateUser
# aws api: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminCreateUser.html 
response = provider_client.admin_create_user(
    UserPoolId=user_pool_id,
    Username=user_name,
    UserAttributes=[
        {
            'Name': 'email',
            'Value': email
        },
        {
            'Name': 'email_verified',
            'Value': 'True'
        },
    ],
    # comment out the line below for the cases of:
    # 1.user didn't get the invitation email, and needed to resend it again
    # 2.wrong email used, changed to the correct email address and resend the invitation
    #MessageAction='RESEND',
    DesiredDeliveryMediums=[
        'EMAIL',
    ]
)

print(response)