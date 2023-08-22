import React from "react";
import "./index.css";
import UsernameLogin from "../UsernameLogin";

export default function Header() {
  return (
    <div id="header">
      <a href="/" id="header-title">
        Jafa
      </a>
      <UsernameLogin />
    </div>
  );
}
