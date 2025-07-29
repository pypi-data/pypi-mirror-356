from enum import Enum

from nqs_sdk.transaction import ABCTransaction


class CurveProtocol:
    # TODO
    def process_one_transaction(self, transaction: ABCTransaction) -> Enum:
        event = transaction.action_type  # Enum
        return event
