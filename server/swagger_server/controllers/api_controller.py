import connexion
import six
import operator

from swagger_server.encoder import JSONEncoder
from swagger_server.models.nums import Nums  # noqa: E501
from swagger_server.models.results import Results  # noqa: E501
from swagger_server import util

results = {}
from ..config import *

def get_results():  # noqa: E501
    """Get previous results

    retrieve results # noqa: E501


    :rtype: List[Results]
    """
    try:
        return ServerDictInst.getAll(), 200
    except:
        return [], 404


def operate(body=None):  # noqa: E501
    """operate 2 numbers

    operate 2 numbers with defined action # noqa: E501

    :param body: Nums request body
    :type body: dict | bytes

    :rtype: List[Nums]
    """

    operations = {
        "+": operator.add,
        "*": lambda x, y: x * y,
        "-": operator.sub
    }

    if connexion.request.is_json:
        body = Nums.from_dict(connexion.request.get_json())  # noqa: E501

        num1 = body.num1
        num2 = body.num2

        try:
            result = operations[body.operation](num1, num2)
            input = str(num1) + " " + body.operation + " " + str(num2)

            resultsObject = Results(result, input)
            ServerDictInst.add(resultsObject)
        except:
            return {}, 500
        return resultsObject, 200
    return {}, 400
