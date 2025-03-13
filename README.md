# Test Automation

# 要件

Python 3.13.1 では動作確認済みです。\
対象機器は Cisco-ios、NX-OS のみ動作確認してますが、基本何でも動くはずです。

# セットアップ

本ページ上部の「Code > Download ZIP」からダウンロードを実行し、解凍したフォルダのプロンプトで以下を実行します。

```
python -m pip install -r requirements.txt
streamlit run app.py
```

初回実行の場合は、メールアドレスを入力してください。
実行したらブラウザで TestAutomation が起動します。

# 使い方

## Device タブ

まずは、Device タブで対象機器の情報を入力します。
![Image](https://github.com/user-attachments/assets/88c9ee5b-1be3-403e-8213-878b86dbe759)

| 項目名      | 必須 | 説明                                                                                            |
| ----------- | ---- | ----------------------------------------------------------------------------------------------- |
| Hostname    | 必須 | ホスト名を入力してください                                                                      |
| IPAddress   | 必須 | ログイン可能な IP アドレスを入力してください                                                    |
| Username    | 必須 | ログイン時に使用するユーザ名を入力してください                                                  |
| Password    | 必須 | ログイン時に使用するパスワードを入力してください                                                |
| EnablePass  | 任意 | ログイン時に使用する Enable パスワードを入力してください                                        |
| Logname     | 任意 | ログファイル名を入力してください<br>入力しない場合、「ホスト名\_yyyymmdd_HHMMSS.log」になります |
| check       | 必須 | 対象機器の場合は必ず「●」を入力してください                                                     |
| description | 任意 | 説明文を入力する欄です                                                                          |

入力が完了したら、右下のボタン「Update device list」をクリックしてください。\
クリックすると Data フォルダに CSV ファイルが作成され、データが保持されます。

### (参考)DeviceType の書き方

接続機器の OS や接続方式によって、値が異なります。\
主なデバイスタイプは以下のとおりです。
| DeviceType | 対象 | 接続方式 |
| ---------------- | --------- | -------- |
| cisco_ios | Cisco ios | SSH |
| cisco_ios_telnet | Cisco ios | Telnet |
| cisco_nxos | Nexus | SSH |
| apresia_aeos | Apresia AEOS | SSH |
| juniper_junos | Juniper | SSH |

詳細は「netmik device_type」で検索してみてください。

## Test-Case タブ

Test-Case タブでは、入力した合格条件をもとに試験を実行することができます。
試験結果のログもブラウザ上で閲覧することが可能です。

### main タブ

main タブで合格条件の入力、試験の実行を行うことができます。

![Image](https://github.com/user-attachments/assets/63d42952-2c55-4d46-aeaf-fade0f92676f)

| 項目名             | 必須 | 説明                                                                                                                                                                                                      |
| ------------------ | ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| expected value     | 〇   | テスト実行時の期待される値を入力してください                                                                                                                                                              |
| operator           | 〇   | =、in、<、>の中から入力してください                                                                                                                                                                       |
| command            | 〇   | 実行するコマンドを入力してください                                                                                                                                                                        |
| top_list number    | -    | 下記、「list number、key の書き方」を参照してください                                                                                                                                                     |
| top_key            | -    | 下記、「list number、key の書き方」を参照してください                                                                                                                                                     |
| second_list number | -    | 下記、「list number、key の書き方」を参照してください                                                                                                                                                     |
| target             | △    | Device で登録した機器の中からテスト対象とするホスト名を入力してください<br>「all」と入力した場合、すべての機器が対象になります<br>「device1,device2」とカンマ区切りで複数の機器を対象にすることも可能です |

画像の例では、test-rt に対して、`show run | i hostname`を実行し、出力結果に`test-rt`が含まれていれば合格となります。

入力が完了したら、右下のボタン「Update test case」をクリックしてください。\
クリックすると Data フォルダに CSV ファイルが作成され、データが保持されます。

ボタン「Test Case Run」をクリックすると、入力した内容で試験が実行されます。

### summary test report タブ

プルダウンから HTML ファイルを選択することで、試験結果のサマリを表示することができます。

![Image](https://github.com/user-attachments/assets/be600096-52fa-4c35-bda6-b1bab14fe9eb)

### text-based test log タブ

プルダウンから log ファイルを選択することで、試験で取得したログファイルを表示することができます。

![Image](https://github.com/user-attachments/assets/5b242968-ba2f-4def-8f74-a704d8f24ba8)

### detail test report タブ

プルダウンから HTML ファイルを選択することで、試験結果の詳細レポートを表示することができます。\
※Robotframework で自動生成されるものです。

## Get Logs タブ

テキストベースのログを取得することができます。\
また、テストケースの top_list number を入力する際に役立つ、コマンドのパースを実行することも可能です。

### main タブ

取得したいコマンドを入力します。
![Image](https://github.com/user-attachments/assets/385d741a-37fa-44bf-8382-7ac635cf45d6)

入力が完了したら、右下のボタン「Update command list」をクリックしてください。\
クリックすると Data フォルダに CSV ファイルが作成され、データが保持されます。

ボタン「Get logs」をクリックすると、入力したコマンドでログが取得されます。\
また、ボタン「Parse Run」をクリックすると、コマンドのパースが実行されます。

### parse result タブ

プルダウンから HTML ファイルを選択することで、パースの結果を表示することができます。

![Image](https://github.com/user-attachments/assets/6df5cbd8-ecd7-4d7a-9034-fd325d304410)

### (参考)list number、key の書き方

list number、key を指定することで、ある特定の情報・ステータスを取得することが可能となり、より正確なテストケースを作成することができます。\
例えば、OS バージョンや port1/0/1 の speed/duplex 情報など。

上記パース結果を例に、list number、key に何を入力したら、どんな値が取得できるのかを以下に示します。

例 1）
| 項目名 | 値 |
| ------------------ | -------- |
| top_list number | 0 |
| top_key | version |
| second_list number | 入力なし |

取得される値：17.10.1prd7

例 2）
| 項目名 | 値 |
| ------------------ | -------- |
| top_list number | 0 |
| top_key | hardware |
| second_list number | 0 |

取得される値：C9KV-Q200-8P

### text-based log タブ

プルダウンから log ファイルを選択することで、ログファイルを表示することができます。

![Image](https://github.com/user-attachments/assets/5b242968-ba2f-4def-8f74-a704d8f24ba8)

## Ping タブ

ボタン「Ping Run」をクリックすると、Device に登録してあるすべての機器に対して Ping を実行します。
実行後、画面に対象機器、レスポンス結果、レスポンスタイムが表示されます。

![Image](https://github.com/user-attachments/assets/3298cbd5-9f2b-4a58-8b19-7053a037f8d7)

## Tips

### 機器台数が多く、ブラウザ上での入力に時間がかかる場合

対象機器/テストケース/コマンドの情報は、ブラウザ上で表を更新し CSV ファイルにバックアップしていますが、逆の更新も可能です。\
各タブにあるボタン「Directly edit ～」をクリックすることで、該当の CSV ファイルを開くことができます。\
CSV ファイルを編集・保存後にブラウザを更新することで、表に情報が反映されます。
