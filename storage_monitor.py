import shutil


def format_bytes(size_bytes: float) -> str:
    """バイト数を読みやすい単位（GB, TBなど）に変換する"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def get_storage_info(path: str = "/") -> None:
    """指定パスのストレージ容量と使用量を表示する"""
    usage = shutil.disk_usage(path)
    percent = (usage.used / usage.total) * 100

    print(f"=== ストレージ状態 ({path}) ===")
    print(f"総容量  : {format_bytes(usage.total)}")
    print(f"使用量  : {format_bytes(usage.used)} ({percent:.1f}%)")
    print(f"空き容量 : {format_bytes(usage.free)}")


if __name__ == "__main__":
    get_storage_info("/mnt/c")  # Windows本体 (Cドライブ)
    print()
    get_storage_info("/")       # WSL2 (Ubuntu仮想環境)
