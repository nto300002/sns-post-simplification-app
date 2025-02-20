import { Header } from '@/components/header';
import { SearchBar } from '@/components/search-bar';
import { BlogCard } from '@/components/blog-card';
import { getMdPosts } from '@/lib/utils';

export default function Home() {
  const posts = getMdPosts();

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <SearchBar />
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {posts.map((post) => (
            <BlogCard key={post.id} {...post} />
          ))}
        </div>
      </main>
    </div>
  );
}
