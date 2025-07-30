from argparse import ONE_OR_MORE, ArgumentParser

from .yahooMailSvc import YahooMail
from .read_svc import ReadSvc
import os
from dotenv import load_dotenv
load_dotenv()
from aia_utils.toml_utils import getVersion

def run():
    """
    entry point
    """
    version = getVersion()
    print (f"STARTING READ SVC v{version} DAEMON")
    readSvc = ReadSvc(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], version)    
    readSvc.readDaemon() 

    #yahooMail = YahooMail(os.environ['CLOUDKAFKA_TOPIC_PRODUCER'], os.environ['CLOUDKAFKA_TOPIC_CONSUMER'], __version__)
    #yahooMail.mailDaemon()
