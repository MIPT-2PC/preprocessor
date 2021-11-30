import connexion
import six

from swagger_server.models.nums import Nums  # noqa: E501
from swagger_server.models.results import Results  # noqa: E501
from swagger_server import util


def get_results():  # noqa: E501
    """Get previous results

    retrieve results # noqa: E501


    :rtype: List[Results]
    """
    return 'do some magic!'


def operate(body=None):  # noqa: E501
    """operate 2 numbers

    operate 2 numbers with defined action # noqa: E501

    :param body: Nums request body
    :type body: dict | bytes

    :rtype: List[Results]
    """
    if connexion.request.is_json:
        body = Nums.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
