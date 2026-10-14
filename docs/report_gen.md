# report_gen —— CSV 转 HTML 报表

把 CSV 变成一份**自包含的 HTML 报表**：统计卡片 + SVG 柱状图 + 完整表格。
零第三方依赖，生成的文件可以双击打开、打印、直接微信发送。

## 用法

```bash
python tools/report_gen.py --input all.csv --title "订单报表" \
    --chart-column 金额 --label-column 月份
```

参数说明：

| 参数 | 说明 |
|---|---|
| `--input` | 输入 CSV 文件 |
| `--out` | 输出 HTML（默认 `report.html`） |
| `--title` | 报表标题 |
| `--chart-column` | 用于统计和画图的**数值列**（计算合计/平均/最大/最小） |
| `--label-column` | 图表 X 轴的标签列（默认第一列） |

## 输出效果

- 顶部统计卡片：合计 / 平均 / 最大 / 最小
- 中部 SVG 柱状图（鼠标悬停显示数值）
- 底部完整数据表格（表头吸顶、hover 高亮）
- 生成时间是自动带上的；表格行数不设上限，只显示前 40 根柱子防止挤成一团

## 完整演示

```bash
python samples/make_samples.py
python tools/excel_batch.py merge samples/orders_q1.csv samples/orders_q2.csv -o all.csv
python tools/report_gen.py --input all.csv --title "2024 订单报表" \
    --chart-column 金额 --label-column 月份
# 双击 report.html 查看
```
