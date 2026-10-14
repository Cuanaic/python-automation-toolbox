#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成演示用示例数据。运行: python samples/make_samples.py"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).parent
random.seed(42)

CITIES = ["北京", "上海", "广州", "深圳", "杭州"]
PRODUCTS = ["标准版", "专业版", "旗舰版"]


def make_orders(path, months):
    rows = []
    for m in months:
        for _ in range(28):
            rows.append([
                f"2024-{m:02d}",
                random.choice(PRODUCTS),
                random.choice(CITIES),
                random.randint(1, 20),
                round(random.uniform(99, 9999), 2),
            ])
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["月份", "产品", "城市", "数量", "金额"])
        w.writerows(rows)
    print("已生成", path, f"({len(rows)} 行)")


def make_employees(path):
    """故意留脏数据（空行、重复行、首尾空格），用于演示 clean 子命令。"""
    rows = [
        ["张伟", "研发部", "18000", "2021-03-01"],
        ["李娜", "市场部", "15000", "2022-07-15"],
        ["王强", "研发部", "22000", "2019-11-20"],
        ["", "", "", ""],
        ["张伟", "研发部", "18000", "2021-03-01"],  # 重复行
        ["赵敏", "财务部", " 13500 ", "2023-02-08"],  # 带空格
    ]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["姓名", "部门", "月薪", "入职日期"])
        w.writerows(rows)
    print("已生成", path, "（含脏数据，用于演示清洗）")


if __name__ == "__main__":
    make_orders(HERE / "orders_q1.csv", [1, 2, 3])
    make_orders(HERE / "orders_q2.csv", [4, 5, 6])
    make_employees(HERE / "employees_dirty.csv")
