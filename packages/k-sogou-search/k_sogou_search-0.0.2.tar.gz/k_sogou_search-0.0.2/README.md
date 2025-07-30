# Sogou Search API

一个非官方的Python API，用于从搜狗获取搜索结果。

## 安装

```bash
pip install k-sogou-search
```

## 使用

```python
from sogou_search import sogou_search

results = sogou_search('人工智能', num_results=15)
for result in results:
    print(result)
```
