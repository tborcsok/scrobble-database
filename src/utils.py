from datetime import date
import logging

def custom_logger():
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', 
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S%z')
