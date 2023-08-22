import React from "react";
import Button from "@mui/material/Button";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import "./index.css";
import { vote, handleError } from "../../../services/api";

interface PostVoteProps {
  post_id: string;
}

export default function PostVote({ post_id }: PostVoteProps) {
  async function voteAction(is_like: boolean) {
    try {
      await vote(post_id, is_like);
    } catch (e) {
      handleError(e);
    }
  }

  return (
    <div className="postvote">
      <Button onClick={() => voteAction(true)}>
        <ArrowUpwardIcon className="postvote-upvote"></ArrowUpwardIcon>
      </Button>
      <Button onClick={() => voteAction(false)}>
        <ArrowDownwardIcon className="postvote-downvote"></ArrowDownwardIcon>
      </Button>
    </div>
  );
}
