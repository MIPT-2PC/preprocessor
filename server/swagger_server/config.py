#from swagger_server import *  # noqa: E501
from swagger_server import util

import json
from types import SimpleNamespace
import operator

class ConfigParser:

    def __init__(self, body):

        # загружаем секцию конфига из прилетевшего реквеста в виде объекта (SimpleNamespace - библиотека)
        configSection = json.loads(json.dumps(body['config']), object_hook=lambda d: SimpleNamespace(**d))

        self.numOfLinks = int(configSection.numOfLinks) # количество линков в цепи (конфиге)
        self.numOfNodes = int(configSection.numOfNodes) # количество узлов в цепи (конфиге)
        self.AinputBitness = int(configSection.AinputBitness) # количество бит клиента А
        self.BinputBitness = int(configSection.BinputBitness) # количество бит клиента B
        self.resultBitness = int(configSection.resultBitness) # количество бит результата


        self.nodes = [0] * self.numOfNodes

        '''
            Создаём массив узлов, в котором по индексам лежат десериализованные (представлены в виде объектов) ноды
            Это даёт возможность обращаться к полям узлов через точку: 
                >>> print(node[23].operation)
                вывод: 'XOR'
        '''
        for i in range(self.numOfNodes):
            self.nodes[i] = json.loads(json.dumps(body['node' + str(i + 1)]), object_hook=lambda d: SimpleNamespace(**d))

class PreprocessorRoutine:
    serverdict = []
    ClientATrigger = False
    ClientBTrigger = False
    outputTableForClientA = {}

    def clearInstance(self):
        self.serverdict = []
        self.ClientATrigger = False
        self.ClientBTrigger = False
        self.outputTableForClientA = {}

'''
это сохранено для дальшейшей разработки
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
'''

