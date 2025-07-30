from mcp.server.fastmcp import FastMCP
from k8s_install_mcp.core import ssh_master_data, ssh_client_data
from k8s_install_mcp.function import utils, install

mcp = FastMCP('k8s')

# master type
@mcp.tool()
def master_set_ssh(self, hostname: str, pwd: str, username='root', port=22) -> str:
    """master ssh 정보 설정"""
    return ssh_master_data.update_ssh_client(hostname=hostname, pwd=pwd, username=username, port=port)

@mcp.tool()
def master_token(self) -> str:
    """master 토큰 반환"""
    return ssh_master_data.get_token()

@mcp.tool()
def connect_test(self, type: str, message: str) -> str:
    """연결 테스트하기, master 설치 시 type master"""
    return utils.notify(ssh_data= ssh_master_data if type == 'master' else ssh_client_data,
                        message=message)

@mcp.tool()
def exec(self,type: str, command: str) -> str:
    """커맨드 실행하기,master 설치 시 type master"""
    return utils.exec(ssh_data=ssh_master_data if type == 'master' else ssh_client_data,
                      command=command)

@mcp.tool()
def update(self, type: str) -> str:
    """dnf update: 장시간 걸리므로 계속 기다릴것,master 설치 시 type master, client 설치 시 type client"""
    return install.update(ssh_data=ssh_master_data if type == 'master' else ssh_client_data)


@mcp.tool()
def setting_env(self, type: str) -> str:
    """setting env: k8s 환경 설정,master 설치 시 type master, client 설치 시 type client"""
    return install.set_env(ssh_data=ssh_master_data if type == 'master' else ssh_client_data)

@mcp.tool()
def k8s_master_install(self) -> str:
    """update, setting env 수행 후 (master 설치 시 type master로 설정)
    kubernetes(k8s) master 자동화 설치: 장시간 걸리므로 계속 기다릴것"""
    return install.k8s_master_install(ssh_data=ssh_master_data)


# client type

@mcp.tool()
def set_client_ssh(self, hostname: str, pwd: str, username='root', port=22) -> list:
    """client ssh 정보 설정"""
    ssh_client_data.update_ssh_client(hostname=hostname, pwd=pwd, username=username, port=port)
    return ssh_client_data

@mcp.tool()
def k8s_client_install(self) -> str:
    """client에게 다시 update, setting env 수행 후  kubernetes(k8s) client 자동화 설치하기, 실행 후 client 토큰 설정 실행"""
    return install.k8s_client_install(ssh_data=ssh_client_data)

@mcp.tool()
def k8s_client_token(self ,node_name=utils.get_uuid()):
    """client 토큰 설정"""
    return install.k8s_client_token(ssh_data=ssh_client_data,
                                    token=ssh_master_data.get_token(),
                                    node_name=node_name)

def main():
    print('server test')
    mcp.run()

if __name__ == "__main__":
    main()