# Storage Monitor
![test](https://github.com/KoheiEbara0210/storage-monitor/actions/workflows/test.yml/badge.svg)

自分のストレージの空き容量を確認することができるツールです。
最初に `C` ドライブか `D` ドライブのどちらを確認するか標準入力から選択します（`C` または `D` を入力、大文字・小文字対応）。
選択したドライブの空き容量をバイト単位（B）で標準出力へ出力します。

## 必要なソフトウェア
- Python
  - テスト済みバージョン: 3.10〜3.14

## テスト環境
- Ubuntu 24.04 LTS

## テスト実行

```bash
./test.bash
```

## ライセンス
- このソフトウェアパッケージは、3条項BSDライセンスの下、再頒布および使用が許可されます。
- © 2026 Kohei Ebara
