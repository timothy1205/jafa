import { LoaderFunctionArgs, useLoaderData, redirect } from "react-router-dom";
import PostList from "../components/posts/PostList";

export function subforumLoader({ params }: LoaderFunctionArgs) {
  const subforum = params.subforum;
  if (!subforum) {
    return redirect("/");
  }

  return { subforum };
}

interface SubforumData {
  subforum: string;
}
function Subforum() {
  const { subforum } = useLoaderData() as SubforumData;

  return <PostList subforum={subforum} />;
}

export default Subforum;
