from mitmproxy import http
import json


class RequestModifier:
    def request(self, flow: http.HTTPFlow) -> None:
        """拦截并修改请求"""

        # 只处理 POST 请求
        if flow.request.method == "POST":

            # 匹配特定的 API 端点
            if "studyRecord" in flow.request.pretty_url:
                print(f"拦截到请求: {flow.request.pretty_url}")

                # 获取原始数据
                try:
                    original_data = json.loads(flow.request.content)
                    print(f"原始数据: {original_data}")
                    original_data["actualNum"] = original_data["totalNum"]
                    original_data["studyDuration"] = original_data["totalNum"]
                    original_data["lastNum"] = original_data["totalNum"]

                    # 更新请求体
                    flow.request.content = json.dumps(original_data).encode('utf-8')

                    print(f"修改后数据: {original_data}")

                except json.JSONDecodeError:
                    print("无法解析JSON")

    def response(self, flow: http.HTTPFlow) -> None:
        """拦截并修改响应"""
        if "studyRecord" in flow.request.pretty_url:
            print(f"收到响应: {flow.response.status_code}")
            print(f"响应内容: {flow.response.text[:200]}")


addons = [RequestModifier()]

# "# 方式1: 使用脚本
# mitmdump -s proxyer.py -p 8080