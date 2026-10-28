# 分析脚本

保存 API 取数、清洗和核验脚本。后续按实际需要添加依赖与运行说明。

## 第一个练习：查询 Sepolia 转账

在项目根目录运行（Python 3，仅标准库）：

```powershell
python scripts/fetch_transaction.py
```

脚本依次查询链 ID、交易、交易回执和区块，输出金额、状态、时间和执行手续费。
结果保存在 data/raw/，不纳入 Git。不需要钱包或私钥。
默认使用公共节点；如不可用，可通过环境变量 SEPOLIA_RPC_URL 指定自己的 Sepolia RPC 地址。不要将带密钥的地址写进代码或提交到仓库。

方法说明：https://ethereum.org/developers/docs/apis/json-rpc/

后续复测发现公共节点可能返回空回执；脚本现会显示具体步骤并对空结果尝试最多三次。若仍失败，可以用 `python scripts/fetch_transaction.py --cached` 读取此前成功保存的数据（显示原始查询时间，不进行在线查询）。没有缓存时会明确报错。

验证状态：2026-10-27 在线运行成功。初次 HTTP 403（1010）在补充 User-Agent 和 Accept 请求头后解决。返回的 0.1 ETH、Success、2024-11-04T19:38:24+00:00 和 0.000194337489192 ETH 手续费与浏览器记录一致；gas_used 为 21000。
