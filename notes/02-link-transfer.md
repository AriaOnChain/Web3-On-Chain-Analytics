# Sepolia LINK 转账：浏览器核验

核验日期：2026-10-29。
来源：https://sepolia.etherscan.io/tx/0x4ad3936bb034989eaa504cfbf586d24737ea50ffb2ac8e4a81bafb1f2ef051c3

范围：浏览器详情及用户逐项核对的解码 input、Transfer 事件。尚未为此交易编写或运行 RPC 日志解析。

## 交易概要

- 链：Sepolia；时间：2024-11-04 19:38:24 UTC。
- 状态：Success；顶层 value：0 ETH。
- 发送方：0x4281eCF07378Ee595C564a59048801330f3084eE。
- 顶层 To（LINK 合约）：0x779877A7B0D9E8603169DdbD7836e478b4624789。
- 代币接收地址：0x10FC64f63B3E9C23c9b2912C2B6F1A3A7637DF59。
- 浏览器显示转入 250 测试 LINK。

## 已完成的对应检查

- 用户读取函数选择器 0xa9059cbb，对应本例 transfer(address,uint256)。
- input 接收参数与钱包地址一致。
- input 数量参数为 250000000000000000000。
- 用户确认事件名称为 Transfer。
- 用户确认事件 to 与钱包地址一致。
- 用户确认事件 value 与 input 数量相同。
- 原始数量 / 10^18 = 250，与浏览器显示一致。后续程序取数时应独立查询合约 decimals，不可对所有代币默认使用 18。

结论：本次成功的合约调用中，转账请求和 Transfer 事件的接收地址、数量一致；顶层 0 ETH 不代表没有代币转移。

下一步：取得并解码这笔交易的原始回执，理解日志 address、topics 和 data。
