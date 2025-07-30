import paramiko
from k8s_install_mcp.core import install_commands
from k8s_install_mcp.core import ssh_client
from k8s_install_mcp.function import utils

class InstallTools:

    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    def update(self, ssh_data: ssh_client):
        log = utils.exec(ssh_data=ssh_data, command="sudo dnf -y update")
        return ''.join(log)

    def set_env(self, ssh_data: ssh_client) -> str:
        log = utils.exec_commands(ssh_data=ssh_data, commands=install_commands.setting_commands)
        return ''.join(log)

    def k8s_master_install(self, ssh_data: ssh_client) -> str:
        logs = utils.exec_commands(ssh_data=ssh_data, commands=install_commands.master_install_commands)
        ssh_data.token = utils.exec(ssh_data=ssh_data, command="cat token.txt")
        return ''.join(logs)

    def k8s_client_install(self, ssh_data: ssh_client) -> str:
        logs = utils.exec_commands(ssh_data=ssh_data, commands=install_commands.client_install_commands)
        return ''.join(logs)

    def k8s_client_token(self, ssh_data: ssh_client, token: str, node_name : str):
        utils.exec(ssh_data=ssh_data, command='sudo ' + token + ' --node-name ' + node_name)
install = InstallTools()