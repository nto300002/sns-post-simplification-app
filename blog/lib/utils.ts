import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { v4 as uuidv4 } from 'uuid';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export interface BlogPost {
  id: string;
  title: string;
  date: string;
  tags: string[];
  image: string;
  excerpt: string;
  content: string;
  filename: string;
}

interface PostMapping {
  [filename: string]: string; // filename -> uuid のマッピング
}

const POST_MAPPING_FILE = path.join(process.cwd(), 'lib', 'post-mapping.json');

// UUIDマッピングの読み込み
function loadPostMapping(): PostMapping {
  try {
    if (fs.existsSync(POST_MAPPING_FILE)) {
      return JSON.parse(fs.readFileSync(POST_MAPPING_FILE, 'utf8'));
    }
  } catch (error) {
    console.error('Error loading post mapping:', error);
  }
  return {};
}

// UUIDマッピングの保存
function savePostMapping(mapping: PostMapping) {
  try {
    fs.writeFileSync(POST_MAPPING_FILE, JSON.stringify(mapping, null, 2));
  } catch (error) {
    console.error('Error saving post mapping:', error);
  }
}

export function getMdPosts(): BlogPost[] {
  const postsDirectory = path.join(process.cwd(), 'lib');
  const fileNames = fs.readdirSync(postsDirectory);
  const mdFiles = fileNames.filter((fileName) => fileName.endsWith('.md'));
  const postMapping = loadPostMapping();

  const posts = mdFiles.map((fileName) => {
    const id = fileName.replace(/\.md$/, '');
    const fullPath = path.join(postsDirectory, fileName);
    const fileContents = fs.readFileSync(fullPath, 'utf8');

    // ファイルにUUIDが未割り当ての場合、新規作成
    if (!postMapping[fileName]) {
      postMapping[fileName] = uuidv4();
      savePostMapping(postMapping);
    }

    // MDファイルの内容を解析
    const { content } = matter(fileContents);

    // ファイル名から日付を取得 (YYYYMMDD形式)
    const date = id.match(/\d{8}/)?.[0] || '';
    const formattedDate = date
      ? `${date.slice(0, 4)}/${date.slice(4, 6)}/${date.slice(6, 8)}`
      : '';

    return {
      id: postMapping[fileName],
      title: `${formattedDate}の投稿`,
      date: formattedDate,
      tags: ['日記'],
      image: '', // プレースホルダー画像が使用される
      excerpt: content.slice(0, 150),
      content,
      filename: fileName, // ファイル名も保持
    };
  });

  // 日付の新しい順にソート
  return posts.sort((a, b) => b.date.localeCompare(a.date));
}

// 個別の投稿を取得する関数を追加
export function getPost(id: string): BlogPost | null {
  const posts = getMdPosts();
  return posts.find((post) => post.id === id) || null;
}
