import boto3
connection = boto3.client('emr', region_name='eu-west-1')

cluster_id = connection.run_job_flow(
    Name='TEST',
    LogUri='s3n://aws-logs-983147734805-eu-west-1/elasticmapreduce/',
    ReleaseLabel='emr-6.1.0',
    Applications=[
        {
            'Name': 'Spark'
        },
    ],
    Instances={
        'InstanceGroups': [
            {
                'Name': "Master nodes",
                'Market': 'SPOT',
                'InstanceRole': 'MASTER',
                'InstanceType': 'r5d.4xlarge',
                'InstanceCount': 1,
                'EbsConfiguration': {
                    'EbsBlockDeviceConfigs': [
                        {
                            'VolumeSpecification': {
                                'VolumeType': 'gp2',
                                'SizeInGB': 600
                            },
                            'VolumesPerInstance': 1
                        },
                    ],
                    'EbsOptimized': True
                }
            },
            {
                'Name': "Slave nodes",
                'Market': 'SPOT',
                'InstanceRole': 'CORE',
                'InstanceType': 'r5d.4xlarge',
                'InstanceCount': 3,
                'EbsConfiguration': {
                    'EbsBlockDeviceConfigs': [
                        {
                            'VolumeSpecification': {
                                'VolumeType': 'gp2',
                                'SizeInGB': 600
                            },
                            'VolumesPerInstance': 1
                        },
                    ],
                    'EbsOptimized': True
                }
            }
        ],
        'Ec2KeyName': 'key_name',
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False,
        'Ec2SubnetId': 'subnet-1c21db46',
    },
    BootstrapActions=[
        {
            'Name': 'assign_static_ip2',
            'ScriptBootstrapAction': {
                'Path': 's3://bucket/spark/ip4.py',
                'Args': [
                    'static_ip_address_for_master',
                ]
            }
        },
{
            'Name': 'install_libraries',
            'ScriptBootstrapAction': {
                'Path': 's3://bucket/spark/install_this.sh',
                'Args': [
                ]
            }
        },
    ],
    VisibleToAllUsers=True,
    JobFlowRole='Matillion_ETL_IAM_Role',
    ServiceRole='EMR_DefaultRole',
)

print('cluster created with the step...', cluster_id)