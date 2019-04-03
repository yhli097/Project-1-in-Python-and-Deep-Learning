# coding: utf-8
import requests
import json
import pandas as pd
import csv

#获取所有菜谱类型，写入EXCEL文件并返回
def get_alltype(appcode): 

    url = 'http://caipu.market.alicloudapi.com/showapi_cpType' #读取数据的网页
    headers = {'Authorization': 'APPCODE {}'.format(appcode)} #读取数据的格式

    r = requests.get(url, headers=headers) #读取数据

    content_json = json.loads(r.content) #将数据转为JSON格式

    df = pd.DataFrame(content_json['showapi_res_body']) #转换为数据框
    
    writer = pd.ExcelWriter('alltypes.xlsx') #默认存储位置为~/alltypes.xlsx
    df.to_excel(writer,'Sheet1')
    writer.save()

    return df #输出数据框


#获取某一类型菜谱的信息
def get_dish(Type, appcode):

    url = 'http://caipu.market.alicloudapi.com/showapi_cpQuery' #读取数据的网页
    payload = {'type': Type} #读取菜谱类型
    headers = {'Authorization': 'APPCODE {}'.format(appcode)} #读取数据格式

    r = requests.get(url, params=payload, headers=headers) #读取数据

    content_json = json.loads(r.content) #将数据转换为JSON格式

    df = pd.DataFrame(content_json['showapi_res_body']['datas']) #将数据转为数据框

    return df #输出数据框


#对多种类型多种菜谱进行数据框输出并写成EXCEL文件
def get_dishs(Types, appcode):
    dfs = []
    for Type in Types:
        temp_df = get_dish(Type, appcode)
        dfs.append(temp_df)
    dfs = pd.concat(dfs)
    
    writer = pd.ExcelWriter('certaintypes.xlsx') #默认存储位置为~/certaintypes.xlsx
    dfs.to_excel(writer,'Sheet1')
    writer.save()
    
    return dfs #输出数据框

#对某一具体菜名搜索,包括类别和名称
def get_food(Type, cpName, appcode):
    
    url = 'http://caipu.market.alicloudapi.com/showapi_cpQuery' #读取数据的网页
    payload = {'type': Type, 'cpName':cpName} #读取菜谱类型
    headers = {'Authorization': 'APPCODE {}'.format(appcode)} #读取数据格式
    
    r = requests.get(url, params=payload, headers=headers) #读取数据

    content_json = json.loads(r.content) #将数据转换为JSON格式

    df = pd.DataFrame(content_json['showapi_res_body']['datas']) #将数据转为数据框
    
    return df #输出数据框

#对若干菜品同时进行搜索
def get_foods(Types, cpNames, appcode):
    dfs = []
    for Type in Types:
        dfs_times = []
        for cpName in cpNames:
            temp_df = get_food(Type, cpName, appcode)
            dfs_times.append(temp_df)
        area_df = pd.concat(dfs_times)
        dfs.append(area_df)
    
    df = pd.concat(dfs)
    
    writer = pd.ExcelWriter('dishes.xlsx') #默认存储位置为~/dishes.xlsx
    df.to_excel(writer,'Sheet1')
    writer.save()
    
    return df