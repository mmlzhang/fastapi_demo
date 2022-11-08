import os

from .utils.osenv import OSEnv

# 项目名称
PROJECT_NAME = 'fastapi_demo'
# debug模式
DEBUG = os.getenv("DEBUG", False)

AUTHENTICATION_NAME = 'Authorization'

# TODO 临时测试， 测试完删除
IGNORE_TOKEN_AUTH = OSEnv.bool("IGNORE_TOKEN_AUTH", False, description="是否忽略token验证,临时调试使用")

SHOW_API_DOC = OSEnv.bool("SHOW_API_DOC", False, description="是否显示API文档")

SERVICE_URL_PREFIX = OSEnv.str("SERVICE_URL_PREFIX", default='', description="url前缀")

# 企业微信配置
WECOM_API_KEY = OSEnv.str("WECOM_API_KEY", default='', description="企业微信监控机器人key")
WECOM_MENTIONED_LIST = OSEnv.str("WECOM_MENTIONED_LIST", default='', description="企业微信提醒人员手机号码,多个用逗号隔开")

# 数据库设置
DB_URI = OSEnv.str("DB_URI", "postgres://postgres:123456@127.0.0.1:5432/demo", description="数据库连接字符串")
DB_TABLE_PREFIX = OSEnv.str("DB_TABLE_PREFIX", "dp__", description="数据库表名前缀")


TORTOISE_ORM = {
    "connections": {
        "aerich": DB_URI,
    },
    "apps": {
        # add `aerich.models` to satisfy aerich migration
        "aerich": {"models": ["aerich.models"], "default_connection": "aerich"},
        # "service": {"models": ["service.models"], "default_connection": "aerich"},
    },
}
