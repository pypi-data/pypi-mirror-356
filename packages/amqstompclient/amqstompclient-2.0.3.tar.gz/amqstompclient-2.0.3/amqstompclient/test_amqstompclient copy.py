import amqstompclient
import unittest
import logging
import time

#git tag 1.0.1 -m "PyPi tag"
#git push --tags origin master
#python setup.py sdist
#python3 -m pip install --upgrade build
#python3 -m build
#twine upload dist/*

server={"ip":"localhost","port":"61613","login":"admin","password":"*******"}
logger=None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger()
    logger.info("Starting tests")

    def callback1(self, destination, message,headers):
        logger.info(message, "TEST_MYMESSAGECALLBACK")

    conn=amqstompclient.AMQClient(server, {"name":"TEST","version":"1.0.0"},["/queue/QTEST1","/queue/QTEST2","/topic/TTEST1","/topic/TTEST2"])        

    while (True):
        conn.send_message("/queue/QTEST1","TEST1_MYMESSAGE1")
        time.sleep(5)
