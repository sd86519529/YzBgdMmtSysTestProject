import requests
import json
import base64
from requests_toolbelt import MultipartEncoder


def send_bug_to_cd(severity, module, title, pri, steps, assignedTo):
    import re
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    res = requests.get(url='http://192.168.31.9:8088/zentao/user-login-L3plbnRhby9idWctYnJvd3NlLTEuaHRtbA==.html',
                       headers=headers)

    zentaosid = res.headers.get('Set-Cookie')
    a = re.findall('.*?=(.*?);', zentaosid)

    log_url = 'http://192.168.31.9:8088/zentao/user-login-L3plbnRhby9idWctYnJvd3NlLTEuaHRtbA==.html'
    log_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'cookie': 'lang=zh-cn; device=desktop; theme=default; windowWidth=1920; windowHeight=978; zentaosid=' + a[0]
    }
    log_data = {
        'account': 'jinwei',
        'password': 'qwe123!@#',
        'passwordStrength': '1',
        'referer': '/zentao/bug-browse-1.html',
        'verifyRand': '612514079'
    }

    re = requests.post(url=log_url, headers=log_headers, data=log_data)
    print(re.text)
    put_url = 'http://192.168.31.9:8088/zentao/bug-create-1-0-moduleID=0.html'
    put_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "cookie": "lang=zh-cn; device=desktop; theme=default; preBranch=0; preProductID=1; bugModule=0; lastProduct=1; qaBugOrder=id_desc; windowWidth=1920; windowHeight=978; zentaosid=" +
                  a[0],
        "Referer": "http://k3.hzyz.iotube.cn/zentao/bug-create-1-0-moduleID=0.html",
        "Origin": "http://k3.hzyz.iotube.cn",
        "Host": "k3.hzyz.iotube.cn",
        "X-Requested-With": "XMLHttpRequest"
    }

    put_data = MultipartEncoder({
        'product': '1',
        'module': module,  # 1为接口 2为后管
        'project': '1',
        'openedBuild[]': 'trunk',
        'assignedTo': assignedTo,
        'deadline': '',
        'type': 'codeerror',
        'os': '',
        'browser': '',
        'title': title,
        'color': '',
        'severity': severity,  # 严重程度
        'pri': pri,  # 优先级
        'story': '',
        'task': '31',
        'oldTaskID': '0',
        'steps': steps,
        'keywords': '',
        'status': 'active',
        'labels[]': '',
        'files[]': '',
        'uid': '5e7c45054dfea',
        'case': '0',
        'caseVersion': '0',
        'result': '0',
        'testtask': '0'
    })

    put_headers['Content-Type'] = put_data.content_type
    res = requests.post(url=put_url, headers=put_headers, data=put_data)
    print(res.text)


def data_util(data, html, msg):
    """传入禅道的数据做处理"""
    if isinstance(data['禅道记录'], str):
        info_data = json.loads(data['禅道记录'])
    else:
        info_data = data['禅道记录']
    severity = info_data['severity']
    module = info_data['module']
    pri = info_data['pri']
    assignedTo = info_data['assignedTo']
    f = data['function'].replace('\r', '').replace('\n', '').replace('\t', '')
    title = '【' + data['测试用例名称'] + '】' + data['name'] + f
    steps = '本次请求数据' + json.dumps(data['data']) + '<br>' + '本次返回数据' + str(html) + '<br>' + '期望结果为' + data[
        'excepted_code'] + '<br>' + '程序比较结果:' + str(msg)
    return severity, module, title, pri, steps, assignedTo


if __name__ == '__main__':
    while True:
        send_bug_to_cd(severity='4', module='1', title='测试标题', pri='2', steps="""测试内容""")
