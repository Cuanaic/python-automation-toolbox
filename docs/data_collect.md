# data_collect —— 合规数据采集

一个带**限速、自动重试、断点续传**的采集框架。只用于公开数据，请遵守目标站点的 robots 与使用条款。

## 内置示例：世界银行公开数据

世界银行提供官方开放 API（无需注册、无 key），适合演示：

```bash
# 五国 GDP（2010-2024）
python tools/data_collect.py worldbank -o data/gdp.csv

# 换成人口数据
python tools/data_collect.py worldbank --indicator SP.POP.TOTL -o data/population.csv

# 自定义国家与年份
python tools/data_collect.py worldbank --countries CHN USA --start 2000 --end 2024 -o data/two.csv
```

常用指标代码：

| 指标 | 代码 |
|---|---|
| GDP（美元） | `NY.GDP.MKTP.CD` |
| 总人口 | `SP.POP.TOTL` |
| 人均碳排放 | `EN.ATM.CO2E.PC` |

## 通用 JSON 接口

```bash
python tools/data_collect.py json --url "https://api.example.com/items" \
    --param page=1 --param size=100 -o data/items.csv
```

把返回的列表（或字典中第一个列表字段）自动展开成 CSV；嵌套字段用 `a.b` 命名。

## 断点续传

采集中途中断（网络断了 / Ctrl+C）不要紧：重新运行同一命令会跳过已完成的页码。
进度记录在 `<输出文件>.progress.json`，完成后自动删除。

## 适配新目标

`tools/data_collect.py` 中 `cmd_json` 是通用适配器；遇到特殊接口时，复制它写一个新的
`cmd_xxx` 子命令即可（约 30 行）。
