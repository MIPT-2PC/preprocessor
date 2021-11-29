import connexion
import six

from swagger_server.models.nums import Nums  # noqa: E501
from swagger_server.models.results import Results  # noqa: E501
from swagger_server import util


def do_action(body):  # noqa: E501
    """operate 2 numbers

     # noqa: E501

    :param body: 2 numbers to operate with
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Nums.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_results():  # noqa: E501
    """Get previous results

    Multiple status values can be provided with comma separated strings # noqa: E501


    :rtype: List[Results]
    """
    return 'do some magic!'
