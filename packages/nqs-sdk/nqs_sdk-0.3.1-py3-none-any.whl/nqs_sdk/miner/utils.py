import logging
from collections.abc import Iterator
from typing import Tuple

import numpy as np
from micro_language import Condition

from nqs_sdk.agent import AgentAction
from nqs_sdk.transaction import ABCTransaction


def deduplicate_time_series(timestamps: np.ndarray, values: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # keep unique timestamps
    timestamps_unique, _ = np.unique(timestamps, return_index=True)
    last_index = np.searchsorted(timestamps, timestamps_unique, side="right") - 1
    values_unique = values[last_index]
    return timestamps_unique, values_unique


# linked list
class Node:
    def __init__(self, txn: ABCTransaction | AgentAction):
        self._block_number = txn.block_number
        self._txn = txn
        self.next: Node | None = None

    def get_block_number(self) -> int:
        return self._block_number

    def get_txn(self) -> tuple[ABCTransaction, Condition | None, bool]:
        """
        Returns the transaction object, the condition and a boolean for the agent
        """
        if isinstance(self._txn, ABCTransaction):
            return self._txn, None, False
        elif isinstance(self._txn, AgentAction):
            return self._txn.transactions[0], self._txn.condition, True


class TransactionsLinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None

    def insert(self, txn: ABCTransaction | AgentAction) -> None:
        block_number: int = txn.block_number
        new_node = Node(txn)

        if not self.head or block_number < self.head.get_block_number():
            new_node.next = self.head
            self.head = new_node
            return

        current: Node = self.head
        while current.next and current.next.get_block_number() <= block_number:
            current = current.next

        new_node.next = current.next
        current.next = new_node

    def display(self) -> None:
        current: Node | None = self.head
        while current:
            logging.debug(f"blockNumber: {current.get_block_number()}, Data: {current._txn}")
            current = current.next

    def iterate(self) -> Iterator[Node]:
        current: Node | None = self.head
        while current:
            yield current
            current = current.next


# if __name__ == "__main__":
#     # Make an out-of-order policy and create the linked list
#     agent_policy = [
#         AgentAction(
#             transactions=[
#                 SwapTransactionCurve(
#                     protocol_id="curve_tripool",
#                     block_number=10,
#                     sender_wallet=None,
#                     token_to_sell="USDT",
#                     token_to_buy="DAI",
#                     amount_sold=10000000,
#                 )
#             ],
#         ),
#         AgentAction(
#             transactions=[
#                 MintTransactionCurve(
#                     protocol_id="curve_tripool",
#                     block_number=9,
#                     sender_wallet=None,
#                     balances_to_deposit={
#                         "DAI": 10000000000000000000,
#                         "USDC": 10000000,
#                         "USDT": 10000000,
#                     },
#                 )
#             ],
#         ),
#         AgentAction(
#             transactions=[
#                 BurnTransactionCurve(
#                     protocol_id="curve_tripool",
#                     block_number=8,
#                     sender_wallet=None,
#                     lp_tokens_to_burn=15000000000000000000,
#                 )
#             ],
#         ),
#         AgentAction(
#             transactions=[
#                 BurnImbalanceTransactionCurve(
#                     protocol_id="curve_tripool",
#                     block_number=7,
#                     sender_wallet=None,
#                     balances_to_withdraw={
#                         "DAI": 4000000000000000000,
#                         "USDC": 4000000,
#                         "USDT": 4000000,
#                     },
#                 )
#             ],
#         ),
#         AgentAction(
#             transactions=[
#                 BurnOneTransactionCurve(
#                     protocol_id="curve_tripool",
#                     block_number=6,
#                     sender_wallet=None,
#                     token_to_withdraw="USDC",
#                     lp_tokens_to_burn=2000000000000000000,
#                 )
#             ],
#         ),
#     ]

#     # Example usage:
#     this_linked_list = TransactionsLinkedList()

#     for agent_action in agent_policy:
#         this_linked_list.insert(agent_action)

#     # display the linked list
#     this_linked_list.display()
