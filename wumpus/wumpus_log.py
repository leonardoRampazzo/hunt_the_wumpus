import logging

class WumpusLog:
    def __init__(self):
        logger = logging.getLogger('wumpus_application')
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('wumpus.log')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)
        self.logger = logger
