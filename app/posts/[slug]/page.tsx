import { getPostBySlug, getAllPosts } from '@/lib/posts';
import { format } from 'date-fns';
import { notFound } from 'next/navigation';
import ShareButton from '@/components/ShareButton';

export async function generateStaticParams() {
  const posts = getAllPosts();
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = getPostBySlug(slug);

  if (!post) {
    return {};
  }

  const baseMetadata = {
    title: `${post.title} | Peter's Bookstore`,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.date,
      authors: ['Peter'],
      siteName: "Peter's Bookstore",
      ...(post.image && { images: [{ url: post.image }] }),
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      creator: '@cytronicoder',
      ...(post.image && { images: [post.image] }),
    },
  };

  return baseMetadata;
}

export default async function PostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  return (
    <article className="max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4" style={{ color: 'var(--text-color)' }}>
          {post.title}
        </h1>
        <div className="flex items-center justify-between mb-6" style={{ color: 'var(--text-color)', opacity: 0.7 }}>
          <time dateTime={post.date}>
            {format(new Date(post.date), 'MMMM dd, yyyy')}
          </time>
          <ShareButton title={post.title} />
        </div>
      </div>

      <div
        className="prose prose-lg max-w-none"
        style={{ color: 'var(--text-color)' }}
        dangerouslySetInnerHTML={{ __html: post.content }}
      />

      <div className="mt-12 pt-8" style={{ borderTop: '1px solid var(--foreground)' }}>
        <a
          href="/"
          className="font-medium transition-colors hover:opacity-80"
          style={{ color: 'var(--primary-color)' }}
        >
          ← Back to all posts
        </a>
      </div>
    </article>
  );
}
