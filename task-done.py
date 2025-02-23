import os

def append_done_to_files(directory):
    # 指定されたディレクトリ以下のすべてのファイルを再帰的に処理します
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                # 各ファイルを追記モードで開き、テキストを追加します
                with open(file_path, "a", encoding="utf-8") as file:
                    file.write("Done!")
                print(f"Appended 'Done!' to {file_path}")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

if __name__ == '__main__':
    append_done_to_files("item")
