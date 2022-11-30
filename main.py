import os
from keywords import Keyword
import Mek_master as Master

Master.logo_Slabt('Running')

# 通过文件构建关键词列表
key_list = Master.read_file('keyword_list.txt').split('\n')

k = Keyword()
k.start_date = '2022-10-31'
for key in key_list:
    k.main(k.build_tasks(key))

k.exit()
