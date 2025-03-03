-- 1. カラムをタイムゾーン付きタイムスタンプ型に変更
ALTER TABLE chatmessages
ALTER COLUMN created_at TYPE timestamptz;

-- 2. データベースのデフォルトタイムゾーンを設定
ALTER DATABASE postgres SET timezone TO 'Asia/Tokyo';

-- 3. 既存データを日本時間に変換（データが既にある場合）
UPDATE chatmessages
SET created_at = created_at AT TIME ZONE 'JST' AT TIME ZONE 'Asia/Tokyo';

-- 4. デフォルト値を現在時刻（JST）に設定
ALTER TABLE chatmessages
ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;

-- 5. タイムゾーン設定を確認
SHOW timezone;

PostgreSQL のタイムゾーン設定解説
ここに記載されている内容は、PostgreSQL のタイムゾーン設定に関する SQL コマンドです。これらのコマンドは、データベースのタイムスタンプを日本時間で適切に扱うための一連の手順を示しています。

1. タイムゾーン付きタイムスタンプ型への変更
   ;
   解説:
   timestamptz はタイムゾーン情報を持つタイムスタンプ型
   通常の timestamp と異なり、タイムゾーンの変換を自動的に処理
   内部では UTC で保存されるが、クライアントのタイムゾーン設定に応じて自動変換
2. データベースのタイムゾーン設定
   ;
   解説:
   データベース全体のデフォルトタイムゾーンを日本時間（JST）に設定
   新しく接続するセッションはすべてこの設定を継承
   時差：UTC+9 時間
3. 既存データの変換
   ;
   解説:
   既存データのタイムスタンプを正しいタイムゾーン情報に更新
   二重の AT TIME ZONE 句を使用：
   最初の AT TIME ZONE 'JST'：値を JST として解釈
4. 次の AT TIME ZONE 'Asia/Tokyo'：それを Asia/Tokyo（日本時間）に変換
   この複雑な変換は、データの整合性を確保するため
5. デフォルト値の設定
   ;
   解説:
   新規レコード作成時に自動的に現在時刻が挿入されるよう設定
   CURRENT_TIMESTAMP はセッションのタイムゾーン（この場合 JST）に基づく
6. タイムゾーン設定の確認
   ;
   解説:
   現在のセッションで有効なタイムゾーン設定を表示
   予期される結果：Asia/Tokyo
   技術的背景と重要ポイント
   国際的なアプリケーション対応:
   タイムゾーン付きデータ型を使用することで、異なるタイムゾーンのユーザーに対しても適切な時刻表示が可能
   データの一貫性:
   内部的には UTC で保存されるため、サマータイムなどの複雑な変更にも対応
   アプリケーション側の考慮点:
   JavaScript などのクライアント側では、new Date()で取得した時刻はローカルタイムゾーンに自動変換される
   Supabase などのサービスを使用する場合、クエリ結果は自動的にセッションのタイムゾーンに変換される
   この設定により、日本向けアプリケーションでの日時表示が正確かつ一貫して行われるようになります。
