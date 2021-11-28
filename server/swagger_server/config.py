from swagger_server.models.results import *  # noqa: E501
from swagger_server import util

class ServerDict:
    serverdict = []

    def __init__(self):
        pass

    def add(self, result):
        self.serverdict.append(result)

    def get(self, index):
        result = self.serverdict.pop(index)
        self.serverdict.append(result) # we should just to get item, not to invoke
        return result

    def getAll(self):
        return self.serverdict.copy()

    def remove(self, body):
        if (body.ip, body.port) in self.serverdict:
            time = self.serverdict[(body.ip, body.port)][0]
            port_iperf = self.serverdict[(body.ip, body.port)][1]
            del self.serverdict[(body.ip, body.port)]
            return time
        raise Exception("no such server in dict")


ServerDictInst = ServerDict()