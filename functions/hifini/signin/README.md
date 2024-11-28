# HIFINI 社区签到

### 一、业务逻辑

1. 使用Cookie加载签到页面，获取签到码——sign
2. 使用签到码签到

### 二、部署流程

1. 连接Github仓库，配置根目录为`functions/hifini/signin`
2. 配置入口点Entrypoint=`main.py`
3. 配置构建命令`pip install -r requirements.txt`
4. 配置环境变量COOKIE
5. 配置Cron Schedule表达式为每小时执行一次`0 0-23 * * *`