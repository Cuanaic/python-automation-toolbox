# 更新记录

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-10-14

首个正式版本，四个 CLI 工具全部可用。

### 新增

- `excel_batch` — Excel / CSV 批量合并、拆分、清洗；支持多文件合并、按列拆分、去空行 / 去重 / 去首尾空格
- `data_collect` — 公开数据采集，内置请求限速、失败重试、断点续传
- `report_gen` — CSV 生成单文件 HTML 报表，图表内嵌，零前端依赖
- `file_organizer` — 按类型或日期批量归档文件

### 特性

- 除处理 `.xlsx` 需 `openpyxl` 外，全部仅依赖 Python 标准库
- 所有破坏性操作支持 `--dry-run` 预览，先看结果再动数据
- 附 `samples/make_samples.py`，clone 后可直接生成演示数据跑通完整流程

### 环境

- Python 3.9+
- MIT License
