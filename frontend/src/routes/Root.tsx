import { useEffect, useState } from "react";
import PostList from "../components/posts/PostList";
import { getRoot, handleError } from "../services/api";
import { PostData } from "../components/posts/PostCard";
import { LoaderFunctionArgs, useLoaderData } from "react-router-dom";

interface RootRouteData {
  info: {
    current_page: number;
    page_count: number;
    post_count: number;
  };
  posts: Array<PostData>;
}

export function rootLoader({ params }: LoaderFunctionArgs) {
  let page = undefined;

  if (params.page) {
    page = parseInt(params.page);
  }

  return { page };
}

function Root() {
  const { page } = useLoaderData() as { page?: number };
  const [rootData, setRootData] = useState<RootRouteData>();

  useEffect(() => {
    const getPostList = async () => {
      try {
        const res = await getRoot(page);
        setRootData(res.data);
        console.log(res)
      } catch (e) {
        handleError(e);
      }
    };

    getPostList();
  }, []);

  return <PostList posts={rootData?.posts} />;
}

export default Root;
