import React, { useEffect, useState } from "react";
import api from "../../../services/api";
import PostCard, { PostData } from "../PostCard";

interface PostListProps {
  subforum?: string;
}

export default function PostList({ subforum }: PostListProps) {
  const [posts, setPosts] = useState<Array<PostData>>([]);

  useEffect(() => {
    const getPostList = async () => {
      try {
        const res = await api.postList(subforum);
        setPosts(res.data);
      } catch (e) {
        console.error(e);
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
