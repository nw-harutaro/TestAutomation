from netmiko.ssh_dispatcher import ConnectHandler
from robot.api.deco import library, keyword
from openpyxl import load_workbook
import pandas as pd

@library(scope="SUITE")
class NetworkDeviceHandler():

    def __init__(self):
        self.connection = None

    @keyword
    def connect_device(self,device_info):
        my_device = {            
            "ip":device_info["IPAddress"],
            "username":device_info["Username"],
            "password":device_info["Password"],
            "secret": device_info["EnablePass"],
            "session_log": device_info["LogName"],
            "device_type":device_info["DeviceType"]
            }        
        # 機器に接続
        try:
            self.connection = ConnectHandler(**my_device)
            self.connection.enable()
            return True
        except:
            return False
        
    @keyword
    def connect_device_nolog(self,device_info):
        my_device = {            
            "ip":device_info["IPAddress"],
            "username":device_info["Username"],
            "password":device_info["Password"],
            "secret": device_info["EnablePass"],            
            "device_type":device_info["DeviceType"]
            }        
        # 機器に接続
        try:
            self.connection = ConnectHandler(**my_device)
            self.connection.enable()
            return True
        except TypeError as e:
            print(f"エラーが発生しました: {e}")
            return False
    
    @keyword
    def test_connect_device(self,device_info):
        my_device = {            
            "ip":device_info["IPAddress"],
            "username":device_info["Username"],
            "password":device_info["Password"],
            "secret": device_info["EnablePass"],            
            "device_type":device_info["DeviceType"]
            }        
        # 機器に接続
        try:
            self.connection = ConnectHandler(**my_device)
            self.connection.disconnect()
            return True
        except:
            return False
        
    @keyword
    def move_to_enable_mode(self):
        self.connection.enable()

    # @keyword
    # def send_command(self, command_string):
    #     return self.connection.send_command(command_string)

    @keyword
    def disconnect(self): 
        self.connection.disconnect()           
    
    @keyword
    def Param_Check(self, testcase_info):
        command = testcase_info["Command"]
        top_list_num = testcase_info["TopListNum"]

        if not pd.isna(top_list_num):
            output = self.connection.send_command(command, use_textfsm=True)
            # print(output)
            top_list_num = int(testcase_info["TopListNum"])
            top_key = testcase_info["TopKey"]
            sec_list_num = testcase_info["SecListNum"]
            
            try:
                if not pd.isna(sec_list_num):
                    sec_list_num = int(sec_list_num)
                    output = output[top_list_num][top_key][sec_list_num]
                else:
                    output = output[top_list_num][top_key]
            except:
                output = "non-existent key is specified"    
        else:
            output = self.connection.send_command(command)

        output = str(output)
        expected_value = str(testcase_info["ExpectedValue"])
        expected_values = expected_value.split(",")
        operator = str(testcase_info["Operator"])

        print(f"{expected_value} {operator}")
        print(f"{command}\n ⇒ {output}")

        operations = {
            "=": lambda ev, out: ev == out,
            "<": lambda ev, out: ev < out,
            ">": lambda ev, out: ev > out,
            "in": lambda ev, out: ev in out
        }

        for ev in expected_values:
            if not operations.get(operator, lambda ev, out: False)(ev.strip(), output):
                return False,output
        return True,output
        
    @keyword
    def send_commands_from_csv(self, file_path):
        # 各列の値を取得
        df = pd.read_csv(file_path, encoding="utf-8")        

        results = []
        
        try:
            for index, row in df.iterrows():
                command = row['Command']
                try:
                    if pd.notna(command):  # コマンドがNaNでないことを確認
                        result = self.connection.send_command(command, use_textfsm=True)
                        results.append({command: result})
                except Exception as e:
                    print(f"コマンド実行中にエラーが発生しました: {command} - {e}")
            return results
        except Exception as e:
            print(f"エラーが発生しました: {e}")
