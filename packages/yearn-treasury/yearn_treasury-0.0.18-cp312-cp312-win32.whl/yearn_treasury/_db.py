# mypy: disable-error-code="arg-type"
from dao_treasury.db import Address
from y import Network
from y.constants import CHAINID

from yearn_treasury import constants


def prepare_db() -> None:
    chad = {Network.Mainnet: "y", Network.Fantom: "f"}[CHAINID]  # type: ignore [index]

    labels = {
        constants.TREASURY_MULTISIG: "Yearn Treasury",
        constants.YCHAD_MULTISIG: f"Yearn {chad}Chad Multisig",
        # constants.STRATEGIST_MULTISIG: "Yearn Strategist Multisig",
        # This wallet is an EOA that has been used to assist in bridging tokens across chains.
        "0x5FcdC32DfC361a32e9d5AB9A384b890C62D0b8AC": "Bridge Assistooor EOA",
    }

    Address.set_nicknames(labels)
