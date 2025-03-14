import os
import uuid
from datetime import datetime

def create_chat_interface_explanation():
    """ChatInterface コンポーネントの解説を Markdown ファイルとして生成"""
    # UUID を生成してファイル名として使用
    file_uuid = str(uuid.uuid4())
    destination = os.path.join("blog", "lib")
    os.makedirs(destination, exist_ok=True)
    
    # 現在の日付
    date_str = datetime.now().strftime("%Y%m%d")
    
    # Markdown コンテンツ
    content = """# React チャットインターフェースの実装解説

## 概要

このドキュメントでは、React と Supabase を使用したリアルタイムチャットインターフェースの実装について解説します。このコンポーネントは、1対1のプライベートチャット、スタンプ送信機能、ステータス表示などの機能を備えています。

## 主要な機能

1. **リアルタイムメッセージング**
   - Supabase のリアルタイム購読機能を使用
   - メッセージの送受信をリアルタイムで反映

2. **スタンプ機能**
   - 9種類のスタンプを送信可能
   - テキストとスタンプの組み合わせも可能

3. **クイックリプライ**
   - よく使うフレーズをワンクリックで入力
   - ユーザーの感情エントリーと連携

4. **ステータス管理**
   - 相手のステータスをリアルタイムで表示
   - 「対応可能」状態のみチャット可能

## 技術スタック

- **フロントエンド**: React, TypeScript
- **UI コンポーネント**: Lucide React, カスタムコンポーネント
- **バックエンド**: Supabase (PostgreSQL + リアルタイム機能)
- **認証**: Supabase Auth
- **日付フォーマット**: date-fns

## 実装の詳細

### 状態管理

```tsx
const [messages, setMessages] = useState<ChatMessage[]>([]);
const [inputValue, setInputValue] = useState('');
const [selectedStamp, setSelectedStamp] = useState<string | null>(null);
const [chatRoom, setChatRoom] = useState<ChatRoom | null>(null);
const [loading, setLoading] = useState(true);
const [opponentStatus, setOpponentStatus] = useState<string>('対応可能');
const [canChat, setCanChat] = useState(true);
```

### チャットルームの初期化

チャットルームの初期化では、以下のステップを実行します：

1. 既存のチャットルームを検索
2. 存在しない場合は新規作成
3. 相手のユーザー情報を取得
4. メッセージの初期ロード

### リアルタイム購読

Supabase のチャンネル機能を使用して、以下の変更をリアルタイムで監視：

1. 新しいメッセージの挿入
2. 相手のステータス変更

```tsx
const messagesSubscription = supabase
  .channel('chat-messages')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'chatmessages',
      filter: `room_id=eq.${chatRoom.id}`,
    },
    (payload) => {
      const newMessage = payload.new as ChatMessage;
      setMessages((current) => [...current, newMessage]);
      scrollToBottom();
    }
  )
  .subscribe();
```

### メッセージ送信

```tsx
const handleSend = async () => {
  if ((!inputValue.trim() && !selectedStamp) || !session?.user || !chatRoom)
    return;

  try {
    const messageData = {
      room_id: chatRoom.id,
      sender_id: session.user.id,
      content: inputValue.trim(),
      stamp: selectedStamp || null,
    };

    const { error } = await supabase.from('chatmessages').insert(messageData);

    if (error) throw error;

    // 送信後に最新のメッセージを再取得
    fetchMessages(chatRoom.id);

    setInputValue('');
    setSelectedStamp(null);
  } catch (error) {
    console.error('メッセージ送信エラー:', error.message);
    toast({
      title: 'エラー',
      description: 'メッセージの送信に失敗しました',
      variant: 'destructive',
    });
  }
};
```

### スタンプ機能

スタンプは画像パスとして管理され、選択時に即時送信またはテキストと組み合わせて送信できます：

```tsx
const stamps = [
  { path: '/stamp/moji_yasumi.png', name: 'やすみたい' },
  { path: '/stamp/moji_yaritai.png', name: 'やる気' },
  // ...他のスタンプ
];

const handleStampSelect = (stampPath: string) => {
  setSelectedStamp(stampPath);
  // スタンプのみの場合は即時送信
  if (!inputValue.trim()) {
    // ...送信ロジック
  }
};
```

### UI コンポーネント

UI は以下の主要セクションで構成されています：

1. **チャットヘッダー**: 相手の名前とステータスを表示
2. **メッセージエリア**: スクロール可能なメッセージ履歴
3. **入力エリア**: テキスト入力、スタンプ選択、クイックリプライボタン

## データモデル

### ChatMessage インターフェース

```tsx
interface ChatMessage {
  id: number;
  content: string;
  sender_id: string;
  created_at: string;
  stamp?: string;
  profiles?: {
    username: string;
  };
}
```

### ChatRoom インターフェース

```tsx
interface ChatRoom {
  id: number;
  name: string;
  opponent_id: string;
  opponent_username?: string;
  opponent_status?: string;
}
```

## 改善点と拡張可能性

1. **既読機能**: メッセージの既読状態を追加
2. **メディア共有**: 画像や動画の共有機能
3. **メッセージ検索**: 過去のメッセージを検索する機能
4. **グループチャット**: 複数ユーザーでのチャット機能
5. **メッセージ編集/削除**: 送信済みメッセージの編集・削除機能

## まとめ

このチャットインターフェースは、React と Supabase を組み合わせることで、リアルタイム性の高い使いやすいチャット体験を提供しています。スタンプ機能やステータス管理など、ユーザーエクスペリエンスを向上させる機能が実装されており、さらなる拡張も容易な設計になっています。
"""
    
    # ファイル書き込み
    new_file = os.path.join(destination, f"{file_uuid}.md")
    with open(new_file, "w", encoding="utf-8") as f:
        f.write(f"# {date_str}\n\n{content}")
    
    print(f"Created: {new_file}")

if __name__ == "__main__":
    create_chat_interface_explanation() 
