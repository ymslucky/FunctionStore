import http.client
import os
import re


def create_headers(cookie,
                   user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'):
    return {
        'Cookie': cookie,
        'User-Agent': user_agent
    }


def get_sign(conn, cookie):
    headers = create_headers(cookie)
    conn.request("GET", "/sg_sign.htm", headers=headers)
    res = conn.getresponse()
    html = res.read().decode("utf-8")
    if '<h1>403 Forbidden</h1>' in html:
        raise Exception("加载页面失败，被反爬机制拦截")
    match = re.search(r'var sign = "(.*?)"', html)
    if not match:
        raise Exception("获取签到SIGN失败，请检查Cookie")
    return match.group(1)


def sign_in(conn, sign, cookie):
    headers = create_headers(cookie)
    headers.update({
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    })
    payload = f'sign={sign}'
    conn.request("POST", "/sg_sign.htm", payload, headers)
    res = conn.getresponse()
    response_str = res.read().decode("utf-8")
    return response_str


def main(context):
    cookie = os.environ['COOKIE']
    context.log(f"Cookie: {cookie}")
    conn = http.client.HTTPSConnection("www.hifini.com")
    try:
        # 通过Cookie获取当天SIGN
        sign = get_sign(conn, cookie)
        context.log(f"SIGN: {sign}")
        # 使用Cookie与SIGN签到
        response = sign_in(conn, sign, cookie)
        context.log(f"签到结果:\n{response}")
        return context.res.json(response)
    except Exception as e:
        context.log(f"签到失败: {e}")
        return context.res.json({"error": str(e)})
    finally:
        conn.close()
