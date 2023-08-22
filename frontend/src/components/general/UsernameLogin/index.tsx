import React, { useContext } from "react";
import { Link } from "react-router-dom";
import "./index.css";
import { UserContext } from "../../../providers/UserProvider";

export default function UsernameLogin() {
  const { user } = useContext(UserContext);

  let toRender;
  if (user === null) {
    toRender = (
      <Link className="usernamelogin-link" to="/login">
        Login
      </Link>
    );
  } else {
    toRender = <p className="usernamelogin-username">{user.username}</p>;
  }

  return <div className="usernamelogin">{toRender}</div>;
}
