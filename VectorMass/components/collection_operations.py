import numpy as np
from VectorMass.config.configuration import ConfigurationManager

class Collection:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        print(self.conn, self.cursor)