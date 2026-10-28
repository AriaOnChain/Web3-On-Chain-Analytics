"""查询已确认的 Sepolia 交易；仅使用 Python 标准库，不连接钱包。"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

RPC_URL = os.environ.get("SEPOLIA_RPC_URL", "https://ethereum-sepolia-rpc.publicnode.com")
TX_HASH = "0x58207214813ef175475186776675de58b065ca62fa323c4a7188a60b877d98f1"


def rpc(method, params):
    print(f"正在查询：{method}", flush=True)
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    request = Request(RPC_URL, data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json",
                               "User-Agent": "Web3-On-Chain-Analytics/1.0",
                               "Accept": "application/json"})
    for attempt in range(3):
        with urlopen(request, timeout=25) as response:
            body = json.load(response)
        if body.get("result") is not None or "error" in body:
            break
        if attempt < 2:
            print("节点未返回记录，稍后重试……", flush=True)
            time.sleep(1)
    if "error" in body:
        error = body["error"]
        message = str(error.get("message", "未提供错误说明"))
        message = message.replace(RPC_URL, "[RPC 地址已隐藏]")
        message = re.sub(r"https?://\S+", "[链接已隐藏]", message)
        message = re.sub(r"[A-Za-z0-9_=-]{24,}", "[长标识已隐藏]", message)
        raise RuntimeError(f"{method}：RPC 错误 {error.get('code')}，{message[:300]}")
    if body.get("result") is None:
        raise RuntimeError(f"{method} 未找到记录，可能尚未确认或节点不提供该历史数据")
    return body["result"]


def main():
    output = Path(__file__).resolve().parents[1] / "data" / "raw" / f"{TX_HASH}.json"
    if "--cached" in sys.argv:
        if not output.exists():
            raise RuntimeError("没有已保存的数据，请先完成一次在线查询")
        saved = json.loads(output.read_text(encoding="utf-8"))
        print("离线读取之前成功查询的记录，本次没有访问节点。")
        print(f"原始查询时间：{saved['retrieved_at_utc']}")
        print(json.dumps(saved["summary"], ensure_ascii=False, indent=2))
        return
    # 先确认节点连接的是 Sepolia，避免在错误网络查询。
    chain_id = int(rpc("eth_chainId", []), 16)
    if chain_id != 11155111:
        raise RuntimeError("节点不是 Sepolia，请检查 SEPOLIA_RPC_URL")

    # 交易提供发送方、接收方和金额；回执提供执行状态及实际 Gas。
    tx = rpc("eth_getTransactionByHash", [TX_HASH])
    receipt = rpc("eth_getTransactionReceipt", [TX_HASH])
    block = rpc("eth_getBlockByHash", [receipt["blockHash"], False])
    if (tx["hash"].lower() != TX_HASH or receipt["transactionHash"].lower() != TX_HASH
            or tx["blockHash"] != receipt["blockHash"]
            or block["hash"] != receipt["blockHash"]):
        raise RuntimeError("交易、回执和区块不一致")

    # RPC 数量字段是十六进制；金额单位为 wei，1 ETH = 10**18 wei。
    value_wei = int(tx["value"], 16)
    gas_used = int(receipt["gasUsed"], 16)
    gas_price = int(receipt["effectiveGasPrice"], 16)
    summary = {
        "network": "Sepolia",
        "transaction_hash": TX_HASH,
        "from": tx["from"],
        "to": tx["to"],
        "value_eth": str(Decimal(value_wei) / Decimal(10**18)),
        "status": "Success" if int(receipt["status"], 16) == 1 else "Failed",
        "timestamp_utc": datetime.fromtimestamp(int(block["timestamp"], 16), timezone.utc).isoformat(),
        "gas_used": gas_used,
        "transaction_fee_eth": str(Decimal(gas_used * gas_price) / Decimal(10**18)),
    }
    output = Path(__file__).resolve().parents[1] / "data" / "raw" / f"{TX_HASH}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "chain_id": chain_id, "transaction": tx, "receipt": receipt,
        "block": block, "summary": summary,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"原始数据已保存：{output}")


if __name__ == "__main__":
    try:
        main()
    except HTTPError as exc:
        print(f"查询未完成：RPC 服务返回 HTTP {exc.code}。"
              "403 表示请求被拒绝，429 表示请求过于频繁。未生成本次结果。", file=sys.stderr)
        sys.exit(1)
    except URLError:
        print("查询未完成：无法连接 RPC，请检查网络、代理和证书配置。", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as exc:
        print(f"查询未完成：{exc}。本次未保存新数据。", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        # 不输出可能带有密钥的自定义 RPC URL。
        print(f"查询未完成（{type(exc).__name__}）。请检查网络和 Sepolia RPC 服务；未生成本次结果。", file=sys.stderr)
        sys.exit(1)
