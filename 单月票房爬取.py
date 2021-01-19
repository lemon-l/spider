import urllib.request
import urllib.parse
import json

post_url = 'http://www.endata.com.cn/API/GetData.ashx'

def Get_par(time):
    # 构造表单
    form_data = {
        'startTime':time,
        'MethodName':'BoxOffice_GetMonthBox',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    }

    request = urllib.request.Request(url = post_url, headers = headers)
    form_data = urllib.parse.urlencode(form_data).encode()
    response = urllib.request.urlopen(request, form_data).read().decode()
    # 将json格式数据转换为字典
    json_commet = json.loads(response)
    a = json_commet['Data']
    # 获取当月电影票房
    amount = a['Table1'][0]['amount'] / 10000
    # 获取人数
    people = a["Table1"][0]["people"] / 10000
    # 最后返回的结果
    result  = '票房为{0:.2f}，人次为{1:.2f}'.format(amount, people)
    print(result)

for j in range(2014,2020):
    for i in range(1, 13):
        time = '{0}-{1}-01'
        if(i < 10):
            time = time.format(str(j), '0'+str(i))
        else:
            time = time.format((j), str(i))
        print('{0}:'.format(time), end=" ")
        Get_par(time)
    


