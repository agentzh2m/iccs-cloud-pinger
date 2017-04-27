import boto3
import time
import subprocess
import sys

ec2 = boto3.resource('ec2', region_name='ap-southeast-1')

image_id = 'ami-fc5ae39f'
regions = {
    'ap-northeast-1': 'Tokyo',
    'ap-northeast-2': 'Seoul',
    'ap-southeast-1': 'Singapore',
    'ap-southeast-2': 'Sydney',
    'ap-south-1': 'Mumbai'
}

def ssh_cmd(host, cmd):
    ssh = subprocess.run(["ssh", "-i", "iccs-cloud.pem", host, cmd],
                         stdout=subprocess.PIPE)
    if ssh.return_code == 0:
        return ssh.stdout.decode('utf-8')
    else:
        return cmd, 'fail to execute'

# create instance


instance = ec2.create_instances(ImageId=image_id, MinCount=1,
                                MaxCount=1,
                                InstanceType='t2.micro',
                                KeyName='iccs-cloud',
                                SecurityGroupIds=[
                                    'sg-dbcf87bc'
                                ]
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

before_start = 0
while instance.state != 'running':
    time.sleep(1)
    before_start += 1
    print(instance.id, instance.instance_type, instance.public_ip_address, instance.state)

print('launch time ', before_start)
print ssh_cmd(instance.public_dns_name, "ping -c 20 www.google.com")
print ssh_cmd(instance.public_dns_name, "ping -c 20 www.pantip.com")
instance.terminate()

print('Terminate the instance after executing all command')
