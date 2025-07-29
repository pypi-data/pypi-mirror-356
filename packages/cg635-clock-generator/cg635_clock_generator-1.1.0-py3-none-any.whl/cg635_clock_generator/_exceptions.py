"""
Exceptions for the CG635 clock generator.
"""

__author__ = "Leandro Lanzieri"
__copyright__ = "Deutsches Elektronen-Synchrotron, DESY"
__license__ = "LGPL-3.0"


class CG635OperationTimeoutError(Exception):
    """Raised when a command to the CG635 times out."""

    pass


class CG635CommunicationError(Exception):
    """Raised when there is a communication error with the CG635."""

    pass


class CG635CommandError(Exception):
    """Raised when there is an error in a command to the CG635."""

    pass
