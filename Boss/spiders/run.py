from scrapy.cmdline import execute

import sys
import os

# 设置工程的目录，可以在任何路径下运行execute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

city = "厦门市"
keyword = "瑞幸咖啡"

execute('scrapy crawl Boss_zp -a city={0} -a keyword={1}'.format(city,keyword).split())
