#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CSV → 单文件 HTML 报表生成器（零依赖，内嵌 SVG 柱状图）。

示例:
  python tools/report_gen.py --input all.csv --title "订单报表" \
      --chart-column 金额 --label-column 月份
输出一个自包含 report.html，双击用浏览器打开即可查看/打印/发送。
"""
import argparse
import csv
import html
import statistics
from datetime import datetime
from pathlib import Path


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.reader(f)]
    if not rows:
        raise SystemExit("CSV 文件为空")
    return rows[0], rows[1:]


def to_number(x):
    try:
        return float(str(x).replace(",", "").replace("%", ""))
    except (ValueError, AttributeError):
        return None


def svg_bar_chart(labels, values, width=760, height=340, title=""):
    """手绘 SVG 柱状图，不依赖任何 JS 库。"""
    n = len(labels)
    if n == 0:
        return ""
    pad_l, pad_r, pad_t, pad_b = 66, 20, 44, 84
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    vmax = max(values) or 1
    bar_w = plot_w / n
    parts = [
        f'<text x="{width / 2}" y="24" font-size="15" text-anchor="middle" fill="#222">'
        f'{html.escape(title)}</text>',
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" '
        f'y2="{pad_t + plot_h}" stroke="#999"/>',
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#999"/>',
    ]
    # 简化 x 轴：最多显示 40 根柱子（取前 40 条）
    for i, (lab, v) in enumerate(zip(labels, values)):
        if i >= 40:
            break
        h = (v / vmax) * plot_h
        x = pad_l + i * bar_w + bar_w * 0.15
        y = pad_t + plot_h - h
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w * 0.7:.1f}" height="{max(h, 1):.1f}" '
            f'fill="#4f7cff" rx="3"><title>{html.escape(str(lab))}: {v:,.0f}</title></rect>')
        if n <= 20:
            parts.append(f'<text x="{x + bar_w * 0.35:.1f}" y="{y - 6:.1f}" '
                         f'font-size="11" text-anchor="middle" fill="#333">{v:,.0f}</text>')
        t = str(lab)
        if len(t) > 8:
            t = t[:7] + "…"
        parts.append(f'<text x="{pad_l + i * bar_w + bar_w / 2:.1f}" y="{pad_t + plot_h + 18}" '
                     f'font-size="11" text-anchor="middle" fill="#555">{html.escape(t)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">' + "".join(parts) + "</svg>")


def build_html(title, headers, rows, chart_col, label_col):
    stats_blocks, chart = [], ""

    if chart_col and chart_col in headers:
        ci = headers.index(chart_col)
        li = headers.index(label_col) if label_col in headers else 0
        labels, values = [], []
        for row in rows:
            v = to_number(row[ci]) if ci < len(row) else None
            if v is not None:
                labels.append(row[li] if li < len(row) else "")
                values.append(v)
        if values:
            stats_blocks = [
                ("合计", f"{sum(values):,.2f}"),
                ("平均", f"{statistics.mean(values):,.2f}"),
                ("最大", f"{max(values):,.2f}"),
                ("最小", f"{min(values):,.2f}"),
            ]
            chart = svg_bar_chart(labels, values, title=f"{chart_col} · 柱状图")

    cards = "".join(f'<div class="card"><div class="k">{k}</div>'
                    f'<div class="v">{v}</div></div>' for k, v in stats_blocks)
    thead = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>"
                  for row in rows)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
  body {{ font-family: "Microsoft YaHei", system-ui, sans-serif; margin: 0;
         background: #f5f7fb; color: #222; }}
  .wrap {{ max-width: 900px; margin: 0 auto; padding: 28px 20px 60px; }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  .sub {{ color: #888; font-size: 13px; margin-bottom: 20px; }}
  .cards {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }}
  .card {{ background: #fff; border-radius: 10px; padding: 14px 18px; min-width: 120px;
          box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
  .card .k {{ font-size: 12px; color: #999; }}
  .card .v {{ font-size: 20px; font-weight: 600; color: #2b4bd8; margin-top: 4px; }}
  .chart, .tablebox {{ background: #fff; border-radius: 10px; padding: 16px;
          margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.06); overflow-x: auto; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
  th, td {{ border-bottom: 1px solid #eee; padding: 7px 10px; text-align: left;
           white-space: nowrap; }}
  th {{ background: #fafbff; position: sticky; top: 0; }}
  tr:hover td {{ background: #f6f8ff; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>{html.escape(title)}</h1>
  <div class="sub">report_gen.py 生成 · 共 {len(rows)} 行 · {now}</div>
  <div class="cards">{cards}</div>
  {f'<div class="chart">{chart}</div>' if chart else ""}
  <div class="tablebox"><table><thead><tr>{thead}</tr></thead><tbody>{trs}</tbody></table></div>
</div>
</body>
</html>"""


def main():
    p = argparse.ArgumentParser(description="CSV → 单文件 HTML 报表")
    p.add_argument("--input", required=True, help="输入 CSV")
    p.add_argument("--out", default="report.html", help="输出 HTML")
    p.add_argument("--title", default="数据报表")
    p.add_argument("--chart-column", default=None, help="用于统计和画图的数值列名")
    p.add_argument("--label-column", default=None, help="图表 X 轴标签列名")
    args = p.parse_args()
    headers, rows = read_csv(args.input)
    out_html = build_html(args.title, headers, rows, args.chart_column, args.label_column)
    Path(args.out).write_text(out_html, encoding="utf-8")
    print(f"报表已生成: {args.out}  （双击用浏览器打开）")


if __name__ == "__main__":
    main()
