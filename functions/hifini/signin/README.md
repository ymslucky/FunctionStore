# HIFINI 社区签到

### 一、业务逻辑

1. 使用Cookie加载签到页面，获取签到码——sign
2. 使用签到码签到

### 二、部署流程

1. 配置环境变量COOKIE
2. 连接Github仓库，配置根目录为`functions/hifini/signin`
3. 配置入口点Entrypoint=`main.py`
4. 配置构建命令`pip install -r requirements.txt`