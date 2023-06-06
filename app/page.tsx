import { allPosts } from "@/.contentlayer/generated"
import Link from "next/link"

export default function Home() {
  return (
    <div className="prose dark:prose-invert">
      {allPosts.map((post) => (
        <article key={post._id}>
          <Link href={post.slug} className="text-[#ec3750]">
            <h2 className="mb-2">{post.title}</h2>
          </Link>
          {post.description && <p className="mt-2">{post.description}</p>}
        </article>
      ))}
    </div>
  )
}
