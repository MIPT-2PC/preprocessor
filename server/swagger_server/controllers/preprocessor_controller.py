import connexion
import six

from swagger_server.models.table import Table  # noqa: E501
from swagger_server import util
from flask import Flask, Response
from .additional_func import *

from ..config import *
import copy

PreprocessorRoutineInst = PreprocessorRoutine()


def get_table():  # noqa: E501
    """hello message to get preprocessed data

    Returns preprocessed table for this user, masked input and outputs # noqa: E501

    :rtype: List[Table]
    """

    print("get_table was triggered by ClientB")

    PreprocessorRoutineInst.ClientBTrigger = True

    '''
    while PreprocessorRoutineInst.ClientATrigger == False or PreprocessorRoutineInst.ClientBTrigger == False:
        # тут должен быть таймер, а по таймауту возвращать:
        # return "Computation Error", 500
        continue
    '''
    while (PreprocessorRoutineInst.ClientATrigger == False):
        continue

    print("get_table is unlocked")

    def generate():
        yield str([PreprocessorRoutineInst.outputTableForClientB]).replace("\'", "\"")
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

    #print(ConfigParserInstance.nodes[0])
    #print(ConfigParserInstance.nodes[0].inn)
    #print(ConfigParserInstance.nodes[0].out)
    #print(ConfigParserInstance.nodes[0].inList)
    #print(ConfigParserInstance.numOfLinks)

    # предположим, что мы написали алгоритм, тогда смотрим, в каком формате нужно вернуть Response:
    # https://app.swaggerhub.com/apis/ProValdi/preprocessor/1.0.0#/interaction/start2PC
    # вернуть нужно List[Table], но Table задан просто как {}, поэтому тупа возвращаем сгенерированный [джейсон],
    # Например, на основе результатов алгоритма мы сгенерировали ответ в виде json, пусть это переменная outputTableForClientA
    # тогда Response будет выглядеть так:
    # return [outputTableForClientA], 200
    # чуть позже добавим обработку ошибок (коды 400, 500)

    # Сейчас, для примера, я верну фейковые данные, но в правильном формате

    nodesA = copy.deepcopy(ConfigParserInstance.nodes)  # просто присваивать не стоит, ...ance.node - копируется ссылка на объект SimpleNamespace
    nodesB = copy.deepcopy(ConfigParserInstance.nodes)

    list_of_masks = generateInput(ConfigParserInstance.numOfLinks)

    for i in range(ConfigParserInstance.numOfNodes):
        nodesA[i].operation = [0] * 4
        nodesB[i].operation = [0] * 4

        result_A = result_Creation()
        nodesA[i].operation[0] = result_A[0]
        nodesA[i].operation[1] = result_A[1]
        nodesA[i].operation[2] = result_A[2]
        nodesA[i].operation[3] = result_A[3]

        result_B = matrix_B_Creation(result_A, list_of_masks, nodesA[i].inList + nodesA[i].outList,
                                     ConfigParserInstance.nodes[i].operation)
        nodesB[i].operation[0] = result_B[0]
        nodesB[i].operation[1] = result_B[1]
        nodesB[i].operation[2] = result_B[2]
        nodesB[i].operation[3] = result_B[3]

    inputMasksForA = 0
    inputMasksForB = 0
    for i in range(ConfigParserInstance.AinputBitness):
        inputMasksForA = inputMasksForA << list_of_masks[i] | 1
        inputMasksForB = inputMasksForB << list_of_masks[i + 32] | 1

    stri = ""
    for i in reversed(range(int(ConfigParserInstance.numOfLinks))):
        if i < int(ConfigParserInstance.numOfLinks) - int(ConfigParserInstance.resultBitness):
            break
        stri = stri + str(list_of_masks[i])
    out = int(stri, 2)

    outputTableForClientA = {}
    outputTableForClientA['config'] = {
        "numOfLinks": str(ConfigParserInstance.numOfLinks),
        "numOfNodes": str(ConfigParserInstance.numOfNodes),
        "masksBitness": str(ConfigParserInstance.AinputBitness),
        "inputMasks": str(inputMasksForA),  # см описание ниже
        "outputMasks": str(out)  # см описание ниже
    }

    outputTableForClientB = {}
    outputTableForClientB['config'] = {
        "numOfLinks": str(ConfigParserInstance.numOfLinks),
        "numOfNodes": str(ConfigParserInstance.numOfNodes),
        "masksBitness": str(ConfigParserInstance.BinputBitness),
        "inputMasks": str(inputMasksForB),  # см описание ниже
        "outputMasks": str(out)  # см описание ниже
    }

    #print(outputTableForClientA)
    #print(outputTableForClientB)

    '''
        вместо того, чтобы передавать массив маскирующих битов, можно сэкономить память и передать 
        десятичное число, которое кодирует эти маскируюшие биты
        12 = 1100
        с дополнением до 32 битов (согласно конфигу - maskBitness):
        00000000.00000000.00000000.00001100 - точкой разделил для удобства
        Как быстро достать бит и применить его? Очень просто:
        inputMasks >> i & 1 - получим i-й бит справа (нумерация с нуля)
        
          00000000.00000000.00000000.000011 
        00000000.00000000.00000000.00000001 
    '''

    # до этого nodes был объектом типа namespace, нам же нужно получить обратно питоновский словарь
    # на самом деле вернётся list из одного словаря, поэтому потом словарь нужно будет получить методом .pop()
    nodesDictFromSimpleNamespaceB = json.loads(json.dumps(nodesB, default=lambda s: vars(s)))
    nodesDictFromSimpleNamespaceA = json.loads(json.dumps(nodesA, default=lambda s: vars(s)))
    #print(nodesDictFromSimpleNamespaceA)
    #print(nodesDictFromSimpleNamespaceB)

    for i in range(ConfigParserInstance.numOfNodes):
        outputTableForClientA['node' + str(i + 1)] = {}
        outputTableForClientA['node' + str(i + 1)].update(nodesDictFromSimpleNamespaceA.pop())

        outputTableForClientB['node' + str(i + 1)] = {}
        outputTableForClientB['node' + str(i + 1)].update(nodesDictFromSimpleNamespaceB.pop())

    PreprocessorRoutineInst.outputTableForClientA = outputTableForClientA
    PreprocessorRoutineInst.outputTableForClientB = outputTableForClientB

    PreprocessorRoutineInst.ClientATrigger = True

    return [PreprocessorRoutineInst.outputTableForClientA], 200
