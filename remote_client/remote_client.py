import math
import logging
import logging.config
import yaml
import queue
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from threading import Thread


broker = "192.168.1.60"
port = 1883


class Listener():
    """Listens for inbound MQTT messages"""
    def __init__(self, mqttc: mqtt.Client, topic: str):
        self.mqttc = mqttc
        self.topic = topic

    def on_connect(self, mqttc, obj, flags, rc):
        LoggingHandler.log_to_console("Connected")

    def on_message(self, mqttc, obj, msg):
        msg_handler_queue.put(msg)
        LoggingHandler.log_to_console(CsvDecoder.decode(msg))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        LoggingHandler.log_to_console(f'Subscribed: {self.topic} {mid} {granted_qos}')

    def run(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_message = self.on_message
        self.mqttc.connect(broker, port)
        self.mqttc.subscribe(self.topic, 0)
        self.mqttc.loop_forever()


class MessageHandler(Thread):
    """Decodes message and dispatches them to handlers"""
    def dispatch_message(message: str):
        dev, t1, t2, t3 = CsvDecoder.decode(message)
        action_handler_queue.put((dev, t1, t2, t3))
        LoggingHandler.log_to_file(f'{dev}, {t1:.2f}, {t2:.2f}, {t3:.2f}')

    def run(self):
        while True:
            msg = msg_handler_queue.get()
            MessageHandler.dispatch_message(msg)


class ActionHandler(Thread):
    """Generates outbound MQTT messages according to rule"""
    previous_event = False

    def test_rule(t1, t2, t3):
        is_tripped = False
        if Rule.rule(t1, t2, t3):
            is_tripped = True
            if ActionHandler.previous_event != is_tripped:
                publish.single("test/activate", "ON", hostname=broker)
                LoggingHandler.log_to_console("ON")
        else:
            is_tripped = False
            if ActionHandler.previous_event != is_tripped:
                publish.single("test/activate", "OFF", hostname=broker)
                LoggingHandler.log_to_console("OFF")
        ActionHandler.previous_event = is_tripped

    def run(self):
        while True:
            dev, t1, t2, t3 = action_handler_queue.get()
            if not math.isnan(t1) or math.isnan(t2) or math.isnan(t3):
                ActionHandler.test_rule(t1, t2, t3)


class LoggingHandler():
    """Handles logging to file and console - setup from YAML config"""
    file_logger = logging.getLogger("fileLogger")
    console_logger = logging.getLogger("root")

    with open('logger.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    def log_to_file(log_str):
        LoggingHandler.file_logger.info(log_str)

    def log_to_console(log_str):
        LoggingHandler.console_logger.debug(log_str)


class Rule():
    trip = 25.0

    def rule(t1, t2, t3) -> bool:
        if t1 >= Rule.trip and t2 >= Rule.trip and t3 >= Rule.trip:
            return True
        return False


class CsvDecoder():
    def decode(message) -> (str, float, float, float):
        msg_str = message.payload.decode('utf-8')
        dev, t1, t2, t3 = msg_str.split(',')
        return (dev, float(t1), float(t2), float(t3))


if __name__ == '__main__':
    mqttc = mqtt.Client()
    msg_handler_queue = queue.Queue()
    action_handler_queue = queue.Queue()
    message_handler = MessageHandler()
    action_handler = ActionHandler()

    action_handler.start()
    message_handler.start()

    listener = Listener(mqttc, "test/thermos")
    listener.run()
