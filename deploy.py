from shutil import copyfile
import os

os.mkdir('temp')
copyfile('cognito-idp/group.yaml', 'temp/group.yaml')

with open('cognito-idp/user.yaml', 'r') as user_file :
  user_template = user_file.read()

with open('users.txt', 'r') as user_list :
   for cnt, user_info in enumerate(user_list):
      user, email = user_info.split()
      user_cf = user_template.replace('{{UserName}}', user)
      user_cf = user_cf.replace('{{Password}}', email)
      with open('temp/group.yaml', 'a') as file:
         file.write(user_cf)

