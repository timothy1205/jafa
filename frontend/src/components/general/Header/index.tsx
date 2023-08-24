import React from "react";
import { Link } from "react-router-dom";
import "./index.css";
import UsernameLogin from "../UsernameLogin";

export default function Header() {
  return (
    <div id="header">
      <Link to="/" id="header-title">
        Jafa
      </Link>
      <UsernameLogin />
    </div>
  );
}
