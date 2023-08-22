import React, { useEffect, useState } from "react";
import { postList, handleError } from "../../../services/api";
import PostCard, { PostData } from "../PostCard";

interface PostListProps {
  subforum?: string;
}

export default function PostList({ subforum }: PostListProps) {
  const [posts, setPosts] = useState<Array<PostData>>([]);

  useEffect(() => {
    const getPostList = async () => {
      try {
        const res = await postList(subforum);
        setPosts(res.data);
      } catch (e) {
        handleError(e);
      }
    };

    getPostList();
  }, [subforum]);

  return (
    <>
      {posts.map((post) => (
        <PostCard data={post} key={post.post_id}></PostCard>
      ))}
    </>
  );
}
