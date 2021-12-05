import connexion
import six

from swagger_server.models.table import Table  # noqa: E501
from swagger_server import util


def get_table():  # noqa: E501
    """hello message to get preprocessed data

    Returns preprocessed table for this user, masked input and outputs # noqa: E501


    :rtype: List[Table]
    """
    return 'do some magic!'


def start2_pc(body=None):  # noqa: E501
    """start preprocessing procedure

    send config file to start preprocessing # noqa: E501

    :param body: Nums request body
    :type body: dict | bytes

    :rtype: List[Table]
    """
    if connexion.request.is_json:
        body = Table.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
