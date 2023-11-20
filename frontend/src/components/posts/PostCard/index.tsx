import React from "react";
import { Link } from "react-router-dom";
import "./index.css";
import PostVote from "../PostVote";

export interface PostData {
  body: string;
  creation_date: string;
  dislikes: number;
  likes: number;
  locked: boolean;
  media?: Array<string>;
  modified_date?: string;
  op: string;
  post_id: string;
  subforum: string;
  tags?: Array<string>;
  title: string;
}

interface PostCardProps {
  data: PostData;
}

export default function PostCard({ data }: Readonly<PostCardProps>) {
  return (
    <div className="postcard">
      <PostVote post_id={data.post_id} />
      <div className="postcard-content">
        <div className="postcard-info">
          <Link to={`/subforum/${data.subforum}`} className="postcard-subforum">
            {data.subforum}
          </Link>
          <p className="postcard-creation">{data.creation_date}</p>
        </div>
        <Link to={`/post/${data.post_id}`} className="postcard-title">
          {data.title}
        </Link>
        <p className="postcard-body">{data.body}</p>
      </div>
    </div>
  );
}
