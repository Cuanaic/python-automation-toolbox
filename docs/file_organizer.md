# file_organizer —— 文件批量整理

按文件类型或修改日期，把目录里的一堆文件归档到子文件夹。**先预览、后执行**，绝不覆盖同名文件。

## 用法

```bash
# 1. 先预览（不动任何文件）
python tools/file_organizer.py --dir ~/Downloads --dry-run

# 2. 按类型整理（图片/视频/文档/压缩包/程序/其他）
python tools/file_organizer.py --dir ~/Downloads

# 3. 按修改月份归档（2024-01、2024-02 …）
python tools/file_organizer.py --dir ~/Photos --by date

# 4. 复制而非移动（保留原文件）
python tools/file_organizer.py --dir ~/Desktop --copy
```

## 参数

| 参数 | 说明 |
|---|---|
| `--dir` | 要整理的目录（必填） |
| `--by ext` | 按文件类型归档（默认） |
| `--by date` | 按修改日期 `年-月` 归档 |
| `--copy` | 复制而非移动 |
| `--dry-run` | 只预览计划，不做任何改动 |

## 安全设计

- 默认先建议 `--dry-run` 预览
- 目标同名文件自动重命名（`file (1).jpg`），**永不覆盖**
- 只处理一层目录里的文件，不动已有的子文件夹
