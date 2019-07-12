import logging
 
def logDebug(str):
    logging.basicConfig(filename='fishPI.log',level=logging.DEBUG)
    logging.debug(str)
    print(str)

def logInfo(str):
    logging.basicConfig(filename='fishPI.log',level=logging.INFO)
    logging.info(str)
    print(str)

def logWarning(str):
    logging.basicConfig(filename='fishPI.log',level=logging.WARNING)
    logging.warning(str)
    print(str)




