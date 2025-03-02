import subprocess
import datetime as dt
import os

def run_get_log():
    # robotファイルへの相対パスを指定
    robot_file = os.path.join('Robots', 'get_log.robot')
    
    now = dt.datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')

    # ログを保存するフォルダを作成
    rawlog_folder = os.path.join('RawLog', timestamp)
    os.makedirs(rawlog_folder, exist_ok=True)  # フォルダが存在しない場合は作成

    # Robot Frameworkのコマンドを指定    
    command = [
        'robot', 
        '--report', 'NONE', 
        '--log', 'NONE', 
        '--output', 'NONE', 
        '--variable', f'Timestamp:{timestamp}',  # TIMESTAMPを変数として渡す
        robot_file
    ]
    
    try:
        # コマンドを実行
        subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{robot_file} executed successfully.")
        # print("Output:", result.stdout.decode())
        # print("Errors:", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running robot test: {e}")
        # print("Output:", e.stdout.decode())
        # print("Errors:", e.stderr.decode())

# 実行
if __name__ == "__main__":
    run_get_log()
