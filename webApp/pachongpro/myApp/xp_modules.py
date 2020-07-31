import requests
import numpy as np
import json

# json数据url
url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"

def get_json(url, page):
    # 网页的url
    url1 = "https://www.lagou.com/jobs/list_python%E5%B7%A5%E7%A8%8B%E5%B8%88?labelWords=&fromSearch=true&suginput="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        'origin': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'first': 'true',
        'pn': page,
        'kd': 'python工程师'}
    print("第", page, "页的内容： ")
    s = requests.Session()
    print('建立session：', s)
    s.get(url=url1, headers=headers, timeout=3)
    cookie = s.cookies
    print('获取cookie：', cookie)
    res = requests.post(url, headers=headers, data=data, cookies=cookie, timeout=3)
    res.raise_for_status()
    res.encoding = 'utf-8'
    page_data = res.json()
    print('请求响应结果：', page_data, '\n\n')
    # 返回招聘信息
    return page_data


def getData_n():
    positionResult = []
    for one in range(15):
        page_data = get_json(url, one + 1)
        for result in page_data["content"]["positionResult"]["result"]:
            positionResult.append(result)
    # print(positionResult)
    return positionResult

'''
获取得到职位的所有信息： getData_n
根据工资分类信息： 
    positionSalaryDic 提取工资，所有的信息
    salaryDic 分类后的工资信息
'''
def getPositionSalaryDic():
    #　获取职位的所有信息
    positionResult = getData_n()
    # 提取工资，所有的信息
    positionSalaryDic = []
    '''
    工资的分类：
        0～8000
        8000～9000
        9000～10000
        10000～12000
        >12000
    '''
    # 分类后的工资信息
    num = [0, 0, 0, 0, 0]
    salaryDic = {
        "salary1": [],
        "salary2": [],
        "salary3": [],
        "salary4": [],
        "salary5": [],
        "num": num
    }
    for rs in positionResult:
        postion = {}
        salary_max = 0
        salary_min = 0
        # 切片获取工资
        salary = rs["salary"]
        if len(salary) >= 7:
            salary_max = int(salary[0:2]) * 1000
            salary_min = int(salary[4:6]) * 1000
        elif (len(salary) < 7) and (len(salary) >= 6):
            salary_max = int(salary[0:1]) * 1000
            salary_min = int(salary[3:5]) * 1000
        else:
            salary_max = int(salary[0:1]) * 1000
            salary_min = int(salary[3:4]) * 1000
        # print(salary, salary_max, salary_min, "\n")
        postion["salary_max"] = salary_max
        postion["salary_min"] = salary_min
        postion["companyFullName"] = rs["companyFullName"]
        postion["city"] = rs["city"]
        postion["district"] = rs["district"]
        postion["businessZones"] = rs["businessZones"]
        positionSalaryDic.append(postion)
        if salary_min > 0 and salary_max < 8000:
            num[0] +=1
            salaryDic["salary1"].append(postion)
        elif salary_min >= 8000 and salary_max < 9000:
            num[1] +=1
            salaryDic["salary2"].append(postion)
        elif salary_min >= 9000 and salary_max < 10000:
            num[2] +=1
            salaryDic["salary3"].append(postion)
        elif salary_min >= 10000 and salary_max < 12000:
            num[3] +=1
            salaryDic["salary4"].append(postion)
        else:
            num[4] +=1
            salaryDic["salary5"].append(postion)
    # print(salaryDic)
    # print(positionSalaryDic)
    return salaryDic

'''
根据最低工资进行排序
'''
def sortSalary(salaryDic):
    salaryDic.pop("num")
    dt = np.dtype([

    ])
    for salary in salaryDic.values():
        salary_tmp = np.array(salary)
        # np.sort(salary_tmp, kind="mergesort", order="salary_min")
        print(salary_tmp)
    # 通过np.sort排序

salaryDic = getPositionSalaryDic()
sortSalary(salaryDic)
