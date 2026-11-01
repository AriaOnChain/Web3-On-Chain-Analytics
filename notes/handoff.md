# 新对话教学接续

更新日期：2026-10-29。

## 学生与节奏

会 Excel、SQL、Python，使用过 MetaMask 测试网。目标是链上分析师。
坚持中文、一步一步：一个小知识点或操作，等用户回答后再推进。不要重复完整基础课程，不要一次生成大项目。

## 已有证据的学习成果

- 已核验 Sepolia 原生转账的金额、Gas、状态及时间，见 00-native-transfer.md。
- 已理解交易 To 是被调用合约、事件 to 是代币接收方，value=0 ETH 不代表没有代币转移。
- LINK input 与 Transfer 事件的地址及数量已核对，见 02-link-transfer.md。
- 已理解日志 Address、Topic 0/1/2、Data，地址取末尾 40 个十六进制字符。
- 用户成功运行 scripts/decode_transfer_log.py，输出 250 LINK。这是按核对字段重建的离线教学样本，不是此次下载的完整回执。
- 用户正确回答 decimals=6、原始数量 250000000 对应 250。
- 用户正确回答一笔交易含三条 Transfer 时，交易数 1、转账事件数 3；仅按交易哈希去重会剩一条。

## 精确停留位置

刚讲过事件标识使用 chain_id + transaction_hash + log_index。尚未开始多条事件表格或 SQL 统计。

新聊天建议从这里开始：用一个明确标为虚构的三行教学表说明这三个字段如何区分事件，先让用户理解 log_index，无需再重复问交易数与事件数。随后逐步练习 COUNT(*) 与 COUNT(DISTINCT transaction_hash)，前提是单链、已筛选 Transfer 且事件去重完成。按步骤等待用户回答。

## 数据与未解决事项

- 原生转账：0x58207214813ef175475186776675de58b065ca62fa323c4a7188a60b877d98f1。
- LINK 转账：0x4ad3936bb034989eaa504cfbf586d24737ea50ffb2ac8e4a81bafb1f2ef051c3。
- scripts/fetch_transaction.py 曾成功保存原生转账 JSON，之后公共节点回执返回 null，重试未解决；--cached 可离线读取，用户已成功执行。
- LINK 完整 RPC 回执尚未取得，decimals=18 目前为教学配置，不能声称已经程序查询合约。
- 不编造真实 log_index、多条事件或在线查询结果。虚构样本须明确标识。
- 尚未进行 Dune 查询或 Uniswap 实战，不能勾选完成。

## 文件入口

教学规则：AGENTS.md；总进度：notes/progress.md；单条解析：scripts/decode_transfer_log.py。
