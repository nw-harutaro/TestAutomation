from robot.api.deco import library, keyword
import os

@library(scope="SUITE")
class GenerateHTML():
    
    def __init__(self):
        self.connection = None

    @keyword
    def generate_html_dict_structure(self, parsed_data_list, timestamp):
        # HTMLのヘッダー部分を作成
        html_content = """
        <html>
            <head>
                <title>Show Command Hierarchical Structure</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .title { font-size: 24px; font-weight: bold; margin-bottom: 20px; }
                    .section { margin-bottom: 20px; cursor: pointer; padding: 10px; background-color: #f1f1f1; border: 1px solid #ddd; }
                    .section:hover { background-color: #ddd; }
                    .section-content { display: none; margin-top: 20px; padding-left: 20px; }
                    .active { background-color: #ccc; }
                    .item { margin-left: 20px; }
                    .list-index { color: blue; font-weight: bold; }
                    .key { color: green; font-weight: bold; }
                    .value { color: purple; }
                    .nested { border-left: 2px solid #ddd; margin-left: 20px; padding-left: 10px; }
                </style>
            </head>
            <body>
                <div class="title">Show Command Hierarchical Structure</div>
        """
        
        # 各セクションを作成
        for i, parsed_data in enumerate(parsed_data_list):
            section_title = list(parsed_data.keys())[0]  # 最初のキーをセクション名として使用        
            html_content += f'<div class="section" onclick="toggleContent({i})">{section_title}</div>'
            html_content += f'<div class="section-content" id="content{i}">'
            # parse_structure関数で内容を解析し追加
            html_content += GenerateHTML.parse_structure(parsed_data)
            html_content += "</div>"
            html_content += "</div>"
        
        # HTMLの閉じタグを追加
        html_content += """
                <script>
                    function toggleContent(index) {
                        var content = document.getElementById('content' + index);
                        // コンテンツの表示・非表示を切り替え
                        if (content.style.display === 'none' || content.style.display === '') {
                            content.style.display = 'block';
                        } else {
                            content.style.display = 'none';
                        }
                    }
                </script>
            </body>
        </html>
        """            
        # 生成されたHTMLを保存
        log_folder = os.path.join('Output', 'Parse')
        log_folder = os.path.join(log_folder, timestamp)
        os.makedirs(log_folder, exist_ok=True)  # フォルダが存在しない場合は作成

        filename = f"show_command_parse_{timestamp}.html"
        filename = os.path.join(log_folder, filename)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

    @keyword
    def parse_structure(data):
        html = ""
        
        # データがリストの場合、各要素のインデックスを表示
        if isinstance(data, list):
            for i, item in enumerate(data):
                html += f'<div class="list-index">List Index [{i}]</div>'
                # ネストされた内容を処理
                html += f'<div class="nested">{GenerateHTML.parse_structure(item)}</div>'
            
            html += "</div>"
        
        # データが辞書の場合、各キーと値を表示
        elif isinstance(data, dict):
            for key, value in data.items():
                html += f'<div><span class="key">{key}:</span> '
                if isinstance(value, (dict, list)):
                    # 値がネストされている場合、再帰的に処理
                    html += f'<div class="nested">{GenerateHTML.parse_structure(value)}</div>'
                else:
                    # 単一の値を表示
                    html += f'<span class="value">{value}</span></div>'
            
        
        # 単一の値を表示
        else:
            html += f'<div><span class="value">{data}</span></div>'
        
        return html
    
    @keyword
    def generate_html_result_summary(self, data, timestamp):
        """
        Generate an HTML report for host results with row color change and newline support.
        
        :param data: List of tuples in the format [(hostname, expected, operator, output, result), ...]
        :param output_file: The name of the HTML file to save the report.
        """
        # Start of the HTML structure
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Result Summary</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f4f4f4; }
                .ok-row { background-color: #d4edda; } /* Light green for OK */
                .ng-row { background-color: #f8d7da; } /* Light red for NG */
            </style>
        </head>
        <body>
            <h1>Result Summary</h1>
        """

        # Group data by hostname
        grouped_data = {}
        for hostname, expected, operator, output, result in data:
            if hostname not in grouped_data:
                grouped_data[hostname] = []
            grouped_data[hostname].append((expected, operator, output, result))
        
        # Add content for each host
        for hostname, results in grouped_data.items():
            html_content += f"<h2>{hostname}</h2>\n"
            html_content += """
            <table>
                <thead>
                    <tr>
                        <th>Expected</th>
                        <th>Operator</th>
                        <th>Output</th>
                        <th>Result</th>
                    </tr>
                </thead>
                <tbody>
            """
            for expected, operator, output, result in results:
                row_class = "ok-row" if result == "OK" else "ng-row"
                # Replace newlines with <br> for HTML
                expected = str(expected)
                operator = str(operator)
                output = str(output)
                expected_html = expected.replace("\n", "<br>")
                operator_html = operator.replace("\n", "<br>")
                output_html = output.replace("\n", "<br>")
                html_content += f"""
                    <tr class="{row_class}">
                        <td>{expected_html}</td>
                        <td>{operator_html}</td>
                        <td>{output_html}</td>
                        <td>{result}</td>
                    </tr>
                """
            html_content += """
                </tbody>
            </table>
            """

        # End of the HTML structure
        html_content += """
        </body>
        </html>
        """

        # Save to file        
        output_folder = os.path.join("Output", "TestResult")
        output_folder = os.path.join(output_folder, timestamp)
        filename = f"result_summary_{timestamp}.html"
        filename = os.path.join(output_folder, filename)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
