import os
import stat
import subprocess
from datetime import datetime

def get_code_changes():
    """ステージング済みの編集差分を取得"""
    result = subprocess.run(
        ['git', 'diff', '--staged'],  # ステージング済みの差分を取得
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def format_content(diff_text):
    """差分テキストを整形"""
    max_length = 10000 - 4 - 8  # ハッシュタグと行頭の余白を考慮
    trimmed = (diff_text[:max_length] + '...') if len(diff_text) > max_length else diff_text
    
    # 差分のフォーマット整形
    formatted = []
    for line in trimmed.split('\n'):
        if line.startswith('+'):
            formatted.append(f"✅ {line[1:]}")
        elif line.startswith('-'):
            formatted.append(f"❌ {line[1:]}")
        else:
            formatted.append(line)
    message = f"```{''.join(formatted)}```#今日の積み上げ"
    return message

def create_markdown(content):
    """日付ベースのMDファイル生成"""
    date_str = datetime.now().strftime("%Y%m%d")
    os.makedirs('item', exist_ok=True)
    
    with open(f'item/{date_str}.md', 'w') as f:
        f.write(f"# {date_str}\n\n{content}")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'nikki.txt')
    #os.chmod(file_path, stat.S_IWRITE)
    # ニッキーファイルの内容を削除
    with open(file_path, 'w', encoding='utf-8') as f:
        pass

def main():
    code_diff = get_code_changes()
    if not code_diff:
        print("差分が見つかりませんでした")
        return
    
    formatted = format_content(code_diff)
    create_markdown(formatted)
    print(f"Created: item/{datetime.now().strftime('%Y%m%d')}.md")

if __name__ == "__main__":
    main()
