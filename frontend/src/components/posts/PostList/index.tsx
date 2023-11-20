import PostCard, { PostData } from "../PostCard";
import "./index.css";

interface PostListProps {
  posts?: Array<PostData>;
}

export default function PostList({ posts }: Readonly<PostListProps>) {
  if (posts && posts.length > 0) {
    return (
      <>
        {posts.map((post) => (
          <PostCard data={post} key={post.post_id}></PostCard>
        ))}
      </>
    );
  } else {
    return <h1>No posts found...</h1>;
  }
}
