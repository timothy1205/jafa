import React from "react";
import Button from "@mui/material/Button";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import "./index.css";
import { vote, handleError, APIResponse } from "../../../services/api";
import { generateToast } from "../../../services/utils";

interface PostVoteProps {
  post_id: string;
}

export default function PostVote({ post_id }: PostVoteProps) {
  async function voteAction(is_like: boolean) {
    try {
      const res = await vote(post_id, is_like);
      const data = res.data as APIResponse;
      if (data.msg === "Post vote ackowledged") {
        const like = is_like ? "Like" : "Dislike";
        generateToast(`${like} received`, "success");
      }
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
