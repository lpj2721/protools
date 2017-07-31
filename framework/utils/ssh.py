# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2017/4/8 17:57
"""
import paramiko
from scp import SCPClient


class SSH:
    def __init__(self, host, user, password=None):
        """
        初始化ssh基本要素
        :param host: 主机
        :param user: 用户名
        :param password: 密码
        """
        self.host = host
        self.user = user
        self.password = password

    def __enter__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.user, password=self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh.close()

    def execute_cmd(self, cmd):
        """
        :param cmd: 所需要执行的命令
        :return: 返回值，包换stding,stdout,stderr元组，例如type(list) = stdout.readlines()
        """
        _, stdout, stderr = self.ssh.exec_command(cmd)
        channel = stdout.channel
        status = channel.recv_exit_status()
        if status == 0:
            return status, stdout.read()
        else:
            return status, stdout.read() + stderr.read()

    def put(self, local_path, remote_path):
        """
        上传文件
        :param local_path: 本地路径
        :param remote_path: 目标路径
        :return:
        """
        scp_client = SCPClient(self.ssh.get_transport())
        scp_client.put(local_path, remote_path)

    def get(self, remote_path, local_path):
        """
        下载文件
        :param remote_path:
        :param local_path:
        :return:
        """
        scp_client = SCPClient(self.ssh.get_transport())
        scp_client.get(remote_path, local_path)


if __name__ == '__main__':
    with SSH('10.10.0.100', 'root') as ssh:
        status, out = ssh.execute_cmd("ps -")
        print status, out
        # try:
        #     ssh = SSH('10.10.0.100', 'root')
        #     status, stdout = ssh.execute_cmd('ps -')
        #     # stdout = stdout.readlines()
        #     print status, stdout
        # except AuthenticationException:
        #     print "error  12341234"
        # else:
        #     ssh.close()
        # print "aaaaaaaaaaaaaaaaaaaaa"
        # ssh = SSH_key('10.10.0.100', 'root')
        # status, output = ssh.execute_cmd('cat /proc/cpuinfo')
        # print status, output
