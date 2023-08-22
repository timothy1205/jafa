import React from "react";
import Button from "@mui/material/Button";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import "./index.css";

export default function PostVote() {
  return (
    <div className="postvote">
      <Button>
        <ArrowUpwardIcon className="postvote-upvote"></ArrowUpwardIcon>
      </Button>
      <Button>
        <ArrowDownwardIcon className="postvote-downvote"></ArrowDownwardIcon>
      </Button>
    </div>
  );
}
