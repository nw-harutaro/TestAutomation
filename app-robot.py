import streamlit as st
import subprocess
import os
import datetime
import webbrowser
import pandas as pd
import Libraries.General as General
import Run.dict_parse_run as dict_parse_run
from ping3 import ping
from concurrent.futures import ThreadPoolExecutor

# ↓↓↓↓ 変数定義など事前準備 ↓↓↓↓

# 必要なディレクトリに移動
os.chdir(os.path.dirname(os.path.realpath(__file__)))
# ここからの相対パスは `app-robot.py` と同じ基準で解釈される

data_dir = "Data"
backup_dir = os.path.join(data_dir,"Backup")
output_dir = "Output"
parse_dir = os.path.join(output_dir,"Parse")
text_based_log_dir = os.path.join(output_dir,"Text_Based_Log")
test_result_dir = os.path.join(output_dir,"TestResult")
report_dir = os.path.join(output_dir,"Report")

# フォルダが存在しなかったら作成    
os.makedirs(backup_dir, exist_ok=True)
os.makedirs(parse_dir, exist_ok=True)
os.makedirs(text_based_log_dir, exist_ok=True)
os.makedirs(test_result_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)

# CSVの初期ファイル名
initial_device_file = os.path.join(data_dir,"device.csv")
initial_test_case_file = os.path.join(data_dir,"test-case.csv")
initial_command_file = os.path.join(data_dir,"command.csv")

# ↑↑↑↑ 変数定義など事前準備 ↑↑↑↑


# ↓↓↓↓ 関数定義 ↓↓↓↓

# ファイルを開く
def open_data_file(file_path):
    if os.path.exists(file_path):
        try:
            webbrowser.open(f"file://{os.path.abspath(file_path)}")
            st.success(f"File opened: {file_path}")
            st.info("Please refresh the screen after editing the file")
        except Exception as e:
            st.error(f"Could not open file: {e}")
    else:
        st.error(f"File not found {file_path}")

# デバイスデータの読み込みまたは新規作成
def load_device_data():
    if os.path.exists(initial_device_file):
        return pd.read_csv(initial_device_file, encoding="utf-8")
    else:
        # 新規データフレーム作成
        return pd.DataFrame(columns=["Hostname", "IPAddress", "Username", "Password", "EnablePass", "LogName", "DeviceType", "check", "description"])

# デバイスデータの保存
def save_device_data(df):
    # 現在時刻でバックアップを保存
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_device_file = os.path.join(backup_dir, f"device_backup_{timestamp}.csv")
    df.to_csv(backup_device_file, index=False, encoding="utf-8-sig")

    # 最新データを初期CSVに保存
    df.to_csv(initial_device_file, index=False, encoding="utf-8-sig")

# テストケースデータの読み込みまたは新規作成
def load_test_case_data():
    if os.path.exists(initial_test_case_file):
        return pd.read_csv(initial_test_case_file, encoding="utf-8")
    else:
        # 新規データフレーム作成
        return pd.DataFrame(columns=["expected value", "operator", "command", "top_list number", "top_key", "second_list number", "target"])

# テストケースデータの保存
def save_test_case_data(df):
    # 現在時刻でバックアップを保存
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_test_case_file = os.path.join(backup_dir, f"test-case_backup_{timestamp}.csv")
    df.to_csv(backup_test_case_file, index=False, encoding="utf-8-sig")

    # 最新データを初期CSVに保存
    df.to_csv(initial_test_case_file, index=False, encoding="utf-8-sig")

# コマンドデータの読み込みまたは新規作成
def load_command_data():
    if os.path.exists(initial_command_file):
        return pd.read_csv(initial_command_file, encoding="utf-8")
    else:
        # 新規データフレーム作成
        return pd.DataFrame(columns=["Command"])

# コマンドデータの保存
def save_command_data(df):
    # 現在時刻でバックアップを保存
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_command_file = os.path.join(backup_dir, f"command_backup_{timestamp}.csv")
    df.to_csv(backup_command_file, index=False, encoding="utf-8-sig")

    # 最新データを初期CSVに保存
    df.to_csv(initial_command_file, index=False, encoding="utf-8-sig")

