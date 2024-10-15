## 这是查询天气系统的coding test

体验网站: https://www.source-cn.net/query_weather

### 目前使用的部署方案是 安装venv虚拟环境 + 源码部署. (很丑陋, 因为服务器在国内,下载依赖很麻烦) 后续完善,  计划使用容器化部署 k8s or docker


![My Project Logo](https://github.com/a0x5b22bbb/QueryWeatherServer/blob/master/%E6%88%AA%E5%9B%BE1.png)


![My Project Logo](https://github.com/a0x5b22bbb/QueryWeatherServer/blob/master/%E6%88%AA%E5%9B%BE2.png)



启动方法: 

sudo apt update

sudo apt upgrade -y

sudo apt install python3 python3-pip -y

sudo apt install python3-venv -y

python3 -m venv venv

source venv/bin/activate

### 如果可以 使用 git pull 
cd /path/to/your/flask/project
pip install -r requirements.txt

### 因为是coding test 所以用dev server 运行, 生产环境可以使用nginx / uwsgi / gunicorn
nohup python3 main.py > /dev/null  2>&1 &

### 以很丑陋的方式运行.后续会完善

### 访问 localhost:8000/apidocs  或者  https://127.0.0.1:8000/apidocs/ (目前还有问题) 查看相关API接口文档.

