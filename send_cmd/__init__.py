from helper import crossaccount_session

def send_shell_document(ssm,scriptList,instanceList):
    output=ssm.send_command(InstanceIds=instanceList,DocumentName="AWS-RunShellScript",Parameters={"commands":scriptList,"executionTimeout":["300"]})
    return output

def command_invocation(ssm, CommandID, InstanceID):
    output = ssm.get_command_invocation(
        CommandId = CommandID,
        InstanceId = InstanceID
    )
    return output
