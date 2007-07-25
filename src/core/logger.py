import logging
from datetime import datetime

FORMAT_LOG = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT_LOG)

class Logger:
    def __init__(self):
	self.error_msgs = ''
	self.warning_msgs = ''
	self.info_msgs = ''
	self.debug_msgs = ''

    def error(self, msg, args = ''):
	if args:
	    logging.error(msg,args)
	    self.error_msgs += msg % args +'\n'
	else:
	    logging.error(msg)
	    self.error_msgs += msg +'\n'


    def warning(self, msg, args = ''):
	if args:
	    logging.warning(msg,args)
	    self.warning_msgs += msg % args +'\n'
	else:
	    logging.warning(msg)
	    self.warning_msgs += msg +'\n'

    def info(self, msg, args = ''):
	if args:
	    logging.info(msg,args)
	    self.info_msgs += msg % args +'\n'
	else:
	    logging.info(msg)
	    self.info_msgs += msg +'\n'

    def debug(self, msg, args = ''):
	if args:
	    logging.debug(msg,args)
	    self.debug_msgs += msg % args +'\n'
	else:
	    logging.debug(msg)
	    self.debug_msgs += msg +'\n'


