import connexion
import six

from swagger_server.models.table import Table  # noqa: E501
from swagger_server import util
from flask import Flask, Response

from ..config import *
import copy

PreprocessorRoutineInst = PreprocessorRoutine()

def get_table():  # noqa: E501
    """hello message to get preprocessed data

    Returns preprocessed table for this user, masked input and outputs # noqa: E501


    :rtype: List[Table]
    """

    PreprocessorRoutineInst.ClientBTrigger = True

    while PreprocessorRoutineInst.ClientATrigger == False or PreprocessorRoutineInst.ClientBTrigger == False:
        # тут должен быть таймер, а по таймауту возвращать:
        # return "Computation Error", 500
        continue

    def generate():
        yield str([PreprocessorRoutineInst.outputTableForClientA]).replace("\'", "\"")
        PreprocessorRoutineInst.clearInstance()
        yield ''
    return Response(generate(), mimetype='application/json'), 200


def start2_pc(body=None):  # noqa: E501
    """start preprocessing procedure

    send config file to start preprocessing # noqa: E501

    :param body: Nums request body
    :type body: dict | bytes

    :rtype: List[Table]
    """
    if connexion.request.is_json:
        body = Table.from_dict(connexion.request.get_json())  # noqa: E501

    ConfigParserInstance = ConfigParser(body)  # надо добавить валидацию на ошибки для входных данных
    # после валидации можно дёрнуть триггер, что клиент А начал процедуру препроцессинга:

    PreprocessorRoutineInst.ClientATrigger = True

    # обращаемся к полям класса парсера для работы с ними
    # можно создать дополнительные переменные для удобного доступа к ним напрямую, а не через инстанс класса парсера
    print(ConfigParserInstance.nodes[0])
    print(ConfigParserInstance.numOfLinks)

    '''
        По идее тут нужно сделать так, под капотом:
        
        outputTableForClientA = PreprocessorRoutineInst.processTables(ConfigParserInstance)
        
        потом в конце сразу эту штуку и возвращаем
    
        я пока прямо в этой функции все сделаю
    
        create masks, tables for A
        create masks, tables for B
    '''

    # предположим, что мы написали алгоритм, тогда смотрим, в каком формате нужно вернуть Response:
    # https://app.swaggerhub.com/apis/ProValdi/preprocessor/1.0.0#/interaction/start2PC
    # вернуть нужно List[Table], но Table задан просто как {}, поэтому тупа возвращаем сгенерированный [джейсон],
    # Например, на основе результатов алгоритма мы сгенерировали ответ в виде json, пусть это переменная outputTableForClientA
    # тогда Response будет выглядеть так:
    # return [outputTableForClientA], 200
    # чуть позже добавим обработку ошибок (коды 400, 500)

    # Сейчас, для примера, я верну фейковые данные, но в правильном формате

    nodes = copy.deepcopy(
        ConfigParserInstance.nodes)  # просто присваивать не стоит, ...ance.node - копируется ссылка на объект SimpleNamespace
    nodes[0].operation = [0] * 4

    nodes[0].operation[0] = "1"
    nodes[0].operation[1] = "0"
    nodes[0].operation[2] = "1"
    nodes[0].operation[3] = "0"

    configForOutputTableA = {}
    configForOutputTableA['config'] = {
        "numOfLinks": str(ConfigParserInstance.numOfLinks),
        "numOfNodes": str(ConfigParserInstance.numOfNodes),
        "masksBitness": "32",
        "inputMasks": "12",  # см описание ниже
        "outputMasks": "24"  # см описание ниже
    }

    print(configForOutputTableA)

    '''
        вместо того, чтобы передавать массив маскирующих битов, можно сэкономить память и передать 
        десятичное число, которое кодирует эти маскируюшие биты
        12 = 1100
        с дополнением до 32 битов (согласно конфигу - maskBitness):
        00000000.00000000.00000000.00001100 - точкой разделил для удобства
        Как быстро достать бит и применить его? Очень просто:
        inputMasks >> i & 1 - получим i-й бит справа (нумерация с нуля)
    '''

    # до этого nodes был объектом типа namespace, нам же нужно получить обратно питоновский словарь
    # на самом деле вернётся list из одного словаря, поэтому потом словарь нужно будет получить методом .pop()
    nodesDictFromSimpleNamespace = json.loads(json.dumps(ConfigParserInstance.nodes, default=lambda s: vars(s)))

    outputTableForClientA = {}
    outputTableForClientA['config'] = {
        "numOfLinks": str(ConfigParserInstance.numOfLinks),
        "numOfNodes": str(ConfigParserInstance.numOfNodes),
        "masksBitness": "32",
        "inputMasks": "12",  # см описание ниже
        "outputMasks": "24"  # см описание ниже
    }
    for i in range(ConfigParserInstance.numOfNodes):
        outputTableForClientA['node' + str(i + 1)] = {}
        outputTableForClientA['node' + str(i + 1)].update(nodesDictFromSimpleNamespace.pop())

    PreprocessorRoutineInst.outputTableForClientA = outputTableForClientA

    while PreprocessorRoutineInst.ClientATrigger == False or PreprocessorRoutineInst.ClientBTrigger == False:
        # тут должен быть таймер, а по таймауту возвращать:
        # return "Computation Error", 500
        continue

    def generate():
        yield str([PreprocessorRoutineInst.outputTableForClientA]).replace("\'", "\"")
        PreprocessorRoutineInst.clearInstance()
        yield ''
    return Response(generate(), mimetype='application/json'), 200
