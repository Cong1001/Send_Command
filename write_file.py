import json
from settings import GetSettings
from helper import crossaccount_session
from aws_ec2 import get_ssm_instance_list, get_linux_list, get_linux_id_list
from send_cmd import command_invocation

def write_to_local(customer_id, account_id, account_region, sh_command_id, result_file):
    session = crossaccount_session(account_id)
    ssm_client = session.client('ssm', region_name=account_region)
    instance_list = get_ssm_instance_list(ssm_client)
    linux_list = get_linux_list(instance_list)
    linux_id_list = get_linux_id_list(linux_list)
    with open(result_file ,'a', newline="") as csv_file:
        for linux_id in linux_id_list:
            command_out = command_invocation(ssm_client, sh_command_id, linux_id)
            input_info = customer_id + ',' + account_region + ',' + command_out['StandardOutputContent']
            print(input_info)
            csv_file.write(input_info)
    csv_file.close()

if __name__ == "__main__":
    settings = GetSettings()
    result_file = settings.result_file
    cmd_dict_file = settings.cmd_dict_file
    with open(cmd_dict_file, 'r') as cmd_dict:
        command_dict = json.loads(cmd_dict.read())
    cmd_dict.close()

    for customer in list(command_dict.keys()):
        print("*****************%s****************" %customer)
        customer_id = customer
        account_id = command_dict[customer]['account_id']
        account_region = command_dict[customer]['region']
        sh_command_id = command_dict[customer]['Linux']
        write_to_local(customer_id, account_id, account_region, sh_command_id, result_file)
