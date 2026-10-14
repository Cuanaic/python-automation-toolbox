# Python 自动化工具箱

一组开箱即用的 Python 自动化小工具，覆盖日常办公与数据场景。
除 Excel 支持外全部使用 Python 标准库，零重依赖。

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

## 项目定位

本仓库用于展示与承接以下方向的自动化需求：

- 📊 Excel / CSV 批量数据处理
- 🕸️ 公开数据采集（合规、限速、可断点续传）
- 📈 数据报表生成与可视化（单文件 HTML，零依赖）
- 🗂️ 文件批量整理与归档

> 每个工具都支持 `--dry-run` 预览模式，先看结果再动数据。

## License

MIT © 2026 Cuanaic
