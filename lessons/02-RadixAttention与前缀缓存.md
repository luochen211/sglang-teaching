# 02｜RadixAttention 与前缀缓存：先用实验理解

## 直觉

如果许多请求共享同一段长 system prompt，服务端重复做 prefill 会浪费计算和显存带宽。前缀缓存的基本想法是：把已经处理过的 token 前缀保留下来，后续请求从最长的已缓存前缀继续。

本仓库的 `PrefixCache` 是一个 CPU-only 教学模型：它用集合记录每个已插入的前缀，用最长匹配展示“共享前缀越长，新增处理 token 越少”。它不是 SGLang 生产代码，也不模拟 CUDA kernel、调度器或真实显存。

## 运行实验

```bash
PYTHONPATH=src python examples/simulate_prefix_cache.py
```

你应该看到：

- 第一个请求没有命中；
- 第二个请求复用了共同的 system prompt；
- 第三个请求因为在更早位置发生分叉，只复用了更短的前缀；
- 完全不同的请求没有命中。

## 真实服务中的验证思路

用同一组请求，比较启用与禁用 radix cache 的结果。不要只跑一次；要固定 warmup、输入输出长度、并发、请求顺序和随机参数，并保存原始结果。

SGLang 官方 benchmark 文档提供了 `python -m sglang.bench_serving`，支持 TTFT、ITL、端到端延迟、吞吐量和 JSONL 结果输出。可以从下面的骨架开始：

```bash
python -m sglang.bench_serving \
  --backend sglang \
  --host 127.0.0.1 \
  --port 30000 \
  --num-prompts 100 \
  --output-file results.jsonl \
  --output-details
```

参考：[SGLang Bench Serving Guide](https://docs.sglang.ai/developer_guide/bench_serving)。

## 需要警惕的误判

- 第一次请求通常是冷启动，不能和 warm cache 直接比较；
- 更高吞吐量可能伴随更高尾延迟；
- 更高 cache hit rate 不等于端到端一定更快，调度、并发和显存压力也会影响结果；
- 不同模型、tokenizer、硬件和版本之间的数字不能直接横比。

