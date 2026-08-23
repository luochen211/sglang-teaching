# 01｜启动一个真实的 SGLang 服务

本节把 CPU 模拟推进到真实服务。命令参数以 [SGLang 官方文档](https://docs.sglang.io/) 为准；SGLang 和模型版本会变化，执行前请重新查看官方安装说明。

## 安装

在有兼容 CUDA 环境的 Linux 机器上，按官方文档安装 SGLang。不要把本地 macOS CPU 运行结果当作真实服务验证。

## 启动服务

下面是一个教学用的小模型示例。模型权重需要从 Hugging Face 下载，显存、网络和模型支持情况需要自行确认：

```bash
python3 -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-0.5B-Instruct \
  --host 127.0.0.1 \
  --port 30000
```

## 发出原生请求

```bash
curl http://127.0.0.1:30000/generate \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "用三句话解释 KV cache，并给出一个适合初学者的类比。",
    "sampling_params": {"temperature": 0.2, "max_new_tokens": 128}
  }'
```

## 验收清单

- 服务进程启动，没有 OOM 或模型加载错误
- `/generate` 返回可解析的 JSON
- 固定 prompt 和 sampling 参数后，结果可被记录和复现
- 记录模型、GPU、SGLang 版本、启动参数和请求参数

“返回 200”只是第一道门。下一节开始测量复用和性能。
