"""离线解析 ERC-20 Transfer 教学样本，仅使用标准库。

样本由浏览器核对的地址、用户提供的 Data 重建；不是新下载的 RPC 回执。
事件结构依据 https://eips.ethereum.org/EIPS/eip-20#transfer-1 。
"""

import json
import re
from decimal import Decimal, localcontext

TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
LINK_CONTRACT = "0x779877a7b0d9e8603169ddbd7836e478b4624789"


def address_topic(address):
    """教学用：将已核对的地址补齐为 32 字节 Topic。"""
    return "0x" + address[2:].lower().zfill(64)


SAMPLE_LOG = {
    "address": LINK_CONTRACT,
    "topics": [
        TRANSFER_TOPIC,
        address_topic("0x4281ecf07378ee595c564a59048801330f3084ee"),
        address_topic("0x10fc64f63b3e9c23c9b2912c2b6f1a3a7637df59"),
    ],
    "data": "0x00000000000000000000000000000000000000000000000d8d726b7177a80000",
}


def decode_transfer(log, decimals):
    """解析已知 ERC-20 合约的标准 Transfer；不判断交易是否成功。"""
    topics = log["topics"]
    if len(topics) != 3 or topics[0].lower() != TRANSFER_TOPIC:
        raise ValueError("不是本脚本支持的标准 ERC-20 Transfer 日志")
    if not re.fullmatch(r"0x[0-9a-fA-F]{40}", log["address"]):
        raise ValueError("日志合约地址格式不正确")
    if type(decimals) is not int or not 0 <= decimals <= 255:
        raise ValueError("decimals 必须为 0–255 的整数")
    for topic in topics[1:]:
        if not re.fullmatch(r"0x0{24}[0-9a-fA-F]{40}", topic):
            raise ValueError("地址 Topic 应为前补零的 32 字节数据")
    if not re.fullmatch(r"0x[0-9a-fA-F]{64}", log["data"]):
        raise ValueError("数量 Data 应为 32 字节")

    # 地址占 20 字节，即最后 40 个十六进制字符。
    sender = "0x" + topics[1][-40:].lower()
    recipient = "0x" + topics[2][-40:].lower()
    raw_amount = int(log["data"], 16)
    with localcontext() as context:
        context.prec = 100  # 足以精确表示 uint256 数量。
        amount = format(Decimal(raw_amount) / Decimal(10**decimals), "f")
    return {
        "token_contract": log["address"].lower(),
        "from": sender,
        "to": recipient,
        "raw_amount": str(raw_amount),
        "decimals": decimals,
        "amount": amount,
    }


if __name__ == "__main__":
    print("离线教学样本：根据已核对字段重建；本次未请求节点。")
    print("18 是本例 LINK 的教学配置，其他代币需独立核验 decimals。")
    print(json.dumps(decode_transfer(SAMPLE_LOG, decimals=18), ensure_ascii=False, indent=2))
