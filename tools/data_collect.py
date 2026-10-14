#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合规数据采集器：限速 + 自动重试 + 断点续传。

内置示例:
  worldbank   世界银行公开数据（GDP、人口等，官方开放 API，无需 key）
  json        通用 JSON 接口采集（把返回列表展开成 CSV）

设计原则: 只采集公开数据、控制请求频率、失败自动重试、可断点续传。
"""
import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "data-collect-tool/1.0 (demo)"
RATE_SLEEP = 1.0  # 每次请求间隔（秒），礼貌采集


def fetch_json(url, params=None, retries=3, sleep=RATE_SLEEP):
    """GET 一个 JSON 接口，带重试和限速。"""
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            time.sleep(sleep)
            return data
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"  请求失败（第 {i + 1} 次）: {e}")
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"重试 {retries} 次仍失败: {url} ({last})")


class Progress:
    """断点续传：把已完成的页码记到 <输出文件>.progress.json。"""

    def __init__(self, out_path):
        self.path = Path(str(out_path) + ".progress.json")
        self.done = set()
        if self.path.exists():
            try:
                self.done = set(json.load(open(self.path, encoding="utf-8")))
            except Exception:  # noqa: BLE001
                self.done = set()

    def mark(self, page):
        self.done.add(page)
        json.dump(sorted(self.done), open(self.path, "w", encoding="utf-8"))

    def clear(self):
        if self.path.exists():
            self.path.unlink()


def save_csv(path, headers, rows, append=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append and path.exists() else "w"
    with open(path, mode, encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        if mode == "w":
            w.writerow(headers)
        w.writerows(rows)


WORLD_BANK = "https://api.worldbank.org/v2"
# 常用指标代码（可自行替换）:
#   NY.GDP.MKTP.CD = GDP（美元）
#   SP.POP.TOTL    = 总人口
#   EN.ATM.CO2E.PC = 人均碳排放


def cmd_worldbank(args):
    """示例：采集世界银行公开指标。"""
    countries = ";".join(args.countries)
    page, total_pages = 1, 1
    prog = Progress(args.out)
    fetched = 0
    while page <= total_pages:
        if page in prog.done:
            page += 1
            continue
        url = f"{WORLD_BANK}/country/{countries}/indicator/{args.indicator}"
        data = fetch_json(url, {"format": "json", "per_page": 100, "page": page,
                                "date": f"{args.start}:{args.end}"})
        if not isinstance(data, list) or len(data) < 2 or not data[1]:
            print("  没有更多数据")
            break
        meta, records = data[0], data[1]
        total_pages = meta.get("pages", 1)
        rows = [[r["country"]["value"], r["countryiso3code"], r["date"],
                 "" if r["value"] is None else r["value"]] for r in records]
        save_csv(args.out, ["国家", "代码", "年份", "数值"], rows, append=(page > 1))
        fetched += len(rows)
        print(f"  第 {page}/{total_pages} 页 → {len(rows)} 条")
        prog.mark(page)
        page += 1
    prog.clear()
    print(f"完成: 共 {fetched} 条 → {args.out}")


def _flatten(obj, prefix=""):
    """把嵌套 JSON 字典展开成一层字段。"""
    out = {}
    for k, v in obj.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(_flatten(v, f"{key}."))
        elif isinstance(v, list):
            out[key] = json.dumps(v, ensure_ascii=False)
        else:
            out[key] = v
    return out


def cmd_json(args):
    """通用采集：把接口返回的列表（或字典里第一个列表）导出为 CSV。"""
    params = dict(kv.split("=", 1) for kv in args.param)
    data = fetch_json(args.url, params)
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                data = v
                break
    if not isinstance(data, list):
        sys.exit("返回数据不是列表结构，请按实际接口修改本文件中的适配逻辑")
    rows = [_flatten(x) if isinstance(x, dict) else {"value": x} for x in data]
    headers = sorted({k for r in rows for k in r})
    save_csv(args.out, headers, [[r.get(h, "") for h in headers] for r in rows])
    print(f"完成: {len(rows)} 条 → {args.out}")


def main():
    p = argparse.ArgumentParser(description="合规数据采集器")
    sub = p.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("worldbank", help="采集世界银行公开指标（示例，无需 key）")
    w.add_argument("--indicator", default="NY.GDP.MKTP.CD",
                   help="指标代码: GDP=NY.GDP.MKTP.CD, 人口=SP.POP.TOTL")
    w.add_argument("--countries", nargs="+",
                   default=["CHN", "USA", "JPN", "DEU", "IND"])
    w.add_argument("--start", default="2010")
    w.add_argument("--end", default="2024")
    w.add_argument("-o", "--out", default="data/worldbank.csv")
    w.set_defaults(func=cmd_worldbank)

    j = sub.add_parser("json", help="通用 JSON 接口采集")
    j.add_argument("--url", required=True)
    j.add_argument("--param", action="append", default=[], metavar="k=v",
                   help="查询参数，可多次指定")
    j.add_argument("-o", "--out", default="data/api_data.csv")
    j.set_defaults(func=cmd_json)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
