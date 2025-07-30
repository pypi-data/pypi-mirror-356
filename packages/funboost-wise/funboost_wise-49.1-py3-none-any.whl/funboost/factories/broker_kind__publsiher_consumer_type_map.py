import typing

from funboost.publishers.empty_publisher import EmptyPublisher
from funboost.publishers.rabbitmq_pika_publisher import RabbitmqPublisher
from funboost.consumers.empty_consumer import EmptyConsumer
from funboost.consumers.rabbitmq_pika_consumer import RabbitmqConsumer

from funboost.publishers.base_publisher import AbstractPublisher
from funboost.consumers.base_consumer import AbstractConsumer
from funboost.constant import BrokerEnum

broker_kind__publsiher_consumer_type_map = {
    BrokerEnum.RABBITMQ_PIKA: (RabbitmqPublisher, RabbitmqConsumer),
    BrokerEnum.EMPTY: (EmptyPublisher, EmptyConsumer),
}

for broker_kindx, cls_tuple in broker_kind__publsiher_consumer_type_map.items():
    cls_tuple[1].BROKER_KIND = broker_kindx


def register_custom_broker(broker_kind, publisher_class: typing.Type[AbstractPublisher], consumer_class: typing.Type[AbstractConsumer]):
    """
    动态注册中间件到框架中， 方便的增加中间件类型或者修改是自定义消费者逻辑。
    :param broker_kind:
    :param publisher_class:
    :param consumer_class:
    :return:
    """
    if not issubclass(publisher_class, AbstractPublisher):
        raise TypeError(f'publisher_class 必须是 AbstractPublisher 的子或孙类')
    if not issubclass(consumer_class, AbstractConsumer):
        raise TypeError(f'consumer_class 必须是 AbstractConsumer 的子或孙类')
    broker_kind__publsiher_consumer_type_map[broker_kind] = (publisher_class, consumer_class)
    consumer_class.BROKER_KIND = broker_kind


def regist_to_funboost(broker_kind: str):
    """
    延迟导入是因为funboost没有pip自动安装这些三方包，防止一启动就报错。
    这样当用户需要使用某些三方包中间件作为消息队列时候，按照import报错信息，用户自己去pip安装好。或者 pip install funboost[all] 一次性安装所有中间件。
    建议按照 https://github.com/ydf0509/funboost/blob/master/setup.py 中的 extra_brokers 和 install_requires 里面的版本号来安装三方包版本.
    """
    if broker_kind == BrokerEnum.RABBITMQ_AMQPSTORM:
        from funboost.publishers.rabbitmq_amqpstorm_publisher import RabbitmqPublisherUsingAmqpStorm
        from funboost.consumers.rabbitmq_amqpstorm_consumer import RabbitmqConsumerAmqpStorm
        register_custom_broker(BrokerEnum.RABBITMQ_AMQPSTORM, RabbitmqPublisherUsingAmqpStorm, RabbitmqConsumerAmqpStorm)

    if broker_kind == BrokerEnum.RABBITMQ_RABBITPY:
        from funboost.publishers.rabbitmq_rabbitpy_publisher import RabbitmqPublisherUsingRabbitpy
        from funboost.consumers.rabbitmq_rabbitpy_consumer import RabbitmqConsumerRabbitpy
        register_custom_broker(BrokerEnum.RABBITMQ_RABBITPY, RabbitmqPublisherUsingRabbitpy, RabbitmqConsumerRabbitpy)


if __name__ == '__main__':
    import sys

    print(sys.modules)
