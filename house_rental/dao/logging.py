from loguru import logger


def init_logging(logging_conf: dict):
    """
    配置项目日志信息
    :param logging_conf: 项目日志配置
    :return:
    """
    for log_handler, log_conf in logging_conf.items():
        log_file = log_conf.pop('file', None)
        logger.add(log_file, **log_conf)
