import boto3
import time
import subprocess
import sys

ec2 = boto3.resource('ec2', region_name='ap-southeast-1')

image_id = 'ami-fc5ae39f'
keyname = 'hamuel-mbp' # go and add your public key in the aws console security
regions = {
    'ap-northeast-1': 'Tokyo',
    'ap-northeast-2': 'Seoul',
    'ap-southeast-1': 'Singapore',
    'ap-southeast-2': 'Sydney',
    'ap-south-1': 'Mumbai'
}


def ssh_cmd(host, cmd):
    ssh = subprocess.run(['ssh',
                          '-o', 'StrictHostKeyChecking=no',
                          ] + [host] + cmd,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ssh.returncode == 0:
        return ssh.stdout.decode('utf-8').strip()
    else:
        return ssh.stderr.decode('utf-8').strip(), 'fail to execute', ssh.returncode

# create instance


def pinging(host):
    ping = subprocess.run(['ping', '-c', '10', host],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ping.returncode == 0:
        return ping.stdout.decode('utf-8').strip()
    else:
        return ping.stderr.decode('utf-8').strip(), 'fail to ping the server'


instances = ec2.create_instances(ImageId=image_id, MinCount=1,
                                 MaxCount=1,
                                 InstanceType='t2.micro',
                                 KeyName=keyname,
                                 # SecurityGroupIds=[
                                 #     'sg-dbcf87bc'
                                 # ],
                                 BlockDeviceMappings=[{
                                     'DeviceName': '/dev/sdf',
                                     'VirtualName': 'ephemeral0',
                                     'Ebs': {
                                         'VolumeSize': 8,
                                         'DeleteOnTermination': True,
                                         'Encrypted': False
                                     }
                                 }]
                                 )

# get current instance
print('Lanuching!! -->', instances)
before_start = 0
instance = instances[0]
while instance.state['Name'] != 'running':
    time.sleep(1)
    before_start += 1
    instances = [i for i in ec2.instances.filter(InstanceIds=[instance.id])]
    instance = instances[0]

print('launch time ', before_start)

host = 'ec2-user@' + instance.public_dns_name
print('try to connect to', host)

print('Waiting for everything to be ready')
time.sleep(15)
print(pinging(instance.public_dns_name))
print('Waiting for ssh server to be up')
time.sleep(30)
print(ssh_cmd(host, ["ping", "-c", "15", "www.google.com"]))
print(ssh_cmd(host, ["ping", "-c", "15", "www.pantip.com"]))

print(instance.terminate())
print('Terminate the instance after executing all command')
