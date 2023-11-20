import { LoaderFunctionArgs, useLoaderData, redirect } from "react-router-dom";
import PostList from "../components/posts/PostList";
import { useState, useEffect } from "react";
import { PostData } from "../components/posts/PostCard";
import { getSubform, handleError } from "../services/api";

interface SubforumRouteData {
  info: {
    current_page: number;
    page_count: number;
    post_count: number;
    creator: string;
    title: string;
    description: string;
    creation_date: Date;
  };
  posts: Array<PostData>;
}

export function subforumLoader({ params }: LoaderFunctionArgs) {
  const subforum = params.subforum;
  let page = undefined;

  if (!subforum) {
    return redirect("/");
  }

  if (params.page) {
    page = parseInt(params.page);
  }

  return { subforum, page };
}

function Subforum() {
  const { subforum, page } = useLoaderData() as {
    subforum: string;
    page?: number;
  };
  const [subforumData, setSubforumData] = useState<SubforumRouteData>();

  useEffect(() => {
    const getPostList = async () => {
      try {
        const res = await getSubform(subforum, page);
        setSubforumData(res.data);
      } catch (e) {
        handleError(e);
      }
    };

    getPostList();
  }, []);

  return <PostList posts={subforumData?.posts} />;
}

export default Subforum;
