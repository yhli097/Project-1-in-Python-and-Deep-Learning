import requests
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
import cv2
import matplotlib.pyplot as plt


#读取网页jpg图片，写入默认路径，并显示出来
def jpg(url, path):
    response = requests.get(url) #从网页抓取图片
    image = Image.open(BytesIO(response.content))
    image.save(path) #写入图片文件
 
    img = cv2.imdecode(np.fromfile(path,dtype=np.uint8),cv2.IMREAD_UNCHANGED)#打开含有中文路径的图片
    img2=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img2)
    plt.show() #显示该文件
    
#输入原数据框中steps每一项，展示steps具体内容及相关图片
def show_steps(step, name):
    dstep = pd.DataFrame(step) 
    n = dstep.shape[0] #求有多少个步骤
    for i in range(n):
        print("步骤%d:"%(i+1)) #打印“步骤i”
        print(dstep['content'][i]) #打印操作内容
        jpg(dstep['imgUrl'][i],'%s%d.jpg'%(name,i)) #打印相关图片

#输入原数据框中yl中每一项，将数据转换为直观的表格
def show_yl(yl):
    dyl = pd.DataFrame(yl) #将输入的list转换为表格
    dyl.columns=['配料名称', '数量'] #更改列名
    return dyl

#打印一道菜的名称、类型、介绍、图片、原料和过程
#并将名称、类型和介绍储存到txt文档
def show_dish(df):
    name = df['cpName']
    f = open("%s.txt"%(name), 'w+')
    
    print('菜名：',name, file=f) #打印菜名
    print('类型：',df['type'], file=f) #打印类型
    if df['tip']:
        print('介绍：',df['des'], file=f) #打印介绍
    
    path = '%s.jpg'%(name)
    jpg(df['largeImg'],path) #打印图片并保存
    
    print('配料如下：') 
    print(show_yl(df['yl'])) #打印配料表格
    
    print('制作步骤如下：')
    show_steps(df['steps'],df['cpName']) #打印制作步骤
    
    if df['tip']:
        print('温馨贴士：',df['tip']) #如果有tip则打印tip
        
    f.close()

#打印DataFrame中所有菜谱
def show_dishes(dfs):
    n = dfs.shape[0]
    for i in range(n):
        print("第%d道菜谱"%(i+1))
        show_dish(dfs.iloc[i]) #对每一行用show_dish函数
        print("\n")