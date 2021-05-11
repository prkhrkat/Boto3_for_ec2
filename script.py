import boto3, os

def create_key_pair():
    ec2_client = boto3.client('ec2', region_name='us-west-2')
    key_pair = ec2_client.create_key_pair(KeyName="aws_key")
    private_key = key_pair["KeyMaterial"]

    # write private key to file with 400 permissions
    with os.fdopen(os.open("/tmp/aws_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(private_key)
    return private_key


def create_instance():
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    instances = ec2.create_instances(
        ImageId="ami-077e31c4939f6a2f3",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="aws_key"
        )

    print (instance[0].id)
    return(instance[0].id)


def get_public_ip(instance_id):
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    reservations = ec2.describe_instances(InstanceIds=[instance_id]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))

def get_running_instances():
    session = boto3.Session(region_name="us-east-2")
    ec2 = session.resource('ec2', region_name='us-east-2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped', 'running', 'terminated']}])

    instances_array = []
    for instance in instances:
        instances_array.append(instance)
    return instances_array

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