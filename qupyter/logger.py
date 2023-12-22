import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(
        name,
        level=logging.DEBUG,
        filename: str = None,
        when: str = 'h',
        interval: int = 1,
        backup_count: int = 24,
) -> logging.Logger:

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # create formatter
        formatter = logging.Formatter('%(asctime)s %(levelname).1s %(name)s: %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        if filename is not None:
            fh = TimedRotatingFileHandler(filename, when=when, backupCount=backup_count, interval=interval)
            fh.setLevel(level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    return logger
