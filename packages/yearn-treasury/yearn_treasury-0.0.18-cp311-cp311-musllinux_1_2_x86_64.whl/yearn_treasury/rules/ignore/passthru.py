from decimal import Decimal
from typing import Final

from dao_treasury import TreasuryTx, ignore
from y import Network


passthru: Final = ignore("Pass-Thru")

cowswap_router: Final = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
ycrv: Final = "0xFCc5c47bE19d06BF83eB04298b026F81069ff65b"


@passthru("Sent to dinobots to dump", Network.Mainnet)
def is_sent_to_dinoswap(tx: TreasuryTx) -> bool:
    """These tokens are dumpped and the proceeds sent back to the origin strategy."""
    return tx.from_nickname == "Contract: Strategy" and tx.to_nickname == "yMechs Multisig"


@passthru("Bribes for yCRV", Network.Mainnet)
def is_ycrv(tx: TreasuryTx) -> bool:
    """These are routed thru cowswap with dai as the purchase token."""
    yswaps = "0x7d2aB9CA511EBD6F03971Fb417d3492aA82513f0"
    ymechs = "0x2C01B4AD51a67E2d8F02208F54dF9aC4c0B778B6"
    if (tx.from_address == yswaps and tx.symbol == "DAI") or (
        tx.from_address == ymechs and tx.symbol == "3Crv"
    ):
        if tx.to_address == cowswap_router:
            for trade in tx.get_events("Trade"):
                (
                    owner,
                    sell_token,
                    buy_token,
                    sell_amount,
                    buy_amount,
                    fee_amount,
                    order_uid,
                ) = trade.values()
                if (
                    tx.from_address == owner
                    and tx.token == sell_token
                    and buy_token == ycrv
                    and Decimal(sell_amount) / 10**18 == tx.amount
                ):
                    return True

    elif tx.hash in {
        # one off exception case to correct accounting mix-up
        "0x1578f3b0d3158d305167c39dc29ada08914e1ddb67ef9698e1b0421432f9aed6",
        # A few donations from ySwap
        "0xb2e335500b33b42edd8a97f57db35e0561df9a3a811d0cd73dce9767c23da0c4",
        "0xc02aab3a84b3bbfbc18f0ee6aa742f233d97511f653b4a40e7cd8f822851e10a",
        "0x8a2dba62eac44fdfc7ff189016ac601c9da664f5dea42d647f2e552319db2f7d",
        "0xd2c0a137d03811c5e4c27be19c7893f7fdd5851bdd6f825ee7301f3634033035",
    }:
        return True
    return is_dola_bribe(tx)


def is_dola_bribe(tx: TreasuryTx) -> bool:
    return (
        tx.from_nickname == "ySwap Multisig"
        and tx.to_nickname == "Contract: GPv2Settlement"
        and tx.symbol == "DOLA"
    )


passthru("BAL Rewards", Network.Mainnet).match(
    hash="0xf4677cce1a08ecd54272cdc1b23bc64693450f8bb5d6de59b8e58e288ec3b2a7",
    symbol="BAL",
)


@passthru("StrategyAuraUSDClonable", Network.Mainnet)
def is_aura(tx: TreasuryTx) -> bool:
    txhash = tx.hash
    if (
        txhash == "0x1621ba5c9b57930c97cc43d5d6d401ee9c69fed435b0b458ee031544a10bfa75"
        and tx.symbol in ["BAL", "AURA"]
    ):
        return True
    return (
        txhash == "0x996b5911a48319133f50f72904e70ed905c08c81e2c03770e0ccc896be873bd4"
        and tx.symbol == "AURA"
    )


@passthru("yPrisma Strategy Migration", Network.Mainnet)
def is_yprisma_migration(tx: TreasuryTx) -> bool:
    # strategies were changed a few times
    txhash = tx.hash
    if txhash in (
        "0x4c19259ff9e23c2f23653b7560526c2dbd5adef2d53c297b63d8c1fa6f4906f1",
        "0xed39b66c01e25b053117778c80e544c985d962522233b49ce6f7fe136b1a4474",
    ):
        return True
    return (
        txhash == "0x45bb5d7c25393c5bb8ad9647ae60ff39ddc39d695f0e427eb45f91b04f42c636"
        and tx.symbol == "yPRISMA"
    )


@passthru("rKP3R", Network.Mainnet)
def is_rkp3r(tx: TreasuryTx) -> bool:
    if tx.symbol == "rKP3R":
        from_nickname = tx.from_nickname
        to_nickname = tx.to_nickname
        if (
            from_nickname == "Contract: StrategyConvexFixedForexClonable"
            and to_nickname == "Yearn yChad Multisig"
        ):
            return True
        elif (
            from_nickname == "Yearn yChad Multisig"
            and to_nickname == "Contract: StrategyConvexFixedForexClonable"
        ):
            return True
    return False


@passthru("Inverse-earned YearnFed Fees", Network.Mainnet)
def is_inverse_fees_from_yearn_fed(tx: TreasuryTx) -> bool:
    return tx.symbol == "yvDOLA-U" and tx.to_nickname == "Contract: YearnFed"


@passthru("stkAAVE", Network.Mainnet)
def is_stkaave(tx: TreasuryTx) -> bool:
    """stkAAVE is sent from a strategy to ychad, then to sms for unwrapping."""
    if tx.symbol == "stkAAVE":
        from_nickname = tx.from_nickname
        to_nickname = tx.to_nickname
        if "Strategy" in from_nickname and to_nickname == "Yearn yChad Multisig":
            return True
        elif from_nickname == "Yearn yChad Multisig" and to_nickname == "Yearn Strategist Multisig":
            return True
    return False


@passthru("StrategyIdle", Network.Mainnet)
def is_idle(tx: TreasuryTx) -> bool:
    return tx.hash in {
        "0x59595773ee4304ba4e7e06d2c02541781d93867f74c6c83056e7295b684036c7",
        "0x4c7685aa3dfa9f375c612a2773951b9edbe059102b505423ed28a97d2692e75a",
        "0xb17317686b57229aeb7f06103097b47dc2eafa34489c40af70d2ac57bcf8f455",
        "0xfd9e6fd303fdbb358207bf3ba069b7f6a21f82f6b082605056d54948127e81e8",
        "0x41c8428fd361c54bb80cdac752e31622915ac626dd1e9270f02af1dc2c84d1f9",
        "0x9c0d169c7362a7fe436ae852c1aee58a5905d10569abbd50261f65cb0574dc3a",
        "0x55d89a5890cfe80da06f6831fdfa3a366c0ed9cf9b7f1b4d53f5007bb9698fa0",
        "0x6c6fc43dca1841af82b517bc5fc53ea8607e3f95512e4dd3009c0dbb425669f7",
    }
