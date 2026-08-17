# SGLang 教学实验室

一个以“能运行、能测量、能解释”为标准的 SGLang 学习仓库。

> 目标不是背参数，而是理解：一个 LLM serving 系统如何把请求变成 token 计算，以及如何用可复现实验证明优化是否真的有用。

## 你会学到什么

- 从请求、token、prefill/decode 到 KV cache 的基本链路
- 如何启动 SGLang 的原生 HTTP 服务
- RadixAttention / prefix cache 为什么能减少重复前缀的处理
- TTFT、ITL、端到端延迟、吞吐量和 p99 应该怎么读
- 如何设计一个可复现的 serving benchmark，而不是只截一张“跑得很快”的截图

## 为什么这个仓库先从 CPU 开始

真实 SGLang 服务通常需要 Linux、CUDA GPU、模型权重和正确的版本组合。为了让学习从第一步就能落地，本仓库提供了两个无需 GPU 的教学组件：

1. `PrefixCache`：用最小模型展示共享前缀、最长匹配和 cache hit rate；
2. `metrics.py`：用固定 fixture 演示 TTFT、延迟分位数和输出 token 吞吐量。

它们是机制示意和实验脚手架，不是 SGLang 生产实现，也不提供真实性能承诺。

## 5 分钟运行

```bash
git clone https://github.com/cuidong233/sglang-teaching.git
cd sglang-teaching

PYTHONPATH=src python examples/simulate_prefix_cache.py
PYTHONPATH=src python examples/benchmark_fixture.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

也可以安装为本地包：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python examples/simulate_prefix_cache.py
```

## 课程路线

| 顺序 | 内容 | 可验证产出 |
| --- | --- | --- |
| 00 | 从请求到 token | 能区分 TTFT、ITL、端到端延迟和吞吐量 |
| 01 | 启动真实服务 | 用 `/generate` 发出第一条 SGLang 请求 |
| 02 | RadixAttention 与前缀缓存 | 用实验解释共享前缀为什么能被复用 |
| 03 | 用指标做性能判断 | 产出带环境、参数和原始结果的 benchmark 表 |

## 真实 SGLang 实验

真实服务需要按官方文档安装：

- [SGLang 官方文档](https://docs.sglang.ai/)
- [Serving / launch server 相关文档](https://docs.sglang.ai/basic_usage/quickstart.html)
- [Bench Serving Guide](https://docs.sglang.ai/developer_guide/bench_serving)
- [SGLang 主仓库](https://github.com/sgl-project/sglang)

示例启动命令：

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-0.5B-Instruct \
  --host 127.0.0.1 \
  --port 30000
```

具体安装方式、支持的模型、硬件和参数以官方文档及当前版本为准。

## 仓库结构

```text
.
├── lessons/                 # 分节教程：先理解问题，再做实验
├── examples/                # 可直接运行的 CPU 示例
├── src/sglang_teaching/     # 教学用 cache 与指标实现
├── tests/                   # 不需要 GPU 的回归测试
└── .github/workflows/       # CI：每次提交运行测试
```

## 贡献方式

欢迎补充实验，但请同时提交：

- 实验环境（模型、版本、硬件）；
- 完整命令和原始结果；
- 对结果的解释及已知限制；
- 能在没有 GPU 的情况下运行的最小测试（如果改动了 CPU 教学组件）。

## 许可证与边界

本仓库代码采用 MIT License。SGLang 是独立的开源项目；本仓库不是 SGLang 官方项目，也不代表其维护者。模型权重、硬件驱动和服务参数各有独立许可与要求，请自行确认。
