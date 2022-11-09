import logging, time

from logging.handlers import TimedRotatingFileHandler


class MyRotatingFileHandler(TimedRotatingFileHandler):

    def __init__(
        self,
        filename
        , mode='a'
        , backupCount=0
        , encoding=None
        , delay=True
        , interval=1
        , when='MIDNIGHT'):
        super().__init__(filename=filename, when=when, 
        interval=interval, delay=delay)

        self.namer = self.addTimeToLog
        

    def addTimeToLog(self, logfile=None):
        """
        Modifies the log file when it rotates, but instead of using the 
        default suffix it will add time before
        Args:
            log (_type_): _description_

        Returns:
            _type_: _description_
        """
        if logfile.endswith('log.log'):
            
            self.suffix = ''

            if self.when == 'S':
                format = "%Y-%m-%d_%H-%M-%S"
            elif self.when == 'M':
                format = "%Y-%m-%d_%H-%M"
            elif self.when == 'H':
                format = "%Y-%m-%d_%H"
            elif self.when == 'D' or self.when == 'MIDNIGHT':
                format = "%Y-%m-%d"
            elif self.when.startswith('W'):
                format = "%Y-%m-%d"

            t = time.strftime(format, time.localtime(self.rolloverAt))
                
            return logfile.replace('log.log', 'log_{}.log'.format(t))

        raise Exception('Log file must end in log.log')

def createLogger(
    name, 
    log_file = None,
    log_fmt = None,
    file_log_level = None,
    stream_fmt = None,
    stream_level = None,
    rotate_when='MIDNIGHT',
    rotate_interval=1):
    """    
    Create the different logger should you want a separate
    configuration for separate loggers. The log file handler 
    is initiated using the file_log__level
    Args:
        name ([str]): name of the logger
        log_file ([str]): log file name. File MUST end in log.log
        log_fmt ([str]): log file formatter
        file_log_level ([str]):   logging level for file handler.
        stream_fmt ([string]): Assign a separate config for steam handler.
        stream_level (str, optional): log level for streamhandler

    Returns:
        [logging.Logger]: logger sub class of the logger with timed file rotation
    """
    if log_file == None and stream_level == None:
        raise('Logger must have a log file and/or stream level defined')

    logger = logging.getLogger(name)
    default_formatter = logging.Formatter('%(asctime)s - %(levelname)s, %(message)s')


    if log_file:
        fh = MyRotatingFileHandler(filename=log_file, when=rotate_when, interval=rotate_interval)
        if log_fmt == None:
            fh.setFormatter(default_formatter)
        else:
            file_log_formatter = logging.Formatter(log_fmt)
            fh.setFormatter(file_log_formatter)
        logger.addHandler(fh)
         
    if stream_level:
        sh = logging.StreamHandler()
        sh.setLevel(getattr(logging, stream_level))
        if stream_fmt:
            stream_formatter = logging.Formatter(stream_fmt)
            sh.setFormatter(stream_formatter)
        else:
            stream_formatter = logging.Formatter(stream_fmt)
            sh.setFormatter(stream_formatter)
        logger.addHandler(sh)
        
    if file_log_level:
        logger.setLevel(getattr(logging, file_log_level))
    else:
        logger.setLevel(logging.WARNING)
    return logger
    
