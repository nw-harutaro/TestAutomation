import subprocess
import datetime as dt
import os

def run_robot_parse(hostname,ipaddress,username,password,enable_pass,device_type):
    # robotファイルへの相対パスを指定    
    robot_file = os.path.join('Robots','dictionary-parse.robot')

    now = dt.datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')
        
    # Robot Frameworkのコマンドを指定
    command = [
        'robot', 
        '--report', 'NONE', 
        '--log', 'NONE', 
        '--output', 'NONE', 
        '--variable', f'Timestamp:{timestamp}',  # TIMESTAMPを変数として渡す
        '--variable', f'Hostname:{hostname}',
        '--variable', f'IPAddress:{ipaddress}',
        '--variable', f'Username:{username}',
        '--variable', f'Password:{password}',
        '--variable', f'EnablePass:{enable_pass}',
        '--variable', f'DeviceType:{device_type}',
        robot_file
    ]
    
    try:
        # コマンドを実行                      
        subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print(f"{robot_file} executed successfully.")
        # print("Output:", result.stdout.decode())
        # print("Errors:", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running robot test: {e}")
        # print("Output:", e.stdout.decode())
        # print("Errors:", e.stderr.decode())

