该项目为 精通有道技术聚合团队 分布式队列爬虫项目。
一、项目环境
  1、python3
  2、celery4

二、工程结构
  1、apps: 1）celery_init.py，celery启动初始化；2）flask_init.py，fask启动初始化；3）timer_task.py，flask对外接口实例
    celery_init.py
    flask_init.py
    timer_task.py
 
   2、browser_interface：浏览器相关接口方法，涉及工厂方法，无头浏览器，requests cookies，代理等
   
   3、celery_tasks：celery具体任务可扩张
   
   4、config 项目相关配置文件
   
   5、db：数据库相关操作方法
   
   6、decorators：异常修饰器
   
   7、feng_huang_net：使用浏览器抓取的一个实例
   
   8、init_classes：一些手动执行的方法，目前大多数为微博抓取相关方法
   
   9、封装的日志方法：logger
   
   10、page_get、page_parse：微博获取、解析方法
   
   11、test、tests：测试相关方法
   
   12、celery_py.py:直接从pycharm 启动celery需要用到的启动脚本
   
   13、jtyd_spider_run.py：flask启动脚本
   
   14、jtyd_spider_run.sh：启动命令集合
   
   15、requirements.txt 需要的lib
   
   16、doc：其他相关文档
   
   
