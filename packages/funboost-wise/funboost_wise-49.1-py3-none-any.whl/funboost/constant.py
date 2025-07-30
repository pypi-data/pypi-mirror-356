# coding= utf-8


class BrokerEnum:
    EMPTY = 'EMPTY'  # 空的实现，需要搭配 boost入参的 consumer_override_cls 和 publisher_override_cls使用，或者被继承。
    RABBITMQ_AMQPSTORM = 'RABBITMQ_AMQPSTORM'  # 使用 amqpstorm 包操作rabbitmq  作为 分布式消息队列，支持消费确认.强烈推荐这个作为funboost中间件。
    RABBITMQ = RABBITMQ_AMQPSTORM
    RABBITMQ_RABBITPY = 'RABBITMQ_RABBITPY'  # 使用 rabbitpy 包操作rabbitmq  作为 分布式消息队列，支持消费确认，不建议使用
    RABBITMQ_PIKA = 'RABBITMQ_PIKA'  # 使用pika包操作rabbitmq  作为 分布式消息队列。，不建议使用


class ConcurrentModeEnum:
    THREADING = 'threading'  # 线程方式运行，兼容支持 async def 的异步函数。
    GEVENT = 'gevent'
    EVENTLET = 'eventlet'
    ASYNC = 'async'  # asyncio并发，适用于async def定义的函数。
    SINGLE_THREAD = 'single_thread'  # 如果你不想并发，不想预先从消息队列中间件拉取消息到python程序的内存queue队列缓冲中，那么就适合使用此并发模式。
    SOLO = SINGLE_THREAD


# is_fsdf_remote_run = 0

class FunctionKind:
    CLASS_METHOD = 'CLASS_METHOD'
    INSTANCE_METHOD = 'INSTANCE_METHOD'
    STATIC_METHOD = 'STATIC_METHOD'
    COMMON_FUNCTION = 'COMMON_FUNCTION'


class ConstStrForClassMethod:
    FIRST_PARAM_NAME = 'first_param_name'
    CLS_NAME = 'cls_name'
    OBJ_INIT_PARAMS = 'obj_init_params'
    CLS_MODULE = 'cls_module'
    CLS_FILE = 'cls_file'


class RedisKeys:
    REDIS_KEY_PAUSE_FLAG = 'funboost_pause_flag'
    REDIS_KEY_STOP_FLAG = 'funboost_stop_flag'
    QUEUE__MSG_COUNT_MAP = 'funboost_queue__msg_count_map'
    FUNBOOST_QUEUE__CONSUMER_PARAMS = 'funboost_queue__consumer_parmas'
    FUNBOOST_QUEUE__RUN_COUNT_MAP = 'funboost_queue__run_count_map'
    FUNBOOST_QUEUE__RUN_FAIL_COUNT_MAP = 'funboost_queue__run_fail_count_map'
    FUNBOOST_ALL_QUEUE_NAMES = 'funboost_all_queue_names'
    FUNBOOST_ALL_IPS = 'funboost_all_ips'
    FUNBOOST_LAST_GET_QUEUE_PARAMS_AND_ACTIVE_CONSUMERS_AND_REPORT__UUID_TS = 'funboost_last_get_queue_params_and_active_consumers_and_report__uuid_ts'

    FUNBOOST_HEARTBEAT_QUEUE__DICT_PREFIX = 'funboost_hearbeat_queue__dict:'
    FUNBOOST_HEARTBEAT_SERVER__DICT_PREFIX = 'funboost_hearbeat_server__dict:'

    @staticmethod
    def gen_funboost_apscheduler_redis_lock_key_by_queue_name(queue_name):
        return f'funboost.BackgroundSchedulerProcessJobsWithinRedisLock:{queue_name}'

    @staticmethod
    def gen_funboost_hearbeat_queue__dict_key_by_queue_name(queue_name):
        return f'{RedisKeys.FUNBOOST_HEARTBEAT_QUEUE__DICT_PREFIX}{queue_name}'

    @staticmethod
    def gen_funboost_hearbeat_server__dict_key_by_ip(ip):
        return f'{RedisKeys.FUNBOOST_HEARTBEAT_SERVER__DICT_PREFIX}{ip}'

    @staticmethod
    def gen_funboost_queue_time_series_data_key_by_queue_name(queue_name):
        return f'funboost_queue_time_series_data:{queue_name}'

    @staticmethod
    def gen_funboost_redis_apscheduler_jobs_key_by_queue_name(queue_name):
        jobs_key = f'funboost.apscheduler.jobs:{queue_name}'
        return jobs_key

    @staticmethod
    def gen_funboost_redis_apscheduler_run_times_key_by_queue_name(queue_name):
        run_times_key = f'funboost.apscheduler.run_times:{queue_name}'
        return run_times_key
