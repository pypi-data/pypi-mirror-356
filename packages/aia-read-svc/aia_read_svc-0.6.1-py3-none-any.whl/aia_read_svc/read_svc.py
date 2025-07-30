from dotenv import load_dotenv
import os
from .repositories.aiaRepo import AIAMessageRepository
from .wh40kSvc import Warhammer40KService
from aia_utils.logs_cfg import config_logger
import logging
config_logger()
logger = logging.getLogger(__name__)
load_dotenv()

class ReadSvc:
    def __init__(self, topic_producer, topic_consumer, version):
        self.topic_producer = topic_producer
        self.topic_consumer = topic_consumer
        self.aiaMsgRepo = AIAMessageRepository(os.environ['MONGODB_URI'])
        self.version = version
        self.wh40k = Warhammer40KService(self.topic_producer, version, os.getenv("WH40K_IMG_FILES_PATH"))

    def readDaemon(self):
        queueConsumer = QueueConsumer(self.topic_consumer, "aia_read_svc")
        queueConsumer.listen(self.callback)


    def callback(self, msgDict):
        text = "Llegó un mensaje!"
        print(text)
        try:
            print(str(msgDict["cmd"]))
            if msgDict["cmd"].upper() == "wh40k".upper():
                logger.info("Llegó un mensaje de wh40k!")
                self.wh40k.process_wh40k_obj(msgDict['semanticGraph']['sentence'])
            if msgDict["cmd"].upper() == "READ_YAHOO_MAIL".upper():
                logger.info("Llegó un mensaje de READ_YAHOO_MAIL!")
                
        except KeyError:
            print("[WARN] not cmd field in message")
            pass