# 指定フォルダ内のファイルリストを再帰的に取得し、ファイルを選択するセレクトボックスを配置
# 選択したファイルの内容を画面に表示する
def display_selected_file_content(extensions,dir,file_type_name):
    files = General.get_files_by_extension(dir,extensions)
    file_names = [file["name"] for file in files]
    selected_file_name = st.selectbox(f"Please select a {file_type_name}", options=file_names)
    selected_file = next((file["path"] for file in files if file["name"] == selected_file_name), None)

    # エクスプローラーでファイルがあるディレクトリを開くボタン
    if st.button(f"Display the {file_type_name} in Explorer"):
        folder_path = os.path.dirname(selected_file)  # 選択したファイルのディレクトリを取得
        if os.name == 'nt':  # Windows
            os.startfile(folder_path)
        elif os.name == 'posix':  # macOS / Linux
            subprocess.run(["xdg-open", folder_path])
        st.success(f"{folder_path} opened in Explorer.")
    
    if selected_file:        
        try:
            # ファイルの拡張子を取得
            file_extension = selected_file.split(".")[-1].lower()

            with open(selected_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 拡張子に応じて表示形式を変更
            if file_extension == "html":
                st.components.v1.html(content, height=800, scrolling=True)
            elif file_extension == "log":
                st.text_area("ログ", content, height=800)
            
        except Exception as e:
            st.error(f"Error: file could not be read - {e}")

def ping_host(row):
    ipaddress = row[1]
    hostname = row[0]
    if pd.isna(ipaddress):
        return None

    response_time = ping(ipaddress)
    return {
        "Hostname": hostname,
        "IPaddress": ipaddress,
        "ResponseTime": response_time
    }

# 並列処理対応のPingモニタリング関数
def ping_monitor(device_data):
    ping_result = []

    with ThreadPoolExecutor() as executor:
        results = executor.map(ping_host, device_data.itertuples(index=False))

    # Noneを除外して結果を収集
    ping_result = [result for result in results if result is not None]
    return ping_result

# Ping結果を表形式に整形する関数
def format_ping_results(ping_results):
    formatted_results = []
    for result in ping_results:
        response_time = result["ResponseTime"]
        formatted_results.append({
            "Hostname": result["Hostname"],
            "IPaddress": result["IPaddress"],
            "ResponseResult": "OK" if response_time else "NG",
            "ResponseTime": f"{response_time:.2f} ms" if response_time else "N/A"
        })
    return pd.DataFrame(formatted_results)

# スタイルを設定してOKとNGの行に色をつける関数
def style_ping_results(df):
    def highlight(row):
        if row["ResponseResult"] == "OK":
            return ['background-color: lightgreen']*len(row)
        elif row["ResponseResult"] == "NG":
            return ['background-color: lightcoral']*len(row)
        else:
            return ['']*len(row)
    
    return df.style.apply(highlight, axis=1)

# ↑↑↑↑ 関数定義 ↑↑↑↑

# ワイドレイアウト
st.set_page_config(layout="wide")

# Webアプリのタイトル
st.title("Test Automation")

# タブを作成
tab1, tab2, tab3, tab4 = st.tabs(["Device","Test-Case", "Get Logs", "Ping"])

# デバイスタブ
with tab1:
    # メイン処理
    # データの読み込み
    data = load_device_data()                

    # データフレームの編集ウィジェット
    edited_device_data = st.data_editor(data, num_rows="dynamic", use_container_width=True)

    col1, col2, col3 = st.columns([6,1,1])
    with col2:
        if st.button("Directly edit the device list"):
            open_data_file(initial_device_file)                    
    
    with col3:               
        if st.button("Update device list"):
            save_device_data(edited_device_data)
            st.success("Device list has been updated and backup has been created")                 

# テストケースタブ
with tab2:
    st.info("If you do not know what to enter in the “top_list number,” “top_key,” and “second_list number” of the test case, "\
            +"please execute the parsing of the “Get Logs” tab and refer to the parsed results of the command.")

    #子タブを作成
    tab2A, tab2B, tab2C, tab2D= st.tabs(["main","summary test report","text-based test log","detail test report"])

    #メインタブ
    with tab2A:        
        # データの読み込み
        data = load_test_case_data()

        # データフレームの編集ウィジェット
        edited_test_case_data = st.data_editor(data, num_rows="dynamic", use_container_width=True)

        # ボタン配置整列用のカラムを作成
        col1, col2 = st.columns([1,6])
        col1, col2, col3, col4 = st.columns([5,1,1,1])

        with col2:  
            if st.button("Test Case Run"):
                try:
                    # Run配下のtest_case_run.pyを実行
                    result = subprocess.run(
                        ["python", os.path.join('Run', "test_case_run.py")],
                        check=True, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE
                    )
                    st.success("Success: Test case")
                    # st.text(result.stdout.decode())
                except subprocess.CalledProcessError as e:
                    st.error("Error: Test case")
                    # st.text(e.stderr.decode())
        with col3:  
            if st.button("Directly edit the test case"):
                open_data_file(initial_test_case_file) 
        with col4:  
            if st.button("Update test case"):
                save_test_case_data(edited_test_case_data)
                st.success("Test case has been updated and backup has been created")                        

    # 結果サマリ表示用タブ
    with tab2B:
        display_selected_file_content(["html"], test_result_dir, "result summary")         
    
    # ログ表示用タブ
    with tab2C:                        
        display_selected_file_content(["log"], test_result_dir, "test log")                 

    # レポート表示用タブ
    with tab2D:                        
        display_selected_file_content(["html"], report_dir, "report")                                 

# パース実行 & ログ取得用タブ
with tab3:
    #子タブを作成
    tab3A, tab3B, tab3C = st.tabs(["main","parse result","text-based log"])
    
    #メインタブ
    with tab3A:
        # データの読み込み
        device_data = load_device_data()
        command_data = load_command_data()

        # データの確認とリストボックスの表示
        if not device_data.empty:            
            selected_row = st.selectbox(
                "Please select the device to perform the parsing:",
                device_data.index,
                format_func=lambda x: f"{device_data.loc[x, 'Hostname']} / {device_data.loc[x, 'IPAddress']}"
            )
            selected_data = device_data.loc[selected_row]
            hostname=selected_data["Hostname"]
            ipaddress = selected_data["IPAddress"]
            username = selected_data["Username"]
            password = selected_data["Password"]
            enable_pass = selected_data["EnablePass"]
            device_type = selected_data["DeviceType"]
        else:
            st.warning("Device list not found or content is empty")
        
        # データフレームの編集ウィジェット
        edited_command_data = st.data_editor(command_data, num_rows="dynamic", use_container_width=True)

        # ボタン配置整列用のカラムを作成
        col1, col2 = st.columns([1,6])
        col1, col2, col3, col4, col5 = st.columns([4,1,1,1,1])

        with col2:
            if st.button("Get logs"):
                try:
                    result = subprocess.run(
                            ["python", os.path.join('Run', "get_log_run.py")],
                            check=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE
                        )
                    st.success("Success: Get logs")
                    # st.text(result.stdout.decode())
                except subprocess.CalledProcessError as e:
                    st.error("Error: Get logs")
                    # st.text(e.stderr.decode())

        with col3:
            if st.button("Parse Run"):
                try:                  
                    dict_parse_run.run_robot_parse(hostname,ipaddress,username,password,enable_pass,device_type)
                    st.success("Success: Parse")
                except:
                    st.error("Error: Parse")

        with col4:
            if st.button("Directly edit the command list"):
                open_data_file(initial_command_file)

        with col5:
            if st.button("Update command list"):
                save_command_data(edited_command_data)
                st.success("Command list has been updated and backup has been created")
    
    # パース結果タブ
    with tab3B:
        display_selected_file_content(["html"], parse_dir, "parse result")   

    # 生ログ表示タブ
    with tab3C:
        display_selected_file_content(["log"], text_based_log_dir, "log file")     

# Ping実行タブ
with tab4:
    if st.button("Ping Run"):
        device_data = load_device_data()

        if device_data.empty:
            st.warning("Device data is empty. Please enter device information")
        else:            
            ping_results = ping_monitor(device_data[["Hostname", "IPAddress"]])            
            formatted_results = format_ping_results(ping_results)
            st.dataframe(style_ping_results(formatted_results), use_container_width=True)

