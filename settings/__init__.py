from os import environ

class GetSettings(object):
    def __init__(self):
        self.SingleCustomer = environ.get('SingleCustomer', None)
        self.CustomerID = environ.get('CustomerID', None)
        self.Cloud = environ.get('Cloud', None)
        self.REGION = environ.get('Region', None)
        self.email = environ.get('Email', None)
        self.script = environ.get('script', None)
        self.output_title = environ.get('script_output_title', None)
        self.cmd_dict_file = './tmp/cmd_dict.json'
        self.result_file = './tmp/result.csv'
        self.AWS_Customer_List_File_Dict = {'test': './Customer_List/AWS/TEST_List.json', 'us-east-1': './Customer_List/AWS/us-east-1.json', 'eu-west-1': './Customer_List/AWS/eu-west-1.json', 'eu-west-2': './Customer_List/AWS/eu-west-2.json', 'us-west-1': './Customer_List/AWS/us-west-1.json', 'us-west-2': './Customer_List/AWS/us-west-2.json', 'ap-northeast-1': './Customer_List/AWS/ap-northeast-1.json', 'ca-central-1': './Customer_List/AWS/ca-central-1.json'}

        self.send_from = 'cofu@jenkins.com'
        self.subject = 'Run Command result'
        self.text = 'Here is the run command result.\n\n For any bug, please contact cofu@microstrategy.'
