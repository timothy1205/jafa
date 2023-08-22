import React from "react";
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

export default function PostCard({ data }: PostCardProps) {
  return (
    <div className="postcard">
      <PostVote post_id={data.post_id} />
      <a href={`/post/${data.post_id}`} className="postcard-content">
        <div className="postcard-info">
          <a href={`/subforum/${data.subforum}`} className="postcard-subforum">
            {data.subforum}
          </a>
          <p className="postcard-creation">{data.creation_date}</p>
        </div>
        <h3 className="postcard-title">{data.title}</h3>
        <p className="postcard-body">{data.body}</p>
      </a>
    </div>
  );
}
