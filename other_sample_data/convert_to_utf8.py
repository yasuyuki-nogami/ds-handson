"""
SampleフォルダのCSVファイルをUTF-8に変換するスクリプト
文科省データ（Shift_JIS）とSSDSEデータ（CP932）を対象
"""

import os
from pathlib import Path

# 変換対象のファイル
TARGET_FILES = [
    "h27_pupils.csv",
    "h27_students.csv",
    "h27_elementary_school.csv",
    "h27_junior_school.csv",
    "r6_pupils.csv",
    "r6_students.csv",
    "SSDSE-A-2025.csv",
    "SSDSE-B-2025.csv",
    "SSDSE-E-2025.csv",
]

# 試行するエンコーディングのリスト
ENCODINGS_TO_TRY = ['utf-8', 'shift_jis', 'cp932', 'euc-jp', 'iso-2022-jp']

def detect_encoding(file_path: str) -> str:
    """ファイルのエンコーディングを検出する（試行錯誤方式）"""
    for encoding in ENCODINGS_TO_TRY:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                # 最初の1000文字読んでみる
                f.read(1000)
            return encoding
        except (UnicodeDecodeError, LookupError):
            continue
    return None

def convert_to_utf8(file_path: str, backup: bool = True):
    """ファイルをUTF-8に変換する"""
    print(f"\n処理中: {os.path.basename(file_path)}")
    
    # エンコーディング検出
    detected_encoding = detect_encoding(file_path)
    
    if not detected_encoding:
        print(f"  ❌ エンコーディングを検出できませんでした")
        return
    
    print(f"  検出エンコーディング: {detected_encoding}")
    
    if detected_encoding.lower() == 'utf-8':
        print(f"  ⏭️  スキップ（既にUTF-8）")
        return
    
    # バックアップ作成
    if backup:
        backup_path = file_path + ".bak"
        if not os.path.exists(backup_path):
            with open(file_path, 'rb') as src:
                with open(backup_path, 'wb') as dst:
                    dst.write(src.read())
            print(f"  💾 バックアップ作成: {os.path.basename(backup_path)}")
    
    try:
        # ファイル読み込み（検出したエンコーディングで）
        with open(file_path, 'r', encoding=detected_encoding, errors='replace') as f:
            content = f.read()
        
        # UTF-8で書き込み（BOM付き：Excelでも文字化けしない）
        with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(content)
        
        print(f"  ✅ 変換完了: {detected_encoding} → UTF-8-BOM")
        
    except Exception as e:
        print(f"  ❌ エラー: {e}")

def main():
    print("=" * 60)
    print("  CSV文字コード変換ツール")
    print("=" * 60)
    
    sample_dir = Path(__file__).parent
    
    for filename in TARGET_FILES:
        file_path = sample_dir / filename
        if file_path.exists():
            convert_to_utf8(str(file_path))
        else:
            print(f"\n⚠️  ファイルが見つかりません: {filename}")
    
    print("\n" + "=" * 60)
    print("  変換処理完了！")
    print("=" * 60)
    print("\n※ 元のファイルは .bak 拡張子で保存されています")

if __name__ == "__main__":
    main()
