import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    # filename='myapp.log',
    # filemode='w'
)
