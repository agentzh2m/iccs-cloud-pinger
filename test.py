import subprocess
def ssh_cmd(host, cmd):
    ssh = subprocess.run(['ssh',
                          '-o', 'StrictHostKeyChecking=no',
                          ] + [host] + cmd,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ssh.returncode == 0:
        return ssh.stdout.decode('utf-8').strip()
    else:
        return ssh.stderr.decode('utf-8').strip(), 'fail to execute', ssh.returncode

host = 'ec2-user@ec2-54-169-248-159.ap-southeast-1.compute.amazonaws.com'
cmd = ["ping", "-c", "10", "www.google.com"]
print(ssh_cmd(host, cmd))
