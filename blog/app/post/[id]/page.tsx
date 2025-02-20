import { Header } from '@/components/header';
import { getPost } from '@/lib/utils';
import Image from 'next/image';
import { notFound } from 'next/navigation';
import { Badge } from '@/components/ui/badge';
import Markdown, { Options } from 'react-markdown';

export default function PostPage({ params }: { params: { id: string } }) {
  const post = getPost(params.id);

  if (!post) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <article className="bg-white shadow-md rounded-lg overflow-hidden">
          <div className="relative w-full h-[200px]">
            <Image
              src={post.image || '/placeholder.png'}
              alt={post.title}
              fill
              className="object-cover object-center"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          </div>
          <div className="p-6">
            <h1 className="text-3xl font-bold mb-2">{post.title}</h1>
            <div className="flex items-center justify-between mb-4">
              <time className="text-gray-500">{post.date}</time>
              <div className="flex gap-2">
                {post.tags.map((tag) => (
                  <Badge key={tag} variant="secondary">
                    {tag}
                  </Badge>
                ))}
              </div>
            </div>
            <div className="prose prose-sm md:prose-base lg:prose-lg max-w-none">
              <Markdown children={post.content} />
            </div>
          </div>
        </article>
      </main>
    </div>
  );
}
