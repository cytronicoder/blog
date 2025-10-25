import { getAllPosts } from '@/lib/posts';
import Link from 'next/link';
import { format } from 'date-fns';
import CuriosityQuote from '@/components/CuriosityQuote';

export default function Home() {
  const posts = getAllPosts();

  return (
    <div className="space-y-8">
      <div className="mb-12">
        <h1 className="text-4xl font-bold mb-4" style={{ color: 'var(--text-color)' }}>
          I write about thoughts, stories, and ideas.
        </h1>
        <CuriosityQuote />
      </div>

      <div className="space-y-8">
        {posts.length === 0 ? (
          <p style={{ color: 'var(--text-color)', opacity: 0.7 }}>No posts yet. Create your first post in the <code className="px-2 py-1 rounded" style={{ background: 'var(--foreground)' }}>posts</code> directory!</p>
        ) : (
          posts.map((post) => (
            <article key={post.slug} className="pb-8 last:border-0">
              <Link href={`/posts/${post.slug}`} className="group">
                <h2 className="text-2xl font-bold mb-2 transition-colors" style={{ color: 'var(--text-color)' }}>
                  {post.title}
                </h2>
              </Link>
              <p className="text-sm mb-3" style={{ color: 'var(--text-color)', opacity: 0.6 }}>
                {format(new Date(post.date), 'MMMM dd, yyyy')}
              </p>
              <p className="mb-3" style={{ color: 'var(--text-color)', opacity: 0.8 }}>
                {post.excerpt}
              </p>
              <Link
                href={`/posts/${post.slug}`}
                className="font-medium transition-colors hover:opacity-80"
                style={{ color: 'var(--primary-color)' }}
              >
                Read more →
              </Link>
            </article>
          ))
        )}
      </div>
    </div>
  );
}
