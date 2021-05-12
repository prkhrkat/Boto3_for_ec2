import boto3, os
import paramiko

def create_key_pair():
    ec2 = boto3.resource('ec2')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)

    # write private key to file with 400 permissions
    with os.fdopen(os.open("/tmp/ec2-keypair.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(KeyPairOut)


def get_public_ip(instance_id):
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    instances = ec2.instances.filter(InstanceIds = [instance_id])
    for instance in instances:
        print(instance.public_ip_address)
    return instance.public_ip_address
    


def create_instance(instance_type):
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    instance = ec2.create_instances(
        ImageId="ami-077e31c4939f6a2f3",
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName="ec2-keypair"
        )

    print (instance[0].id)
    return(instance[0].id)


def get_running_instances():
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped', 'running', 'terminated']}])

    instances_array = []
    for instance in instances:
        instances_array.append(instance)
    return instances_array


def ssh_and_send_command(instance_id):
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    instances = ec2.instances.filter(InstanceIds = [instance_id])
    for instance in instances:
        print(instance.private_ip_address)
    instance_ip = instance.private_ip_address
    key = paramiko.RSAKey.from_private_key_file("/tmp/ec2-keypair.pem")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cmd ='echo "hello world"'
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=instance_ip, username="ec2-user", pkey=key)
        print('SSH is done')

        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read())
        a = stdout.read()
        # close the client connection once the job is done
        client.close()
        return a

    except:
        return 'getting some error'

    
def stop_instance(instance_id):
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    response = ec2.instances.filter(InstanceIds = [instance_id]).stop()
    print(response)

def terminate_instance(instance_id):
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    response = ec2.instances.filter(InstanceIds = [instance_id]).terminate()
    print(response)
