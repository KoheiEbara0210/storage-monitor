import json
import shutil
import subprocess


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


def get_physical_disk_health() -> None:
    """Windows側のPowerShell経由で物理ディスクの温度・摩耗率・稼働時間を取得する"""
    ps_command = """
    Get-PhysicalDisk | ForEach-Object {
        $c = $_ | Get-StorageReliabilityCounter -ErrorAction SilentlyContinue
        [PSCustomObject]@{
            Name = $_.FriendlyName
            MediaType = $_.MediaType
            Health = $_.HealthStatus
            Temp = if ($c) { $c.Temperature } else { $null }
            Wear = if ($c) { $c.Wear } else { $null }
            Hours = if ($c) { $c.PowerOnHours } else { $null }
        }
    } | ConvertTo-Json -Compress
    """

    print("=== 物理ストレージ詳細 (Windows経由) ===")
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=15,
        )
        output = result.stdout.strip()
        if not output:
            print("情報を取得できませんでした（管理者権限が必要な場合があります）。")
            return

        disks = json.loads(output)
        if isinstance(disks, dict):
            disks = [disks]

        for disk in disks:
            temp = f"{disk['Temp']} ℃" if disk.get("Temp") is not None else "取得不可"
            wear = f"{disk['Wear']} %" if disk.get("Wear") is not None else "取得不可"
            hours = f"{disk['Hours']} 時間" if disk.get("Hours") is not None else "取得不可"

            print(f"モデル名 : {disk.get('Name', '不明')} ({disk.get('MediaType', '不明')})")
            print(f"健康状態 : {disk.get('Health', '不明')}")
            print(f"温度   : {temp}")
            print(f"摩耗率  : {wear}")
            print(f"稼働時間 : {hours}")
            print("-" * 35)

    except FileNotFoundError:
        print("powershell.exe が見つかりません（WSL環境ではない可能性があります）。")
    except Exception as e:
        print(f"取得中にエラーが発生しました: {e}")


if __name__ == "__main__":
    get_storage_info("/mnt/c")
    print()
    get_storage_info("/")
    print()
    get_physical_disk_health()
