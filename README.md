# 🔥🔥 Use PYTHON 3.10 🔥🔥


## Quick Start 📚


## Installation
```shell
git clone https://github.com/doge-8/RacerToken.git
cd RacerToken
```

You can also use arguments for quick start, for example:
```shell
~/RacerToken >>> python3 main.py --action (1/2)
# Or
~/RacerToken >>> python3 main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

##配置安装脚本，包含安装python3.10

确保nginx运行正常
```shell
sudo apt-key del ABF5BD827BD9BF62
sudo wget https://nginx.org/keys/nginx_signing.key
sudo apt-key add nginx_signing.key
sudo apt-get update
```
添加库
```shell
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
```
开始安装
```shell
sudo apt-get install python3.10
```
安装pip
```shell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.10 get-pip.py
```
配置环境
```shell
python3.10 -m venv venv
source venv/bin/activate
python3.10 -m pip install -r requirements.txt
```
填写api码
```shell
vim .env-example   #修改填入api id和api hash，nano或者记事本修改都可以
cp .env-example .env
```
运行脚本（先选2创建账户文件，需要账号密码登录。成功登录后使用1启动脚本）
```shell
python3.10 main.py
```



