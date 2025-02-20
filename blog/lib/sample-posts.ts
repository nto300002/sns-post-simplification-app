export const samplePosts = [
  {
    id: '1',
    title: 'はじめてのブログ投稿',
    date: '2024-02-11',
    tags: ['Tech', 'Programming'],
    image: '',
    excerpt:
      'ブログを始めました。技術的な話題を中心に投稿していきます。プログラミング、ウェブ開発、AI、機械学習など、幅広いトピックについて書いていく予定です。日々の学びや発見、プロジェクトの進捗などをシェアしていきたいと思います。技術の世界は日々進化しているので、常に新しい情報をキャッチアップし、ここで共有していきます。',
    content:
      'ここに投稿の全文が入ります。長文の場合はマークダウン形式で記述することをお勧めします。',
  },
  {
    id: '2',
    title: 'テスト投稿1',
    date: '2024-02-12',
    tags: ['Test'],
    image: '',
    excerpt:
      'これはテスト投稿です。短い文章でも問題なく表示されることを確認します。',
    content: 'テスト投稿の全文です。この投稿は短めの内容となっています。',
  },
  {
    id: '3',
    title: 'テスト投稿2',
    date: '2024-02-13',
    tags: ['Test', 'Short'],
    image: '',
    excerpt: '非常に短い文章。',
    content:
      'これは非常に短い投稿の全文です。タイトルと内容がほぼ同じくらいの長さです。',
  },
];

export type Post = (typeof samplePosts)[number];

export function getSortedPosts(): Post[] {
  return [...samplePosts].sort((a, b) => {
    return new Date(b.date).getTime() - new Date(a.date).getTime();
  });
}
