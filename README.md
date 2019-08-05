# Scrapy_Boss
 scrapy爬取BOSS直聘网职位信息

最近在学习scrapy框架，借机找了个项目练手。

[Boss直聘网](https://www.zhipin.com/) 没有常规的反爬虫机制，数据也很规整，很适合入门上手scrapy。

## 逻辑

- Boss直聘网站的每个搜索结果最多只展示10页，即300条数据

  

- 按照城市和搜索关键词爬取

  - 除了四个直辖市以外，不能直接按照省份爬取，只能遍历省份下的每个城市，然后分别爬取
  - 先爬取页面下的 [city.json](https://www.zhipin.com/wapi/zpCommon/data/city.json)，获取城市列表数据和对应的查询编号code
  - 命令行动态传参，如果输入的是省份，就爬取该省每个城市的信息，如果是城市就爬取对应城市

  

- 存进MySQL数据库。存储表名为 `城市名_搜索关键词` 的形式

## 文档

[Scrapy爬取Boss直聘时的问题与解决方案](https://merelysmile.github.io/2019-08-03/scrapy_boss/)

