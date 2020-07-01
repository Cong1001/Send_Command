#!/usr/bin/env python3.6

import os, json, csv, time, sys
from settings import GetSettings
from helper import crossaccount_session
from aws_ec2 import get_ssm_instance_list, get_linux_list, get_linux_id_list
from send_cmd import get_script, send_shell_document, command_invocation

def send_command(customer_id, account_id, account_region, sh_script_list, command_dict):
    session = crossaccount_session(account_id)
    ssm_client = session.client('ssm', region_name=account_region)
    instance_list = get_ssm_instance_list(ssm_client)
    linux_list = get_linux_list(instance_list)
    linux_id_list = get_linux_id_list(linux_list)

    sh_command = send_shell_document(ssm_client, sh_script_list, linux_id_list)
    sh_command_id = sh_command['Command']['CommandId']
    customer_dict = {'account_id': account_id, 'region': account_region, 'Linux': sh_command_id}
    command_dict[customer_id]=customer_dict
    return command_dict

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
    script = settings.script
    print(type(script), script)
    script_list = script.split('\n')
    print(script_list)