from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


async def init_mysql(_app: FastAPI, db_config: dict):
    """
    初始化MySQL
    :param _app: FastAPI应用
    :param db_config: 数据库配置
    db_config
        {
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': {
                        'host': 'localhost',
                        'port': '5432',
                        'user': 'tortoise',
                        'password': 'qwerty123',
                        'database': 'test',
                    }
                },
            },
            'apps': {
                'models': {
                    'models': ['__main__'],             # model所在的目录
                    'default_connection': 'default',    # 对应使用的数据库连接
                }
            }
        }
    """
    [v["credentials"].setdefault("pool_recycle", 3540) for _, v in db_config["connections"].items()]
    register_tortoise(
        _app,
        config=db_config,
        generate_schemas=True,  # 如果数据库为空, 则自动生成对应数据表, 生产环境不要开
        add_exception_handlers=False,  # 生产环境不要开, 会泄露调试信息
    )
