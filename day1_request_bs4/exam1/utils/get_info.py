import requests

if __name__ == '__main__':
    url1='http://127.0.0.1:5000/hello?name=刘奇梦&classes=2010A'
    # 使用requests访问hello接口，传参为自己的姓名，班级信息
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24"
    }
    res=requests.get(url=url1,headers=headers)
    print(res.text)
    print(res.status_code)
    print(res.url)
    print(res.json())

    url2='http://127.0.0.1:5000/add'
    data={'name':'刘奇梦','classes':'2010A'}
    res=requests.post(url=url2,data=data,headers=headers)
    print(res.text)
    print(res.status_code)
    print(res.url)
    print(res.json())
    # 6．使用requests访问add接口，传参为自己的姓名，班级信息
    # 7．分别打印上述两个返回值response
    # 8．获取response的状态码，以及文本信息，url地址，json解析后的数据