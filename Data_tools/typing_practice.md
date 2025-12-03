# 键盘打字练习工具

一个基于词库的命令行打字练习工具，支持顺序/随机练习和错题重练。

## 词库格式

- 每行一个条目，使用制表符分隔：`<练习内容>\t<解释>`
- 允许以 `#` 开头的注释与空行
- 示例：

```
Advantage\t优势
Loss function\t损失函数
Clip\t剪裁
GAE\t广义优势估计
```

## 使用方法

```bash
python Data_tools/typing_practice.py --data Data_tools/typing_sample.txt --mode random --repeat-wrong
```

主要参数：

- `--data`：词库文件路径，默认为仓库自带的 `Data_tools/typing_sample.txt`
- `--mode`：`ordered`（顺序）或 `random`（随机）
- `--cycles`：练习轮数（不含错题重练）
- `--repeat-wrong`：开启后错题会自动重新加入队列，直到答对

练习结束后会统计题量、正确数、错误数、准确率以及平均耗时。
