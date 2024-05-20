# if user want to reset their password for some reason (such as forgot password)
# user need to notify cognito admin to trigger the password reset progress
# how cognito initate the password reset progress for given user:
# aws console: AWS console -> Amazon Cognito -> User pools -> [UserPoolName] -> [User Name] -> Actions -> Reset password
# or aws cli: aws cognito-idp admin-reset-user-password --user-pool-id [user pool id] --username [user name] --region [aws region code]
# after cognito admin initiate the password reset progress for given user
# user will get the password reset email which contains the confirmation code
# and then user could follow the way below to reset their password

import boto3

# required parameters
user_name = "xxxx"
# new password to be set
password_new = "xxxx"
# the client id can be retrieved from AWS console -> Amazon Cognito -> User pools -> [UserPoolName] -> App integration -> App client list
# or AWS cli: aws cognito-idp list-user-pool-clients --user-pool-id [user pool id]  --region [aws region code]
client_id = '3gsq1mhah23uk97h3s6jxxxxxx'
region_name = 'us-east-1'
# the confirmation code sent with password reset email
confirmation_code='xxxxxx'

provider_client = boto3.client('cognito-idp', region_name=region_name)

# use the confirmation code sent with password reset email and set new password with confirm_forgot_password action
# golang sdk: https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service/cognitoidentityprovider#Client.ConfirmForgotPassword
# aws api: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ConfirmForgotPassword.html
response = provider_client.confirm_forgot_password(
    ClientId=client_id,
    Username=user_name,
    ConfirmationCode=confirmation_code,
    Password=password_new
)

print(response)