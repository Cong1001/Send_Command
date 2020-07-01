def get_ssm_instance_list(ssm):
    instance_list = []
    InstanceList = ssm.describe_instance_information(
        MaxResults=50
    )
    for Instance in InstanceList.get('InstanceInformationList'):
        if Instance['PingStatus'] == 'Online':
            instance_list.append(Instance)
    return instance_list

def get_linux_list(instance_list):
    linux_list = []
    for instance in instance_list:
        if instance['PlatformType'] == 'Linux':
            linux_list.append(instance)
    return linux_list

def get_linux_id_list(linux_list):
    linux_id_list = []
    for linux in linux_list:
        linux_id_list.append(linux['InstanceId'])
    return linux_id_list