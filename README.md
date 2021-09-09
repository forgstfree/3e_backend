# 3E后端项目
由Django实现，并集成Vue的前端
## 部署
1. uwsgi作为web服务器
 0. 安装 `conda install -c conda-forge uwsgi` pip安装由于版本太久或者gcc版本太高等原因，安装失败
 1. 启动 `uwsgi --ini uwsgi.ini`
 2. 重新加载配置文件 `uwsig --reload log/uwsgi.pid`, log/uwsgi.pid 需根据配置情况进行调整
 3. 停止 `uwsgi --stop log/uwsgi.pid`
2. nginx作为代理服务器
 1. 配置文件
    ```bash
	
    ```
