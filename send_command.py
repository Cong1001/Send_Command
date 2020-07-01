#!/usr/bin/env python3.6

import os, json, csv, time, sys
from settings import GetSettings
from helper import crossaccount_session
from aws_ec2 import get_ssm_instance_list, get_linux_list, get_linux_id_list
from send_cmd import send_shell_document

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

if __name__ == "__main__":
    settings = GetSettings()
    script = settings.script
    result_file = settings.result_file
    output_title = settings.output_title
    sh_script_list = script.split('\n')
    cmd_dict_file = settings.cmd_dict_file
    
    with open(result_file ,'a', newline="") as csv_file:
        csv_file.write('CustomerID,Region,' + output_title + '\n')
    csv_file.close()
    command_dict={}

    if settings.Cloud == 'AWS': 
        Customer_Files_Dict = settings.AWS_Customer_List_File_Dict
        if settings.SingleCustomer == 'true':
            CustomerID = settings.CustomerID
            if CustomerID == None:
                print("Customer ID is not set. Exiting this script.")
            else:
                for customer_list in Customer_Files_Dict.keys():
                    with open(Customer_Files_Dict[customer_list]) as Customer_File:
                        account_list = json.load(Customer_File)
                        if CustomerID.upper() in account_list.keys():
                            account_id = account_list[CustomerID.upper()]['ID']
                            account_name = account_list[CustomerID.upper()]['Name']
                            account_region = account_list[CustomerID.upper()]['Region']
                            try:
                                command_dict = send_command(account_name, account_id, account_region, sh_script_list, command_dict)
                                time.sleep(30)
                            except:
                                print('ERROR: schedule ' + account_name + ' error!')
                                e = sys.exc_info()[1]
                                print("%s" %e)
                            Customer_File.close()
                            sys.exit(0)
                    Customer_File.close()
                print("%s is not in Customer List, please add it first!" %CustomerID)
        else:
            REGION = settings.REGION
            if REGION not in Customer_Files_Dict.keys():
                print("Customer List json file missing!")
            else:
                with open(Customer_Files_Dict[REGION]) as Customer_File:
                    account_list = json.load(Customer_File)
                    for account in account_list:
                        account_id = account_list[account]['ID']
                        account_name = account_list[account]['Name']
                        account_region = account_list[account]['Region']
                        try:
                            print("**********Sending runcommand to %s ****************" %account_name)
                            command_dict = send_command(account_name, account_id, account_region, sh_script_list, command_dict)
                        except:
                            print('ERROR: schedule ' + account_name + ' error!')
                            e = sys.exc_info()[1]
                            print("%s" %e)
                Customer_File.close()
                time.sleep(30)

    with open(cmd_dict_file, 'a', newline="") as cmd_dict:
        cmd_dict.write(json.dumps(command_dict))
    cmd_dict.close()