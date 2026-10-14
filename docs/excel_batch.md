# excel_batch —— Excel / CSV 批处理

批量合并、拆分、清洗表格文件。支持 `.csv` 与 `.xlsx`（xlsx 需 `pip install openpyxl`）。

## 命令

### 合并多个文件

```bash
# 合并指定的多个文件
python tools/excel_batch.py merge samples/orders_q1.csv samples/orders_q2.csv -o all.csv

# 合并整个目录里的所有表格
python tools/excel_batch.py merge ./csvs/ -o all.csv
```

表头不一致时会自动按列名对齐，缺列补空。

### 按某列拆分

```bash
python tools/excel_batch.py split all.csv -c 城市 -d split_out
```

每个城市一个文件，输出到 `split_out/`。

### 清洗脏数据

```bash
python tools/excel_batch.py clean samples/employees_dirty.csv -o employees_clean.csv
```

- 删除空行
- 删除重复行（含混在数据中的重复表头）
- 去除单元格首尾空白

加 `--keep-duplicates` 可保留重复行（只做空格清理）。

### 快速预览

```bash
python tools/excel_batch.py peek all.csv -n 5
```

## 输出编码说明

CSV 一律用 `utf-8-sig` 读写，Excel / WPS 直接双击打开不乱码。
