# 00｜从一次请求到一组指标

## 先回答一个问题

把模型接到 HTTP 服务上，只能证明“请求能返回”。教学和工程真正要回答的是：

- 首 token 等了多久？
- 后续 token 是否稳定？
- 并发上升时，吞吐量和延迟怎么变化？
- 多个请求重复使用同一段 system prompt 时，有多少输入 token 可以复用？

本课程用一条链路串起来：**请求 → token → prefill/decode → KV cache → 指标 → 判断**。

## 预备知识

- Python 3.10+
- 能读懂基本 HTTP 请求和 Python 类型标注
- 真实 SGLang 实验需要 Linux + CUDA GPU；CPU 先运行本仓库的模拟器

## 先跑不需要 GPU 的实验

```bash
PYTHONPATH=src python3 examples/simulate_prefix_cache.py
PYTHONPATH=src python3 examples/benchmark_fixture.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

这些输出是教学数据，不是 SGLang 在某张 GPU 上的性能承诺。

## 本节产出

读完后，应该能区分：

1. **TTFT**：Time to First Token，首 token 延迟，通常同时受到排队和 prefill 影响。
2. **ITL**：Inter-Token Latency，生成阶段相邻 token 的间隔。
3. **端到端延迟**：一次请求从发出到结束的总时间。
4. **吞吐量**：单位时间完成的请求数或 token 数。

不要只看一个平均值。至少保留 p50 和 p99，并记录请求输入长度、输出长度、并发度、模型、硬件和服务参数。
