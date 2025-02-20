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

def create_markdown():
    """nikki.md の内容を利用して、blog/libフォルダ直下にMDファイル生成"""
    date_str = datetime.now().strftime("%Y%m%d")
    destination = os.path.join("blog", "lib")
    os.makedirs(destination, exist_ok=True)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    nikki_md_path = os.path.join(current_dir, "nikki.md")
    with open(nikki_md_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_file = os.path.join(destination, f"{date_str}.md")
    with open(new_file, "w", encoding="utf-8") as f:
         f.write(f"# {date_str}\n\n{content}")
    
    # nikki.md の内容をクリアする
    with open(nikki_md_path, "w", encoding="utf-8") as f:
         pass
    print(f"Created: {new_file}")

def main():
    create_markdown()
    
if __name__ == "__main__":
    main()
