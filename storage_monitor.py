#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kohei Ebara s25c1013za@chibatech.ac.jp
# SPDX-License-Identifier: BSD-3-Clause

import os
import platform
import shutil
import sys


def is_wsl() -> bool:
    """WSL環境かどうかを判定する"""
    return "microsoft" in platform.release().lower()


def select_drive() -> str:
    """CドライブまたはDドライブを選択する"""
    print("C : Cドライブ", file=sys.stderr)
    print("D : Dドライブ", file=sys.stderr)
    print("ドライブを選択してください: ", end="", file=sys.stderr)

    try:
        choice = input().strip().upper()

    except (KeyboardInterrupt, EOFError):
        print("\n入力が中断されました。", file=sys.stderr)
        sys.exit(1)

    if choice in ["C", "D"]:
        return choice

    print("入力が正しくありません。CまたはDを入力してください。", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    """メイン処理"""
    os_name = platform.system()

    # OSに応じてドライブのパスを設定
    if os_name == "Windows":
        drive_paths = {
            "C": "C:\\",
            "D": "D:\\"
        }

    elif os_name == "Linux" and is_wsl():
        drive_paths = {
            "C": "/mnt/c",
            "D": "/mnt/d"
        }

    else:
        print("対応していないOSです。", file=sys.stderr)
        sys.exit(1)

    # ドライブを選択
    drive = select_drive()
    path = drive_paths[drive]

    # ドライブの存在確認
    if not os.path.exists(path):
        print("指定されたドライブが見つかりません。", file=sys.stderr)
        sys.exit(1)

    # 空き容量を取得
    try:
        usage = shutil.disk_usage(path)

        # 空き容量のみを標準出力に出力
        print(usage.free)

    except OSError as e:
        print(f"ストレージ情報の取得に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

    # 正常終了
    sys.exit(0)


if __name__ == "__main__":
    main()
