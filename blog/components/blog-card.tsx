import Image from 'next/image';
import Link from 'next/link';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface BlogCardProps {
  id: string;
  title: string;
  date: string;
  tags: string[];
  image: string;
  excerpt: string;
}

export function BlogCard({
  id,
  title,
  date,
  tags,
  image,
  excerpt,
}: BlogCardProps) {
  const truncatedExcerpt =
    excerpt.length > 150 ? excerpt.slice(0, 150) + '...' : excerpt;

  return (
    <Link
      href={`/post/${id}`}
      className="block hover:opacity-80 transition-opacity"
    >
      <Card className="overflow-hidden h-full">
        <div className="aspect-video relative">
          <Image
            src={image || '/placeholder.png'}
            alt={title}
            fill
            className="object-cover"
          />
        </div>
        <CardHeader className="flex flex-row items-center justify-between">
          <h2 className="text-xl font-semibold">{title}</h2>
          <time className="text-sm text-gray-500">{date}</time>
        </CardHeader>
        <CardContent>
          <div className="mb-4 flex gap-2">
            {tags.map((tag) => (
              <Badge key={tag} variant="secondary">
                {tag}
              </Badge>
            ))}
          </div>
          <div>
            <p className="text-gray-600">{truncatedExcerpt}</p>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
