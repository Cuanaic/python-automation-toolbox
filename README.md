# Python 自动化工具箱

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/deps-stdlib--only-brightgreen.svg)](requirements.txt)

一组开箱即用的 Python 自动化小工具，覆盖日常办公与数据场景。
除 Excel 支持外全部使用 Python 标准库，零重依赖。

四个命令覆盖四类高频重复劳动：**合并表 / 采数据 / 出报表 / 理文件**。

> 想先看产出长什么样：[**在线演示报表**](https://cuanaic.github.io/python-automation-toolbox/demo-report.html) —— 由 `report_gen` 从示例数据直接生成，单文件、无外部依赖。

## 工具一览

| 工具 | 用途 | 快速示例 |
|---|---|---|
| [excel_batch](docs/excel_batch.md) | Excel / CSV 批量合并、拆分、清洗 | `python tools/excel_batch.py merge samples/orders_q1.csv samples/orders_q2.csv -o all.csv` |
| [data_collect](docs/data_collect.md) | 公开数据采集（限速 + 重试 + 断点续传） | `python tools/data_collect.py worldbank -o gdp.csv` |
| [report_gen](docs/report_gen.md) | CSV → 单文件 HTML 报表（内嵌图表） | `python tools/report_gen.py --input all.csv --chart-column 金额` |
| [file_organizer](docs/file_organizer.md) | 文件批量整理（按类型 / 日期归档） | `python tools/file_organizer.py --dir ~/Downloads --dry-run` |

## 快速开始

```bash
git clone https://github.com/Cuanaic/python-automation-toolbox.git
cd python-automation-toolbox
python samples/make_samples.py        # 1. 生成演示数据

# 2. 合并两个季度的订单表
python tools/excel_batch.py merge samples/orders_q1.csv samples/orders_q2.csv -o all.csv

# 3. 生成 HTML 报表（双击 report.html 用浏览器打开）
python tools/report_gen.py --input all.csv --title "订单报表" --chart-column 金额 --label-column 月份

# 4. 数据清洗（去空行、去重复、去首尾空格）
python tools/excel_batch.py clean samples/employees_dirty.csv -o employees_clean.csv
```

## 环境要求

- Python 3.9+
- 可选依赖：`pip install -r requirements.txt`（只有处理 `.xlsx` 时才需要 openpyxl）

## 使用场景

不太需要"大数据"，需要的是一句话把活干完的时候：

- **HR / 行政汇总表**：各部门发来十几个 `.xlsx`，结构一样名字不一样，一条命令合成本月总表
- **运营出周报**：CSV 交给 `report_gen`，出一个自带图表的 HTML 文件，微信里发出去就能看，对方不用装任何东西
- **拿到一堆脏数据**：几千行里混着空行、重复行、首尾带空格的姓名，先 `clean` 再谈分析
- **下载文件夹炸了**：按类型或按日期自动归到子目录，`--dry-run` 先看它想怎么挪
- **要一份公开统计数据**：`data_collect` 带限速、重试和断点续传，中断了接着跑，不会把对方站点打挂

## 为什么不用 pandas

pandas 很强大，但这个仓库瞄准的是另一类场景。

| 场景 | pandas | 本项目 |
|---|---|---|
| 临时在别人的机器上跑 | 先装 numpy + pandas，几十 MB | 拷一个 `.py` 过去就能跑 |
| 只想合并两个 CSV | 要写 DataFrame 代码 | `excel_batch merge a.csv b.csv -o all.csv` |
| 只想出张图给同事看 | 得配 matplotlib，还要处理中文字体 | `report_gen` 直接吐单文件 HTML，图表内嵌 |
| 破坏性操作怕手滑 | 自己要写备份逻辑 | 所有命令都支持 `--dry-run`，先看结果再动数据 |

要跑复杂分析、做特征工程、处理千万行——用 pandas。
只是想把一件重复的事一次干完——用这个。

## 项目定位

本仓库用于展示与承接以下方向的自动化需求：

- 📊 Excel / CSV 批量数据处理
- 🕸️ 公开数据采集（合规、限速、可断点续传）
- 📈 数据报表生成与可视化（单文件 HTML，零依赖）
- 🗂️ 文件批量整理与归档

> 每个工具都支持 `--dry-run` 预览模式，先看结果再动数据。

## 更新记录

见 [CHANGELOG.md](CHANGELOG.md)。当前版本 **v1.0.0**。

## License

MIT © 2026 Cuanaic
