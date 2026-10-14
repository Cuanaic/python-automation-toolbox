#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文件批量整理工具：按类型 / 修改日期把文件归档到子文件夹。

示例:
  python tools/file_organizer.py --dir ~/Downloads --dry-run     # 先预览
  python tools/file_organizer.py --dir ~/Downloads               # 按类型整理
  python tools/file_organizer.py --dir ~/Photos --by date        # 按修改月份归档
  python tools/file_organizer.py --dir ~/Downloads --copy        # 复制而非移动
"""
import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

CATEGORIES = {
    "图片": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic", ".tif"},
    "视频": {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"},
    "音频": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "文档": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"},
    "压缩包": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "程序": {".exe", ".msi", ".apk", ".dmg", ".py", ".js", ".bat", ".sh"},
}


def categorize(path: Path) -> str:
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "其他"


def unique_target(dst: Path) -> Path:
    """目标重名时自动加序号，绝不覆盖已有文件。"""
    if not dst.exists():
        return dst
    stem, i = dst.stem, 1
    while True:
        cand = dst.with_name(f"{stem} ({i}){dst.suffix}")
        if not cand.exists():
            return cand
        i += 1


def main():
    p = argparse.ArgumentParser(description="文件批量整理工具（先加 --dry-run 预览）")
    p.add_argument("--dir", required=True, help="要整理的目录")
    p.add_argument("--by", choices=["ext", "date"], default="ext",
                   help="ext=按文件类型，date=按修改日期(年-月)")
    p.add_argument("--copy", action="store_true", help="复制而非移动（默认移动）")
    p.add_argument("--dry-run", action="store_true", help="只预览，不动任何文件")
    args = p.parse_args()

    src = Path(args.dir).expanduser()
    if not src.is_dir():
        sys.exit(f"目录不存在: {src}")

    files = [f for f in src.iterdir() if f.is_file()]
    if not files:
        sys.exit("目录里没有文件")

    action = "复制" if args.copy else "移动"
    done = 0
    for f in files:
        if args.by == "ext":
            group = categorize(f)
        else:
            group = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m")
        dst = src / group / f.name
        if args.dry_run:
            print(f"[预览] {f.name}  →  {group}/{f.name}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst = unique_target(dst)
        if args.copy:
            shutil.copy2(f, dst)
        else:
            shutil.move(str(f), str(dst))
        done += 1

    if args.dry_run:
        print(f"\n共 {len(files)} 个文件。确认无误后去掉 --dry-run 即执行{action}。")
    else:
        print(f"完成: {action}了 {done} 个文件到对应子文件夹")


if __name__ == "__main__":
    main()
