from dataclasses import dataclass
import time
from typing import Any, Optional, Tuple

from eth_typing import HexAddress, HexStr
from web3.contract import Contract
from web3.exceptions import ContractCustomError
from web3.exceptions import ContractPanicError

from tread_contracts.base_contract_client import BaseContractClient, Eip712DomainInfo
from tread_contracts.deployments import CONTRACT_NAME_ATTESTATIONS
from tread_contracts.util import (
    SolidityError,
    bytes32_to_hex,
    decode_custom_error,
    random_uint128,
)


@dataclass
class DataRecord:
    merkle_root: HexStr

@dataclass
class DataRecordWithMetadata(DataRecord):
    cid: str

@dataclass
class RiskRecord:
    value: int

@dataclass
class DataRecordWithAttester(DataRecordWithMetadata):
    attester: HexAddress

@dataclass
class RiskRecordWithAttester(RiskRecord):
    attester: HexAddress


EIP712_DOMAIN = Eip712DomainInfo(
    name="Attestations",
    version="0.6",
)
EIP712_ATTEST_TO_DATA = (
    "AttestToData("
    "bytes32 traderId,"
    "uint256 epoch,"
    "uint256 parameterId,"
    "address attester,"
    "bytes32 merkleRoot,"
    "string cid,"
    "uint256 nonce,"
    "uint256 deadline)"
)
EIP712_ATTEST_TO_RISK = (
    "AttestToRisk("
    "bytes32 traderId,"
    "uint256 epoch,"
    "uint256 parameterId,"
    "address attester,"
    "uint256 value,"
    "uint256 riskGroupId,"
    "uint256 nonce,"
    "uint256 deadline)"
)
EIP_712_SIGNATURE_VALID_FOR_SECONDS = 60 * 60  # 1 hour


