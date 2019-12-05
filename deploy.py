from shutil import copyfile,rmtree
import boto3
import os

cf = boto3.client('cloudformation')

def parse_template(template_file):
    with open(template_file) as template:
        template_data = template.read()
    cf.validate_template(TemplateBody=template_data)
    return template_data


os.mkdir('temp')
copyfile('cognito-idp/group.yaml', 'temp/group.yaml')

with open('cognito-idp/user.yaml', 'r') as user_file :
 user_template = user_file.read()

with open('users.txt', 'r') as user_list :
   for cnt, user_info in enumerate(user_list):
      user, email = user_info.split()
      user_cf = user_template.replace('{{UserName}}', user)
      user_cf = user_cf.replace('{{Password}}', email)
      user_cf = user_cf.replace('{{index}}', str(cnt))
      with open('temp/group.yaml', 'a') as file:
         file.write(user_cf)

response = cf.create_stack(
   StackName='cognito-idp-group',
   TemplateBody=parse_template('temp/group.yaml'),
   Capabilities=[
      'CAPABILITY_NAMED_IAM'
   ],
   Tags=[
      {
         'Key': 'project',
         'Value': 'aws-accounts'
      }
   ]
)
print(response)

rmtree('temp')
