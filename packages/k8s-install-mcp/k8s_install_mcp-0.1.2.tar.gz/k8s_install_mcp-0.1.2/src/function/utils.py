import paramiko
from core import ssh_client
import uuid

class UtilsTools:

    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def notify(self, ssh_data: ssh_client, message: str) -> str:
        self.ssh.connect(hostname=ssh_data.hostname,
                    port=ssh_data.port,
                    username=ssh_data.username,
                    password=ssh_data.pwd,
                    allow_agent=True,
                    look_for_keys=True)

        try:
            stdin, stdout, error = self.ssh.exec_command(f'wall {message}')

            if stdout.channel.recv_exit_status() == 0: # 정상 실행 완료
                output = stdout.read().decode()
                return output
            else: # 에러 출력문
                error = error.read().decode()
                return "에러 발생" + error

        except paramiko.AuthenticationException:
            return "인증 실패: 사용자 이름 또는 비밀번호를 확인하세요."
        except paramiko.SSHException as sshException:
            return f"SSH 예외 발생: {sshException}"
        except Exception as e:
            return f"알 수 없는 오류 발생: {e}"

        finally:
            self.ssh.close()

    def exec(self, ssh_data: ssh_client, command: str) -> str:
        self.ssh.connect(hostname=ssh_data.hostname,
                    port=ssh_data.port,
                    username=ssh_data.username,
                    password=ssh_data.pwd,
                    allow_agent=True,
                    look_for_keys=True)
        result = ''
        try:
            stdin, stdout, error = self.ssh.exec_command(command, get_pty=True)
            status = stdout.channel.recv_exit_status()

            if status == 0: # 정상 실행 완료
                result = stdout.read().decode()
            else: # 에러 출력문
                result = command + " : " + error.read().decode()
        except paramiko.AuthenticationException:
            return "인증 실패: 사용자 이름 또는 비밀번호를 확인하세요."
        except paramiko.SSHException as sshException:
            return f"SSH 예외 발생: {sshException}"
        except Exception as e:
            return f"알 수 없는 오류 발생: {e}"

        finally:
            self.ssh.close()
            return result

    def exec_commands(self, ssh_data: ssh_client, commands: list) -> list:

        log = []
        self.ssh.connect(hostname=ssh_data.hostname,
                         port=ssh_data.port,
                         username=ssh_data.username,
                         password=ssh_data.pwd,
                         allow_agent=False,
                         look_for_keys=False)
        try:
            for command in commands:
                stdin, stdout, error = self.ssh.exec_command(command)

                if stdout.channel.recv_exit_status() == 0:
                    txt = stdout.read().decode()
                    if txt:
                        log.append( stdout.read().decode() )
                else:
                    log.append( command + ' : ' + error.read().decode() )
                    break
        finally:
            self.ssh.close()
            return log

    def get_uuid(self):
        return str(uuid.uuid4())


utils = UtilsTools()