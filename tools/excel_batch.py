#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Excel / CSV 批处理工具 —— 合并、拆分、清洗、预览。

支持格式: .csv / .xlsx（xlsx 需 openpyxl）

示例:
  python tools/excel_batch.py merge a.csv b.csv -o merged.csv
  python tools/excel_batch.py merge ./csvs/ -o all.csv
  python tools/excel_batch.py split all.csv -c 城市 -d split_out
  python tools/excel_batch.py clean dirty.csv -o clean.csv
  python tools/excel_batch.py peek big.csv -n 5
"""
import argparse
import csv
import sys
from pathlib import Path


def _require_openpyxl():
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        sys.exit("处理 .xlsx 需要 openpyxl，请先安装:  pip install openpyxl")


def read_table(path):
    """读取表格，返回 (headers, rows)。"""
    path = Path(path)
    if path.suffix.lower() == ".csv":
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            rows = [r for r in csv.reader(f)]
    elif path.suffix.lower() in (".xlsx", ".xlsm"):
        _require_openpyxl()
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.active
        rows = [["" if c is None else str(c) for c in row]
                for row in ws.iter_rows(values_only=True)]
        wb.close()
    else:
        sys.exit(f"不支持的格式: {path}（只支持 .csv / .xlsx）")
    if not rows:
        return [], []
    return rows[0], rows[1:]


def write_table(path, headers, rows):
    """写出表格（.csv / .xlsx，按扩展名自动判断）。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerows(rows)
    elif path.suffix.lower() in (".xlsx", ".xlsm"):
        _require_openpyxl()
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
        for r in rows:
            ws.append(r)
        wb.save(path)
    else:
        sys.exit(f"不支持的输出格式: {path}（用 .csv 或 .xlsx）")


def collect_inputs(inputs):
    """输入可为文件或目录（目录自动收集其中所有 csv/xlsx）。"""
    files = []
    for x in inputs:
        p = Path(x)
        if p.is_dir():
            files += sorted(p.glob("*.csv")) + sorted(p.glob("*.xlsx"))
        elif p.is_file():
            files.append(p)
        else:
            sys.exit(f"路径不存在: {p}")
    if not files:
        sys.exit("没有找到任何 .csv / .xlsx 文件")
    return files


# ---------------- 子命令 ----------------

def cmd_merge(args):
    """合并多个表格（以第一个文件的表头为基准，缺列补空）。"""
    files = collect_inputs(args.inputs)
    base_headers, base_rows = read_table(files[0])
    all_rows = list(base_rows)
    for fp in files[1:]:
        h, rows = read_table(fp)
        if h != base_headers:
            print(f"  提示: {Path(fp).name} 表头与基准不一致，已按列名对齐")
            idx = {name: i for i, name in enumerate(h)}
            all_rows += [[row[idx[name]] if name in idx and idx[name] < len(row) else ""
                          for name in base_headers] for row in rows]
        else:
            all_rows += rows
    write_table(args.output, base_headers, all_rows)
    print(f"合并 {len(files)} 个文件 → {args.output}（共 {len(all_rows)} 行）")


def cmd_split(args):
    """按某列的值拆分成多个文件。"""
    headers, rows = read_table(args.input)
    if args.column not in headers:
        sys.exit(f"列不存在: {args.column}（现有列: {', '.join(headers)}）")
    ci = headers.index(args.column)
    groups = {}
    for row in rows:
        key = row[ci] if ci < len(row) else ""
        groups.setdefault(key, []).append(row)
    outdir = Path(args.outdir)
    for key, grows in groups.items():
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in key) or "empty"
        out = outdir / f"{safe}{Path(args.input).suffix}"
        write_table(out, headers, grows)
        print(f"  {key or '(空值)'} → {out}（{len(grows)} 行）")
    print(f"共拆出 {len(groups)} 个文件 → {outdir}/")


def _clean_row(row):
    return [c.strip() if isinstance(c, str) else c for c in row]


def cmd_clean(args):
    """清洗：去空行、去重复行（含混入的重复表头）、去单元格首尾空白。"""
    headers, rows = read_table(args.input)
    headers = _clean_row(headers)
    seen = set()
    cleaned = []
    dropped = 0
    for row in rows:
        row = _clean_row(row)
        if not any(str(c).strip() for c in row):
            dropped += 1
            continue
        if row == headers:
            dropped += 1
            continue
        key = tuple(row)
        if args.unique and key in seen:
            dropped += 1
            continue
        seen.add(key)
        cleaned.append(row)
    write_table(args.output, headers, cleaned)
    print(f"清洗完成: {len(rows)} 行 → {len(cleaned)} 行（去掉 {dropped} 行）→ {args.output}")


def cmd_peek(args):
    """预览表格前几行。"""
    headers, rows = read_table(args.input)
    print(" | ".join(map(str, headers)))
    print("-" * 60)
    for row in rows[:args.lines]:
        print(" | ".join(map(str, row)))
    print(f"... 共 {len(rows)} 行")


def main():
    p = argparse.ArgumentParser(description="Excel / CSV 批处理工具")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("merge", help="合并多个表格文件")
    m.add_argument("inputs", nargs="+", help="文件或目录（可多个）")
    m.add_argument("-o", "--output", default="merged.csv", help="输出文件")
    m.set_defaults(func=cmd_merge)

    s = sub.add_parser("split", help="按某列的值拆分")
    s.add_argument("input")
    s.add_argument("-c", "--column", required=True, help="用来拆分的列名")
    s.add_argument("-d", "--outdir", default="split_out", help="输出目录")
    s.set_defaults(func=cmd_split)

    c = sub.add_parser("clean", help="清洗（去空行 / 去重复 / 去空格）")
    c.add_argument("input")
    c.add_argument("-o", "--output", required=True)
    c.add_argument("--keep-duplicates", dest="unique", action="store_false",
                   help="保留重复行（默认去重）")
    c.set_defaults(func=cmd_clean, unique=True)

    k = sub.add_parser("peek", help="预览前几行")
    k.add_argument("input")
    k.add_argument("-n", "--lines", type=int, default=10)
    k.set_defaults(func=cmd_peek)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
