import subprocess
import datetime as dt
import os

def run_robot_test():
    # robotファイルへの相対パスを指定
    robot_file = os.path.join('Robots', 'test_case.robot')
    
    now = dt.datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')

    # レポートを保存するフォルダを作成
    output_dir = "Output"
    report_folder = os.path.join(output_dir, 'Report')
    report_folder = os.path.join(report_folder, timestamp)
    os.makedirs(report_folder, exist_ok=True)  # フォルダが存在しない場合は作成

    # 出力ファイルのパスを指定
    ReportFilename = os.path.join(report_folder, f"report_{timestamp}.html")
    LogFilename = os.path.join(report_folder, f"log_{timestamp}.html")
    OutputFilename = os.path.join(report_folder, f"output_{timestamp}.xml")

    # Robot Frameworkのコマンドを指定    
    command = [
        'robot', 
        '--report', ReportFilename, 
        '--log', LogFilename, 
        '--output', OutputFilename, 
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
    run_robot_test()
