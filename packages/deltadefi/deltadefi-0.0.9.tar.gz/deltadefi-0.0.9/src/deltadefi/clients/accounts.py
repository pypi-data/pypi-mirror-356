#
from typing import List

from sidan_gin import Asset, UTxO

from deltadefi.api import API
from deltadefi.lib.utils import check_required_parameter, check_required_parameters
from deltadefi.responses import (
    BuildDepositTransactionResponse,
    BuildWithdrawalTransactionResponse,
    CreateNewAPIKeyResponse,
    GetAccountBalanceResponse,
    GetDepositRecordsResponse,
    GetOrderRecordResponse,
    GetWithdrawalRecordsResponse,
    SubmitDepositTransactionResponse,
    SubmitWithdrawalTransactionResponse,
)
from deltadefi.responses.accounts import GetOperationKeyResponse


class Accounts(API):
    """
    Accounts client for interacting with the DeltaDeFi API.
    """

    group_url_path = "/accounts"

    def __init__(self, api_key=None, base_url=None, **kwargs):
        super().__init__(api_key=api_key, base_url=base_url, **kwargs)

    def get_operation_key(self, **kwargs) -> GetOperationKeyResponse:
        """
        Get the encrypted operation key.

        Returns:
            A GetOperationKeyResponse object containing the encrypted operation key and its hash.
        """

        url_path = "/operation-key"
        return self.send_request("GET", self.group_url_path + url_path, kwargs)

    def create_new_api_key(self, **kwargs) -> CreateNewAPIKeyResponse:
        """
        Create a new API key.

        Returns:
            A CreateNewAPIKeyResponse object containing the new API key.
        """

        url_path = "/new-api-key"
        return self.send_request("GET", self.group_url_path + url_path, kwargs)

    def get_deposit_records(self, **kwargs) -> GetDepositRecordsResponse:
        """
        Get deposit records.

        Returns:
            A GetDepositRecordsResponse object containing the deposit records.
        """
        url_path = "/deposit-records"
        return self.send_request("GET", self.group_url_path + url_path, kwargs)

    def get_withdrawal_records(self, **kwargs) -> GetWithdrawalRecordsResponse:
        """
        Get withdrawal records.

        Returns:
            A GetWithdrawalRecordsResponse object containing the withdrawal records.
        """
        url_path = "/withdrawal-records"
        return self.send_request("GET", self.group_url_path + url_path, kwargs)

    def get_order_records(self, **kwargs) -> GetOrderRecordResponse:
        """
        Get order records.

        Returns:
            A GetOrderRecordResponse object containing the order records.
        """
        url_path = "/order-records"
        return self.send_request("GET", self.group_url_path + url_path, kwargs)

    def get_account_balance(self, **kwargs) -> GetAccountBalanceResponse:
        """
        Get account balance.

        Returns:
            A GetAccountBalanceResponse object containing the account balance.
        """
        url_path = "/balance"
        return self.send_request("GET", self.group_url_path + url_path, kwargs)

    def build_deposit_transaction(
        self, deposit_amount: List[Asset], input_utxos: List[UTxO], **kwargs
    ) -> BuildDepositTransactionResponse:
        """
        Build a deposit transaction.

        Args:
            data: A BuildDepositTransactionRequest object containing the deposit transaction details.

        Returns:
            A BuildDepositTransactionResponse object containing the built deposit transaction.
        """

        check_required_parameters(
            [[deposit_amount, "deposit_amount"], [input_utxos, "input_utxos"]]
        )
        payload = {
            "deposit_amount": deposit_amount,
            "input_utxos": input_utxos,
            **kwargs,
        }

        url_path = "/deposit/build"
        return self.send_request("POST", self.group_url_path + url_path, payload)

    def build_withdrawal_transaction(
        self, withdrawal_amount: List[Asset], **kwargs
    ) -> BuildWithdrawalTransactionResponse:
        """
        Build a withdrawal transaction.

        Args:
            data: A BuildWithdrawalTransactionRequest object containing the withdrawal transaction details.

        Returns:
            A BuildWithdrawalTransactionResponse object containing the built withdrawal transaction.
        """

        check_required_parameter(withdrawal_amount, "withdrawal_amount")
        payload = {"withdrawal_amount": withdrawal_amount, **kwargs}

        url_path = "/withdrawal/build"
        return self.send_request("POST", self.group_url_path + url_path, payload)

    def submit_deposit_transaction(
        self, signed_tx: str, **kwargs
    ) -> SubmitDepositTransactionResponse:
        """
        Submit a deposit transaction.

        Args:
            data: A SubmitDepositTransactionRequest object containing the deposit transaction details.

        Returns:
            A SubmitDepositTransactionResponse object containing the submitted deposit transaction.
        """

        check_required_parameter(signed_tx, "signed_tx")
        payload = {"signed_tx": signed_tx, **kwargs}

        url_path = "/deposit/submit"
        return self.send_request("POST", self.group_url_path + url_path, payload)

    def submit_withdrawal_transaction(
        self, signed_tx: str, **kwargs
    ) -> SubmitWithdrawalTransactionResponse:
        """
        Submit a withdrawal transaction.

        Args:
            data: A SubmitWithdrawalTransactionRequest object containing the withdrawal transaction details.

        Returns:
            A SubmitWithdrawalTransactionResponse object containing the submitted withdrawal transaction.
        """

        check_required_parameter(signed_tx, "signed_tx")
        payload = {"signed_tx": signed_tx, **kwargs}

        url_path = "/withdrawal/submit"
        return self.send_request("POST", self.group_url_path + url_path, payload)
