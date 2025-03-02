# Test Automation

# 要件

Python 3.13.1 では動作確認済み。

# セットアップ

本ページ上部の「Code > Download ZIP」からダウンロードを実行し、解凍したフォルダのプロンプトで以下を実行します。

```
python -m pip install -r requirements.txt
streamlit run app-robot.py
```

初回実行の場合は、メールアドレスを入力してください。
実行したらブラウザで TestAutomation が起動します。

# 使い方

## 機器登録

まずは、Device タブで対象機器の情報を入力します。
![Image](https://github.com/user-attachments/assets/0e4b1aec-bc60-4f12-aa4a-d26192819321)

| 項目名      | 必須 | 説明                                                                                          |
| ----------- | ---- | --------------------------------------------------------------------------------------------- |
| Hostname    | 必須 | ホスト名を入力してください                                                                    |
| IPAddress   | 必須 | ログイン可能な IP アドレスを入力してください                                                  |
| Username    | 必須 | ログイン時に使用するユーザ名を入力してください                                                |
| Password    | 必須 | ログイン時に使用するパスワードを入力してください                                              |
| EnablePass  | 任意 | ログイン時に使用する Enable パスワードを入力してください                                      |
| Logname     | 任意 | ログファイル名を入力してください。入力しない場合、「ホスト名\_yyyymmdd_HHMMSS.log」になります |
| check       | 必須 | 対象機器の場合は必ず「●」を入力してください                                                   |
| description | 任意 | 説明文を入力する欄です                                                                        |

入力が完了したら、右下のボタン「Update device list」をクリックしてください。\
クリックすると Data フォルダに CSV ファイルが作成され、データが保持されます。

### (参考)DeviceType の書き方

接続機器の OS や接続方式によって、値が異なります。\
主なデバイスタイプは以下のとおりです。
| DeviceType | 対象 | 接続方式 |
| ---------------- | --------- | -------- |
| cisco_ios | Cisco IOS | SSH |
| cisco_ios_telnet | Cisco IOS | Telnet |
| cisco_nxos | Nexus | SSH |
| apresia_aeos | Apresia AEOS | SSH |
| juniper_junos | Juniper | SSH |

詳細は「netmik device_type」で検索してみてください。

## テストケース

Test-Case タブでは、入力した合格条件をもとに試験を実行することができます。
試験結果のログもブラウザ上で閲覧することが可能です。

### main タブ

main タブで合格条件の入力、試験の実行を行うことができます。

![Image](https://github.com/user-attachments/assets/63d42952-2c55-4d46-aeaf-fade0f92676f)

| 項目名             | 必須 | 説明                                                                                                                                                                                                    |
| ------------------ | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| expected value     | 必須 | テスト実行時の期待される値を入力してください                                                                                                                                                            |
| operator           | 必須 | =、in、<、>の中から入力してください                                                                                                                                                                     |
| command            | 必須 | 実行するコマンドを入力してください                                                                                                                                                                      |
| top_list number    | 任意 | 詳細は～を参照してください                                                                                                                                                                              |
| top_key            | 任意 | 詳細は～を参照してください                                                                                                                                                                              |
| second_list number | 任意 | 詳細は～を参照してください                                                                                                                                                                              |
| target             | 必須 | Device で登録した機器の中からテスト対象とするホスト名を入力してください。「all」と入力した場合、すべての機器が対象になります。「device1,device2」とカンマ区切りで複数の機器を対象にすることも可能です。 |

画像の例では、test-rt に対して、`show run | i hostname`を実行し、出力結果に`test-rt`が含まれていれば合格となる

入力が完了したら、右下のボタン「Update test case」をクリックしてください。\
クリックすると Data フォルダに CSV ファイルが作成され、データが保持されます。

### summary test report タブ

プルダウンから HTML ファイルを選択することで、試験結果のサマリを表示することができます。

![Image](https://github.com/user-attachments/assets/be600096-52fa-4c35-bda6-b1bab14fe9eb)

### text-based test log タブ

プルダウンから log ファイルを選択することで、試験結果の詳細レポートを表示することができます。

![Image](https://github.com/user-attachments/assets/5b242968-ba2f-4def-8f74-a704d8f24ba8)

### detail test report タブ

プルダウンから HTML ファイルを選択することで、試験で取得したログファイルを表示することができます。\
※Robotframework で自動生成されるものです。

## ログ取得

![Image](https://github.com/user-attachments/assets/385d741a-37fa-44bf-8382-7ac635cf45d6)

## Ping 実行
