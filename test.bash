cat << 'EOF' > test.bash
#!/usr/bin/env bash
set -euo pipefail

PASS_COUNT=0
FAIL_COUNT=0

assert_equals() {
  local actual="$1"
  local expected="$2"
  local test_name="$3"

  if [ "$actual" = "$expected" ]; then
    echo "[PASS] $test_name"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    echo "[FAIL] $test_name (期待: '$expected', 実際: '$actual')"
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
}

assert_regex() {
  local actual="$1"
  local pattern="$2"
  local test_name="$3"

  if [[ "$actual" =~ $pattern ]]; then
    echo "[PASS] $test_name"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    echo "[FAIL] $test_name (パターン '$pattern' に不一致: '$actual')"
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
}

echo "=== storage_monitor.py テスト開始 ==="

# 1. Cドライブ指定（標準出力に空き容量の数値が出ること、終了コード0）
set +e
OUT_C="$(printf "c\n" | python3 storage_monitor.py 2>/dev/null)"
CODE_C=$?
set -e
assert_equals "$CODE_C" "0" "Cドライブ入力時の終了コードが0"
assert_regex "$OUT_C" '^[0-9]+$' "Cドライブ入力時の標準出力が数字のみ"

# 2. 不正な入力（標準入力にXを渡したとき終了コード1になること）
set +e
printf "X\n" | python3 storage_monitor.py >/dev/null 2>&1
CODE_INVALID=$?
set -e
assert_equals "$CODE_INVALID" "1" "不正入力時の終了コードが1"

# 3. 入力EOF（空入力で中断したとき終了コード1になること）
set +e
printf "" | python3 storage_monitor.py >/dev/null 2>&1
CODE_EOF=$?
set -e
assert_equals "$CODE_EOF" "1" "入力中断（EOF）時の終了コードが1"

echo "----------------------------------------"
echo "結果: PASS=${PASS_COUNT}, FAIL=${FAIL_COUNT}"

if [ "$FAIL_COUNT" -ne 0 ]; then
  exit 1
fi
EOF
chmod +x test.bash
./test.bash
