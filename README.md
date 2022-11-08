## 数据生产

### 需求/设计/开发文档
http://wiki.bigquant.ai/pages/viewpage.action?pageId=265912341


## 初始化数据库
```
cd /var/app/enabled/bigdataproduction
aerich init -t dataplatform.settings.TORTOISE_ORM
aerich --app dataplatform init-db
```

## 本地开发调试

```
# 设置环境变量 或者添加到 bashrc / zshrc 中

# DB_URI 默认值为下面的值，可以自行设置成自己的
export DB_URI="postgres://postgres:123456@127.0.0.1:5432/bigquant_service"

export DEBUG="True"
export SHOW_API_DOC="True"
export IGNORE_TOKEN_AUTH="True"

# 启动服务命令
uvicorn service:app --host 0.0.0.0 --port 8000 --loop uvloop --http httptools --workers 1 --reload

# 文档访问地址
http://127.0.0.1:8000/api/dataproduction/docs

```