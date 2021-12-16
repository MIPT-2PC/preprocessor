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

    nodesA = copy.deepcopy(ConfigParserInstance.nodes)
    nodesB = copy.deepcopy(ConfigParserInstance.nodes)

    list_of_masks = generateInput(ConfigParserInstance.numOfLinks)

    for i in range(ConfigParserInstance.numOfNodes):
        nodesA[i].operation = [0] * 4
        nodesB[i].operation = [0] * 4

        result_A, hashA0, hashA1 = result_Creation()
        nodesA[i].operation[0] = result_A[0]
        nodesA[i].operation[1] = result_A[1]
        nodesA[i].operation[2] = result_A[2]
        nodesA[i].operation[3] = result_A[3]

        nodesA[i].selfHash = [0] * 4
        nodesA[i].selfHash[0] = hashA1[0] if result_A[0] == 1 else hashA0[0]
        nodesA[i].selfHash[1] = hashA1[1] if result_A[1] == 1 else hashA0[1]
        nodesA[i].selfHash[2] = hashA1[2] if result_A[2] == 1 else hashA0[2]
        nodesA[i].selfHash[3] = hashA1[3] if result_A[3] == 1 else hashA0[3]


        result_B, hashB0, hashB1 = matrix_B_Creation(result_A, list_of_masks, nodesA[i].inList + nodesA[i].outList, ConfigParserInstance.nodes[i].operation)
        nodesB[i].operation[0] = result_B[0]
        nodesB[i].operation[1] = result_B[1]
        nodesB[i].operation[2] = result_B[2]
        nodesB[i].operation[3] = result_B[3]

        nodesB[i].selfHash = [0] * 4
        nodesB[i].selfHash[0] = hashB1[0] if result_B[0] == 1 else hashB0[0]
        nodesB[i].selfHash[1] = hashB1[1] if result_B[1] == 1 else hashB0[1]
        nodesB[i].selfHash[2] = hashB1[2] if result_B[2] == 1 else hashB0[2]
        nodesB[i].selfHash[3] = hashB1[3] if result_B[3] == 1 else hashB0[3]

        nodesB[i].neiHash = {}
        nodesB[i].neiHash['bit0'] = hashA0
        nodesB[i].neiHash['bit1'] = hashA1

        nodesA[i].neiHash = {}
        nodesA[i].neiHash['bit0'] = hashB0
        nodesA[i].neiHash['bit1'] = hashB1

    inputMasksForA = 0
    inputMasksForB = 0
    for i in range(ConfigParserInstance.AinputBitness):
        inputMasksForA |= list_of_masks[i] << i  # LSB
        inputMasksForB |= list_of_masks[i + ConfigParserInstance.AinputBitness] << i

    out = 0
    for i in range(ConfigParserInstance.resultBitness):
        out |= list_of_masks[ConfigParserInstance.numOfLinks - 1 - i] << i  # LSB

    outputTableForClientA = {}
    outputTableForClientA['config'] = {
        "numOfLinks": str(ConfigParserInstance.numOfLinks),
        "numOfNodes": str(ConfigParserInstance.numOfNodes),
        "masksBitness": str(ConfigParserInstance.AinputBitness),
        "inputMasks": str(inputMasksForA),  # LSB
        "outputMasks": str(out)  # LSB
    }

    outputTableForClientB = {}
    outputTableForClientB['config'] = {
        "numOfLinks": str(ConfigParserInstance.numOfLinks),
        "numOfNodes": str(ConfigParserInstance.numOfNodes),
        "masksBitness": str(ConfigParserInstance.BinputBitness),
        "inputMasks": str(inputMasksForB),  # LSB
        "outputMasks": str(out)  # LSB
    }

    nodesDictFromSimpleNamespaceB = json.loads(json.dumps(nodesB, default=lambda s: vars(s)))
    nodesDictFromSimpleNamespaceA = json.loads(json.dumps(nodesA, default=lambda s: vars(s)))

    for i in reversed(range(ConfigParserInstance.numOfNodes)):
        outputTableForClientA['node' + str(i + 1)] = {}
        outputTableForClientA['node' + str(i + 1)].update(nodesDictFromSimpleNamespaceA.pop())

        outputTableForClientB['node' + str(i + 1)] = {}
        outputTableForClientB['node' + str(i + 1)].update(nodesDictFromSimpleNamespaceB.pop())

    PreprocessorRoutineInst.outputTableForClientA = outputTableForClientA
    PreprocessorRoutineInst.outputTableForClientB = outputTableForClientB

    PreprocessorRoutineInst.ClientATrigger = True

    return [PreprocessorRoutineInst.outputTableForClientA], 200
