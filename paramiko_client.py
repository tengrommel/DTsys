import paramiko
import configparser

class ParamikoClient:
    def __init__(self, config_str, section):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp_client = None
        self.client_state = 0
        self.section = section

    def connect(self):
        try:
            self.client.connect(hostname=self.config.get(self.section, 'host'),
                                port=self.config.getint(self.section, 'port'),
                                username=self.config.get(self.section, 'username'),
                                password=self.config.get(self.section, 'password'),
                                timeout=self.config.getfloat(self.section, 'timeout'))
            self.client_state = 1
        except Exception as e:
            print(e)
            try:
                self.client.close()
            except Exception as e:
                 print(e)
    def run_cmd(self, cmd_str):
        stdin, stdout, stderr = self.client.exec_command(cmd_str)
        # if " " in cmd_str:
        #     print("文件log名将以第一个单词命名")
        #     cmd_str_list = cmd_str.split()
        #     cmd_str=cmd_str_list[0]
        cmd_str = cmd_str.replace(' ', '')
        cmd_str = cmd_str.replace('/', '')
        filelog = cmd_str + "_" + self.section+".log"
        with open(filelog, 'w', encoding='utf-8') as new:
            for line in stdout:
                print(line,end='')
                new.write(line)


    def get_sftp_client(self):
        if self.client_state == 0:
            self.connect()
        if not self.sftp_client:
            self.sftp_client = paramiko.SFTPClient.from_transport(self.client.get_transport())
        return self.sftp_client