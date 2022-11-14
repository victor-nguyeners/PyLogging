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
                
            return logfile.replace('log', '_{}.log'.format(t))

        raise Exception('Log file must end in log.log')

def myLogger(
        name, log_file=None, log_fmt=None, logfile_level=None, 
        stream_fmt=None, stream=False, stream_level=None, when='MIDNIGHT', 
        interval=10, propogate=True) -> logging.Logger:
    """    
    Create the different logger should you want a separate
    configuration for separate loggers. The log file handler 
    is initiated using the file_log__level.
    """
    if log_file == None and stream_level == None:
        raise('Logger must have a log file and/or stream level defined')

    logger = logging.getLogger(name)
    default_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Using the log_file file name as the indicator to set up the log to file
    # We expect most usage around not defining a custom formatter so we
    # check for the None first.
    if log_file:
        fh = MyRotatingFileHandler(
            filename=log_file, when=when, interval=interval)
        if log_fmt == None:
            fh.setFormatter(default_formatter)
        else:
            file_log_formatter = logging.Formatter(log_fmt)
            fh.setFormatter(file_log_formatter)
        logger.addHandler(fh)
    
    if stream:
        sh = logging.StreamHandler()
        if stream_level:
            sh.setLevel(getattr(logging, stream_level))
        else:
            if logfile_level == None:
                sh.setLevel(logging.ERROR)
            else:
                sh.setLevel(getattr(logging, logfile_level))
        if stream_fmt:
            stream_formatter = logging.Formatter(stream_fmt)
            sh.setFormatter(stream_formatter)
        else:
            sh.setFormatter(default_formatter)
        logger.addHandler(sh)
        
    if logfile_level:
        logger.setLevel(getattr(logging, logfile_level))
    else:
        logger.setLevel(logging.WARNING)
    if propogate == False:
        logger.propagate = False
    return logger
