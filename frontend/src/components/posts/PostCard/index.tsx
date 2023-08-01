import React from "react";
import Button from "@mui/material/Button";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import "./index.css";

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
      <div className="postcard-vote">
        <Button>
          <ArrowUpwardIcon className="postcard-upvote"></ArrowUpwardIcon>
        </Button>
        <Button>
          <ArrowDownwardIcon className="postcard-downvote"></ArrowDownwardIcon>
        </Button>
      </div>
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
