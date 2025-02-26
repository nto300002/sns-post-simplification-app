# 20250226

読み込み高速化
useEffect(() => {
if (session?.user?.id) { //session ではなく
fetchMembers();
}
}, [session?.user?.id]);

メンバー承認処理の問題と解決策のまとめ
問題点
RLS ポリシーの制約違反
エラー: "new row violates row-level security policy for table \"usermembers\""
フロントエンドから直接 usermembers テーブルに挿入しようとした際に発生
相互関係の作成の複雑さ
双方向のメンバー関係（A が B のメンバー、B が A のメンバー）を作成する必要がある
2 つの別々の挿入操作が必要で、整合性が保証されない 3. RLS ポリシーの設計難易度
複雑な条件を持つ RLS ポリシーが正しく機能しない場合がある
特に相互関係を要する場合、適切なポリシー設計が困難

解決策
SQL 関数によるアプローチ（採用した解決策）

-- データベース側で関数を作成
CREATE OR REPLACE FUNCTION accept_member_invite(invite_id INTEGER, current_user_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
invite_record RECORD;
BEGIN
-- 招待を取得・検証
SELECT inviter_id, invitee_id INTO invite_record
FROM memberinvites
WHERE id = invite_id AND invitee_id = current_user_id;

IF NOT FOUND THEN
RETURN FALSE;
END IF;

-- 招待ステータスを更新
UPDATE memberinvites
SET status = 'accepted'
WHERE id = invite_id;

-- 双方向のメンバー関係を作成
INSERT INTO usermembers (user_id, member_id)
VALUES
(invite_record.inviter_id, invite_record.invitee_id),
(invite_record.invitee_id, invite_record.inviter_id)
ON CONFLICT DO NOTHING;

RETURN TRUE;
END;

$$
LANGUAGE plpgsql SECURITY DEFINER;

解決策のメリット
RLSポリシーのバイパス
SECURITY DEFINERにより、関数はポリシーを迂回して実行される
トランザクション整合性
すべての操作が単一トランザクション内で実行され、部分的な更新を防止
セキュリティの向上
ユーザーが適切な権限を持つ場合のみ操作が成功する
SQLインジェクションのリスクが軽減される
コードの簡素化
フロントエンド側のコードが大幅に簡略化される
複雑なエラーハンドリングが不要に
$$