class Attestations(BaseContractClient):

    def __init__(
        self, override_contract_address: Optional[HexAddress] = None, **kwargs
    ):
        self._override_contract_address = override_contract_address
        self._epoch_length = None
        self._epoch_zero_start = None
        super(Attestations, self).__init__(**kwargs)

    # ---------- #
    # Properties #
    # ---------- #

    @property
    def contract(self) -> Contract:
        return self.get_contract(
            CONTRACT_NAME_ATTESTATIONS, self._override_contract_address
        )

    # -------------- #
    # Public Methods #
    # -------------- #

    def create_risk_group(
        self,
        members: list[HexAddress],
        threshold: int,
    ) -> int:
        group_params = (int(threshold), members)
        tx_hash = self._call_contract_write(
            "createRiskGroup",
            group_params,
            use_meta_tx=False,
        )
        receipt = self.wait_for_tx_or_throw(tx_hash)
        [event] = self.contract.events.SetGroupParams().process_receipt(receipt)
        group_id = event.args.groupId
        return group_id

    def create_risk_parameter(
        self,
        metadata_name: str,
        metadata_description: str,
    ) -> int:
        risk_parameter = (metadata_name, metadata_description)
        tx_hash = self._call_contract_write(
            "createRiskParameter",
            risk_parameter,
            use_meta_tx=False,
        )
        receipt = self.wait_for_tx_or_throw(tx_hash)
        [event] = self.contract.events.CreatedRiskParameter().process_receipt(receipt)
        parameter_id = event.args.parameterId
        return parameter_id

    def get_default_data_group(self):
        return self._call_contract_read("getDefaultDataGroup")

    def get_data_group_by_trader_id(self, trader_id: bytes):
        return self._call_contract_read("getDataGroupByTraderId", trader_id)

    def get_risk_group(self, group_id: int):
        return self._call_contract_read("getRiskGroup", group_id)

    def get_risk_parameter(self, parameter_id: int):
        return self._call_contract_read("getRiskParameter", parameter_id)

    def get_data_record(self, trader_id: bytes, epoch: int, parameter_id: int) -> Tuple[DataRecord, bool]:
        key = (trader_id, epoch, parameter_id)
        ((merkle_root,), has_consensus) = self._call_contract_read(
            "getDataRecord", key
        )
        return DataRecord(bytes32_to_hex(merkle_root)), has_consensus

    def get_risk_record(
        self, trader_id: bytes, epoch: int, parameter_id: int, group_id: int
    ) -> Tuple[int, bool]:
        key = (trader_id, epoch, parameter_id)
        (risk_value,), has_consensus = self._call_contract_read(
            "getRiskRecord", key, group_id
        )
        return RiskRecord(risk_value), has_consensus

    def attest_to_data(
        self,
        trader_id: bytes,
        epoch: int,
        parameter_id: int,
        merkle_root: bytes,
        cid: str,
        *,
        use_meta_tx: bool = False,
    ) -> HexStr:
        # TODO: Validate and maybe sanitize format of the inputs.
        key = (trader_id, epoch, parameter_id)
        record = (merkle_root, cid)
        if use_meta_tx:
            nonce = random_uint128()
            deadline = int(time.time()) + EIP_712_SIGNATURE_VALID_FOR_SECONDS
            signature = self._eip712_sign(
                EIP712_DOMAIN,
                EIP712_ATTEST_TO_DATA,
                [
                    trader_id,
                    epoch,
                    parameter_id,
                    self.account.address,
                    merkle_root,
                    cid,
                    nonce,
                    deadline,
                ],
            )
            return self._call_contract_write(
                "attestToDataAndTryToRecordConsensusViaSig",
                key,
                self.account.address,
                record,
                signature,
                nonce,
                deadline,
                use_meta_tx=use_meta_tx,
            )

        # Submit attestation and wait for confirmation
        tx_hash = self._call_contract_write(
            "attestToData",
            key,
            self.account.address,
            record,
            use_meta_tx=use_meta_tx,
        )

        return tx_hash

    def attest_to_risk(
        self,
        trader_id: bytes,
        epoch: int,
        parameter_id: int,
        risk_group_id: int,
        risk_value: int,
        *,
        use_meta_tx: bool = False,
    ) -> HexStr:
        # TODO: Validate and maybe sanitize format of the inputs.
        key = (trader_id, epoch, parameter_id)
        record = (risk_value,)
        if use_meta_tx:
            nonce = random_uint128()
            deadline = int(time.time()) + EIP_712_SIGNATURE_VALID_FOR_SECONDS
            signature = self._eip712_sign(
                EIP712_DOMAIN,
                EIP712_ATTEST_TO_RISK,
                [
                    trader_id,
                    epoch,
                    parameter_id,
                    self.account.address,
                    risk_value,
                    risk_group_id,
                    nonce,
                    deadline,
                ],
            )
            return self._call_contract_write(
                "attestToRiskAndTryToRecordConsensusViaSig",
                key,
                self.account.address,
                record,
                risk_group_id,
                signature,
                nonce,
                deadline,
                use_meta_tx=use_meta_tx,
            )

        # Submit attestation and wait for confirmation
        tx_hash = self._call_contract_write(
            "attestToRisk",
            key,
            self.account.address,
            record,
            use_meta_tx=use_meta_tx,
        )

        return tx_hash

    def get_epoch_length(self) -> int:
        # Cache this because it is a constant.
        if self._epoch_length is None:
            self._epoch_length = self.contract.functions.EPOCH_LENGTH().call()
        return self._epoch_length

    def get_epoch_zero_start(self) -> int:
        # Cache this because it is a constant.
        if self._epoch_zero_start is None:
            self._epoch_zero_start = self.contract.functions.EPOCH_ZERO_START().call()
        return self._epoch_zero_start

    def get_epoch_from_timestamp(self, timestamp: int) -> int:
        epoch_zero_start = self.get_epoch_zero_start()
        epoch_length = self.get_epoch_length()
        return (timestamp - epoch_zero_start) // epoch_length

    def get_epoch_start_and_end(self, epoch: int) -> Tuple[int, int]:
        epoch_zero_start = self.get_epoch_zero_start()
        epoch_length = self.get_epoch_length()
        start = epoch_zero_start + epoch * epoch_length
        end = start + epoch_length
        return start, end

    def get_data_record_details(
        self, trader_id: bytes, epoch: int, parameter_id: int
    ) -> list[DataRecordWithAttester]:
        key = (trader_id, epoch, parameter_id)
        attestations = self._call_contract_read("getDataRecordDetails", key)
        return [
            DataRecordWithAttester(
                merkle_root=bytes32_to_hex(attestation[0]),  # merkleRoot
                cid=attestation[1],                          # cid
                attester=attestation[2],                     # attester
            )
            for attestation in attestations
        ]

    def get_risk_record_details(
        self, trader_id: bytes, epoch: int, parameter_id: int, group_id: int
    ) -> list[RiskRecordWithAttester]:
        key = (trader_id, epoch, parameter_id)  # RiskKey struct as tuple
        attestations = self._call_contract_read("getRiskRecordDetails", key, group_id)
        return [
            RiskRecordWithAttester(
                value=attestation[0],      # value
                attester=attestation[1],   # attester
            )
            for attestation in attestations
        ]

    def record_data_consensus(
        self,
        trader_id: bytes,
        epoch: int,
        parameter_id: int,
        *,
        use_meta_tx: bool = False,
    ) -> Optional[HexStr]:
        """
        Record consensus for data attestations if threshold is met.

        Args:
            trader_id: The trader ID
            epoch: The epoch number
            parameter_id: The parameter ID
            use_meta_tx: Whether to use meta-transactions (not implemented)

        Returns:
            The transaction hash if consensus was recorded, None otherwise

        Raises:
            NotImplementedError: If use_meta_tx is True
        """
        if use_meta_tx:
            raise NotImplementedError("Meta-transactions not implemented for record_data_consensus")

        key = (trader_id, epoch, parameter_id)

        # Get threshold from data group
        group_params = self.get_data_group_by_trader_id(trader_id)
        threshold = group_params[0]

        # Get attestations
        attestations = self.get_data_record_details(trader_id, epoch, parameter_id)

        # Count attestations for each merkle root
        merkle_root_counts: dict[HexStr, list[HexAddress]] = {}
        for attestation in attestations:
            attesters = merkle_root_counts.setdefault(attestation.merkle_root, [])
            attesters.append(attestation.attester)

        # Find merkle root with most attestations
        most_attesters = []
        max_count = 0
        for attesters in merkle_root_counts.values():
            attesters = sorted(set(attesters))  # sort and deduplicate, supposed to be unique already
            if len(attesters) > max_count:
                max_count = len(attesters)
                most_attesters = attesters

        # Record consensus if threshold met
        if max_count >= threshold:
            quorum = most_attesters[:threshold]
            consensus_tx = self._call_contract_write(
                "recordConsensusForData",
                key,
                quorum,
                use_meta_tx=False,
            )
            return consensus_tx

        return None

    def record_risk_consensus(
        self,
        trader_id: bytes,
        epoch: int,
        parameter_id: int,
        risk_group_id: int,
        *,
        use_meta_tx: bool = False,
    ) -> Optional[HexStr]:
        """
        Record consensus for risk attestations if threshold is met.

        Args:
            trader_id: The trader ID
            epoch: The epoch number
            parameter_id: The risk parameter ID
            risk_group_id: The risk group ID
            use_meta_tx: Whether to use meta-transactions (not implemented)

        Returns:
            The transaction hash if consensus was recorded, None otherwise

        Raises:
            NotImplementedError: If use_meta_tx is True
        """
        if use_meta_tx:
            raise NotImplementedError("Meta-transactions not implemented for record_risk_consensus")

        key = (trader_id, epoch, parameter_id)

        # Get threshold from risk group
        group_params = self.get_risk_group(risk_group_id)
        threshold = group_params[0]

        # Get attestations
        attestations = self.get_risk_record_details(trader_id, epoch, parameter_id, risk_group_id)

        # Count attestations for each risk value
        risk_value_counts: dict[int, list[HexAddress]] = {}
        for attestation in attestations:
            attesters = risk_value_counts.setdefault(attestation.value, [])
            attesters.append(attestation.attester)

        # Find risk value with most attestations
        most_attesters = []
        max_count = 0
        for attesters in risk_value_counts.values():
            attesters = sorted(set(attesters))  # sort and deduplicate, supposed to be unique already
            if len(attesters) > max_count:
                max_count = len(attesters)
                most_attesters = attesters

        # Record consensus if threshold met
        if max_count >= threshold:
            quorum = most_attesters[:threshold]
            consensus_tx = self._call_contract_write(
                "recordConsensusForRisk",
                key,                # RiskKey struct
                risk_group_id,      # uint256 groupId
                quorum,             # address[] quorum
                use_meta_tx=False,
            )
            return consensus_tx

        return None

    def admin_create_custom_data_group(
        self,
        threshold: int,
        members: list[HexAddress],
        *,
        use_meta_tx: bool = False,
    ) -> int:
        """
        Create a custom data group with specified threshold and members.

        Args:
            threshold: The number of attestations required for consensus
            members: List of addresses that can attest to data
            use_meta_tx: Whether to use meta-transactions

        Returns:
            The ID of the created group
        """
        group_params = (threshold, members)
        tx_hash = self._call_contract_write(
            "adminCreateCustomDataGroup",
            group_params,
            use_meta_tx=use_meta_tx,
        )
        receipt = self.wait_for_tx_or_throw(tx_hash)
        [event] = self.contract.events.SetDataGroupParams().process_receipt(receipt)
        group_id = event.args.groupId
        return group_id

    def admin_map_trader_to_data_group(
        self,
        trader_id: bytes,
        group_id: int,
        *,
        use_meta_tx: bool = False,
    ) -> HexStr:
        """
        Map a trader to a specific data group.

        Args:
            trader_id: The trader ID to map
            group_id: The ID of the data group to map to
            use_meta_tx: Whether to use meta-transactions

        Returns:
            The transaction hash
        """
        tx_hash = self._call_contract_write(
            "adminMapTraderToDataGroup",
            trader_id,
            group_id,
            use_meta_tx=use_meta_tx,
        )
        receipt = self.wait_for_tx_or_throw(tx_hash)
        [event] = self.contract.events.MapTraderToDataGroup().process_receipt(receipt)
        return tx_hash

    def admin_unmap_trader_to_data_group(
        self,
        trader_id: bytes,
        *,
        use_meta_tx: bool = False,
    ) -> HexStr:
        """
        Remove a trader's mapping to a data group.

        Args:
            trader_id: The trader ID to unmap
            use_meta_tx: Whether to use meta-transactions

        Returns:
            The transaction hash
        """
        tx_hash = self._call_contract_write(
            "adminUnmapTraderToDataGroup",
            trader_id,
            use_meta_tx=use_meta_tx,
        )
        receipt = self.wait_for_tx_or_throw(tx_hash)
        return tx_hash

    def admin_update_data_group(
        self,
        group_id: int,
        threshold: int,
        members: list[HexAddress],
        *,
        use_meta_tx: bool = False,
    ) -> HexStr:
        """
        Update the parameters of a data group.

        Args:
            group_id: The ID of the data group to update
            threshold: The new number of attestations required for consensus
            members: The new list of addresses that can attest to data
            use_meta_tx: Whether to use meta-transactions

        Returns:
            The transaction hash
        """
        new_params = (threshold, members)
        tx_hash = self._call_contract_write(
            "adminUpdateDataGroup",
            group_id,
            new_params,
            use_meta_tx=use_meta_tx,
        )
        receipt = self.wait_for_tx_or_throw(tx_hash)
        [event] = self.contract.events.SetDataGroupParams().process_receipt(receipt)
        return tx_hash

    def admin_update_risk_group(
        self,
        group_id: int,
        threshold: int,
        members: list[HexAddress],
        *,
        use_meta_tx: bool = False,
    ) -> HexStr:
        """
        Update the parameters of a risk group.

        Args:
            group_id: The ID of the risk group to update
            threshold: The new number of attestations required for consensus
            members: The new list of addresses that can attest to risk
            use_meta_tx: Whether to use meta-transactions

        Returns:
            The transaction hash
        """
        new_params = (threshold, members)
        tx_hash = self._call_contract_write(
            "adminUpdateRiskGroup",
            group_id,
            new_params,
            use_meta_tx=use_meta_tx,
        )
        receipt = self.wait_for_tx_or_throw(tx_hash)
        [event] = self.contract.events.SetRiskGroupParams().process_receipt(receipt)
        return tx_hash
