import subprocess
import socket
import sys

# colors
bg = ''
G = bg + '\033[32m'
O = bg + '\033[33m'
GR = bg + '\033[37m'
R = bg + '\033[31m'

def ssh_client(socks5_port, host, port, user, password):
    try:
        global soc, payload
        
         # Create a socket connecting to inject_host and inject_port
        inject_host = '127.0.0.1'
        inject_port = '8980'
        
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((inject_host, inject_port))
        
        
        dynamic_port_forwarding = '-CND {}'.format(socks5_port)
        username = user
        password = password
        
        
        payload = f'CONNECT {host}:{port} HTTP/1.0\r\n\r\n'
        
        # Initialize the socket connection
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((inject_host, inject_port))
        soc.send(payload.encode())
        res = soc.recv(8192)
        print(res)
        
        response = subprocess.Popen(
            (
                f'sshpass -p {password} ssh -o "ProxyCommand=nc --proxy {inject_host}:{inject_port} %h %p" {username}@{host} -p {port} -v {dynamic_port_forwarding} ' +
                '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
            ),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        for line in response.stdout:
            line = line.decode().lstrip(r'(debug1|Warning):').strip() + '\r'
            #print(line)
            if 'pledge: proc' in line:
                print(G + 'CONNECTED SUCCESSFULLY' + GR)
                cmdl = subprocess.Popen('su -c am start --user 0 -n com.newtoolsworks.tun2tap/com.newtoolsworks.vpn2share.MainActivity', shell=True)
                
            elif 'Permission denied' in line:
                print(R + 'Access Denied' + GR)
            elif 'Connection closed' in line:
                print(R + 'Connection closed' + GR)
            elif 'Could not request local forwarding' in line:
                print(R + 'Port used by another programs' + GR)
    except Exception as e:
        print(R + '{}{}'.format(e, GR))
    except KeyboardInterrupt:
        sys.exit(0)

f = open('sshacc.txt', 'r').readline().strip('\n').split('@')
host = f[0].split(':')[0]
port = f[0].split(':')[1]
user = f[1].split(':')[0]
password = f[1].split(':')[1]

ssh_client('1080', host, port, user, password)
