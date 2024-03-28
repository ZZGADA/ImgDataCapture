# 爬取图片脚本
import requests
from urllib import request
import urllib
import random
import pandas as pd
import time
import os


class CaptureImgService:
    def __init__(self, _data_capture_head: str, _capture_url_head: str, _needed_files: list, _end_txt: str):
        self.__data_capture_head = _data_capture_head  # 数据存储的包头路径
        self.__capture_url_head = _capture_url_head  # 存放爬取数据url路径的文件
        self.__needed_files = _needed_files
        self.__end_txt = _end_txt
    
    '''
        爬取图片的核心逻辑，内容包括：
            1.通过pandas读取文件，读入我们想要的url路径
            2.根据读入的url路径，去网络爬取文件
            3.将爬取到的图片写入本地的文件夹
        label: str  必传    存放图片url文件的文件名
        flag:  int  可以不传 文本读取从第几行开始读取，如果已经有3个文件爬取完毕，那么就传入参数3表示跳过前3个url 从第4个开始爬取
    '''
    
    def get_img_by_url(self, label: str, flag: int = 0):
        #  pandas读取文件
        table = pd.read_table(f'{self.__capture_url_head}{label}{self.__end_txt}', header=None, names=['url'],
                              skiprows=flag)
        path = self.__data_capture_head + label + '/'
        
        opener = urllib.request.build_opener()
        # 构建请求头列表每次随机选择一个 用于防止反爬虫检测
        # 这些是请求头中的User-Agent参数 用于模拟实际浏览器的请求访问 各位可以在自己使用的浏览器按F12 抓包一下数据就看到浏览器发出请求头的User-Agent字段
        # 可以自由的向这个列表中加入自己浏览器的User-Agent参数
        ua_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'
                   ]
        
        count = 0
        error_count = 0
        url_data: pd.Series = table.loc[:, "url"]  # 读取指定列
        total_size = url_data.size
        
        print("===> 正在爬取 " + label)
        while True:
            try:
                if count > total_size - 1:
                    break
                url = url_data.get(count)
                agent = random.choice(ua_list)
                opener.addheaders = [('User-Agent', agent)]  # 加载user-agent
                urllib.request.install_opener(opener)  # urlib 加载opener
                file_head = label.title() + '_' + str(count)
                request.urlretrieve(url, path + file_head + url[url.rfind(
                    "."):])  # 下载图片 第一个参数：l爬取图片的url路径  第二个参数：下载图片的路径（需要加上文件格式）
                count += 1
                wait_time = round(random.uniform(1, 3), 1)
                print(f'\r[={count * "="}>] {count}/{total_size}  | 下一次请求请等待{wait_time}秒', end="")  # 显示当前状态
                time.sleep(wait_time)  # 1~3秒随机睡眠 防止被反爬虫检测
            
            except Exception as e:
                # 如果爬取错误失败次数超过三次 那么就跳过这个url
                if error_count >= 3:
                    count += 1
                    error_count = 0
                    continue
                print(f'\n{e}', end="")
                error_count += 1
        print(f'\n<=== 爬取 {label} 结束')
    
    '''
        创建所需的文件和文件夹
        文件：url路径文档
        文件夹：存放爬取图片地址的文件夹
        
        注意：文件和文件夹的层级不要超过README.md的显示
    '''
    
    def dir_and_file_init(self):
        # 创建存放爬取图片的文件夹
        for needed_dir in self.__needed_files:
            needed_dir_path = self.__data_capture_head + needed_dir
            # 分两步创建文件夹和子文件夹
            if not os.path.exists(self.__data_capture_head):
                os.mkdir(self.__data_capture_head)
            if not os.path.exists(needed_dir_path):
                os.mkdir(needed_dir_path)
        
        # 创建存放图片地址url路径的文件
        for needed_file in self.__needed_files:
            needed_file_path = self.__capture_url_head + needed_file + self.__end_txt
            if not os.path.exists(self.__capture_url_head):
                os.mkdir(self.__capture_url_head)
            
            if not os.path.exists(needed_file_path):
                file = open(needed_file_path, 'w')
                file.close()

  
if __name__ == '__main__':
    data_capture_head = './data_capture/'  # 数据存储的包头路径 结尾必须带/
    capture_url_head = './capture_url/'  # 存放爬取数据url路径的文件 结尾必须带/
    
    # 爬取数据类型定义
    bomber = 'bomber'  # 轰炸机
    carrier = 'carrier'  # 航母
    destroyer = 'destroyer'  # 驱逐舰
    helicopter = 'helicopter'  # 直升机
    needed_files = [bomber, carrier, destroyer, helicopter]
    
    end_txt = '.txt'  # 存放url路径的结尾格式文件
    
    # 初始化实例
    capture_img_service = CaptureImgService(_data_capture_head=data_capture_head,
                                            _capture_url_head=capture_url_head,
                                            _needed_files=needed_files,
                                            _end_txt=end_txt)
    # 初始化文件夹
    capture_img_service.dir_and_file_init()
    
    # 依次选择bomber carrier destroyer helicopter 顺序无所谓
    # 可以自行修改脚本 循环遍历爬取图片 或者开启多线程任务 实现多线程抓取
    # 函数参数的具体意义看函数体的注释
    capture_img_service.get_img_by_url(bomber)
