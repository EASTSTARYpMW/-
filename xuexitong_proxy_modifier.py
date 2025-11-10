from mitmproxy import http
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import hashlib


str1 = "d_yHJ!$pdA~5"

# ============ 你的自定义方法 ============


def return_hash(result):
    dur_time = f"0_{result['duration']}"
    max_time = f"{result['duration']}000"
    playing_time = f"{result['duration']}000"
    raw_string = f"{result['clazzId']}{result['userid']}{result['jobid']}{result['objectId']}{playing_time}{str1}{max_time}{dur_time}"
    print(raw_string)
    enc1 = hashlib.md5(raw_string.encode()).hexdigest()
    return enc1



def decrypt_or_transform_enc(enc_value, info_lis):
    try:
        # 这里写你的具体实现
        print(f"[TRANSFORM] 原始 enc: {enc_value}")
        new_enc = return_hash(info_lis)
        print(f"[TRANSFORM] 新 enc: {new_enc}")
        return new_enc
    except Exception as e:
        print(f"[ERROR] 转换失败: {e}")
        return enc_value  # 失败时返回原值


# ============ mitmproxy 拦截器 ============
def request(flow: http.HTTPFlow) -> None:
    """
    拦截请求，修改 enc 参数
    """
    if flow.request.method != "GET":
        return

    url = flow.request.url
    print(f"[DEBUG] 完整 URL: {url}")

    if 'mooc1.chaoxing.com/mooc-ans/multimedia/log/a' in url:
        print("[DEBUG] 匹配到目标 URL！")

        # 解析 URL
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query, keep_blank_values=True)

        print(f"[DEBUG] 查询参数: {query_params}")

        # 检查是否存在 'enc' 参数
        if 'enc' in query_params:
            old_enc = query_params['enc'][0]
            print(f"[DEBUG] 原始 enc: {old_enc}")

            # 调用你的方法转换 enc
            new_enc = decrypt_or_transform_enc(old_enc, query_params)

            # 替换 enc 参数
            query_params['enc'] = [new_enc]
            print(f"[SUCCESS] enc 已替换为: {new_enc}")

            # 重新构建查询字符串
            new_query = urlencode(query_params, doseq=True)

            # 重新构建 URL
            new_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query,
                parsed_url.fragment
            ))

            # 更新请求 URL
            flow.request.url = new_url
            print(f"[INFO] 更新后的 URL: {new_url}")
        else:
            print("[DEBUG] 没有找到 'enc' 参数")
            print(f"[DEBUG] 可用的参数: {list(query_params.keys())}")

# 运行: mitmdump -s proxy_modifier.py