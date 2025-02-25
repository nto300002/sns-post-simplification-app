PostgreSQL の RLS ポリシーを活用したデータアクセス制御
こんにちは、エンジニアの皆さん。今日は PostgreSQL の Row Level Security (RLS) ポリシーについて掘り下げていきたいと思います。特に PostgREST と組み合わせた実装パターンに焦点を当てます。
RLS ポリシーとは？
PostgreSQL の Row Level Security (RLS) は、テーブルレベルではなく行レベルでのアクセス制御を可能にする強力な機能です。これにより、同じテーブルに対して異なるユーザーに異なる行の表示・編集権限を与えることができます。

PostgreSQL の OLD と NEW 参照
RLS ポリシーを作成する際、トリガーと同様に OLD と NEW という特殊な参照を使用できます。これらは更新前後のレコード状態を参照するもので、特に UPDATE や DELETE 操作の制御に役立ちます。

```
CREATE POLICY update_if_owner ON posts
    FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = NEW.user_id);
```

実践的な複雑クエリ例
以下は、ユーザープロファイルと関連データを取得する複雑なクエリ例です。このようなクエリを RLS と組み合わせることで、ユーザーごとに適切なデータのみを返すことができます。

```
SELECT
  p.id,
  p.username,
  p.created_at,
  p.updated_at,
  row_to_json(ps._) AS profilestatus,
  row_to_json(us._) AS userstatus,
  (
    SELECT json_agg(row_to_json(um_data))
    FROM (
      SELECT
        um.user_id,
        um.member_id,
        um.created_at,
        row_to_json(pr._) AS member_profile
      FROM usermembers um
      JOIN profiles pr ON pr.id = um.member_id
      WHERE um.user_id = p.id
    ) AS um_data
  ) AS usermembers,
  (
    SELECT json_agg(row_to_json(mi_data))
    FROM (
      SELECT
        mi.id,
        mi.inviter_id,
        mi.invitee_id,
        mi.status,
        mi.created_at,
        mi.updated_at,
        row_to_json(pi._) AS inviter_profile,
        row_to_json(pe.*) AS invitee_profile
      FROM memberinvites mi
      JOIN profiles pi ON pi.id = mi.inviter_id
      JOIN profiles pe ON pe.id = mi.invitee_id
      WHERE mi.inviter_id = p.id OR mi.invitee_id = p.id
    ) AS mi_data
  ) AS memberinvites
FROM profiles p
LEFT JOIN ProfileStatus ps ON p.id = ps.profile_id
LEFT JOIN UserStatus us ON ps.status_id = us.id
WHERE p.id = 'user uuid';
```

このクエリでは:
プロファイル基本情報の取得
プロファイルステータスとユーザーステータスの JOIN
ネストされたサブクエリによるユーザーメンバー情報の取得
招待情報の取得と関連プロファイルの JOIN

実装のポイント
RLS ポリシーを実装する際の重要なポイントは:
適切な粒度の設計: 必要以上に複雑なポリシーは避け、シンプルで理解しやすいものにする
パフォーマンスへの配慮: 複雑なポリシーはクエリのパフォーマンスに影響する可能性がある
テスト: 様々なユーザーロールでポリシーが正しく機能することを確認する
メンテナンス性: 将来の変更に対応しやすいよう、ポリシーの目的と動作を文書化する

まとめ
PostgreSQL の RLS ポリシーは、アプリケーションのセキュリティ層を強化する強力なツールです。特に PostgREST のようなツールと組み合わせることで、API 開発の効率化とセキュリティの向上を同時に実現できます。
次回は、これらのポリシーをテストする効率的な方法について掘り下げていきたいと思います。
