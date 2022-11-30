# weibo_Keyword
##### 新浪微博#关键字#话题搜索页面高清图片下载

基于Python3.8.10 + selenium 实现

适用平台：Windows10 + Chrome



##### 0.准备工作

拉取代码

安装Chrome浏览器：https://www.google.cn/chrome/

下载浏览器版本对应的chromedriver.exe ：https://chromedriver.chromium.org/downloads 

并放入driver文件夹

打开Chrome浏览器进入微博首页登录账号

关闭浏览器



##### 1.配置相关参数

安装依赖库：

```python
pip install -r requirements.txt
```

打开keyword_list.txt文件输入关键词，多个换行

打开main.py文件设置其他参数：

```python
import os
from keywords import Keyword
import Mek_master as Master

Master.logo_Slabt('Running')

# 通过文件构建关键词列表
key_list = Master.read_file('keyword_list.txt').split('\n')

k = Keyword()

#k.start_date = '2022-10-31'  # 开始日期
#k.end_date = '2022-10-31' # 结束日期

for key in key_list:
    k.main(k.build_tasks(key))

k.exit()

```



##### 2.开始下载

```bash
python mian.py
```

