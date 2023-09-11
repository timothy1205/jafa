import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { UserContext } from "../../../providers/UserProvider";
import { Button } from "@mui/material";
import { generateToast, useUserUpdater } from "../../../services/utils";
import { handleError, logout } from "../../../services/api";
import "./index.css";

export default function UsernameLogin() {
  const { user, setUser } = useContext(UserContext);
  const navigate = useNavigate();

  useUserUpdater();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (e) {
      handleError(e);
    }

    setUser(null);
    navigate("/");
    generateToast("Logged out", "success");
  };

  let toRender;
  if (user === null) {
    toRender = (
      <Link className="usernamelogin-link" to="/login">
        Login
      </Link>
    );
  } else {
    toRender = (
      <>
        <p className="usernamelogin-username">{user.username}</p>
        <Button onClick={handleLogout}>Logout</Button>
      </>
    );
  }

  return <div className="usernamelogin">{toRender}</div>;
}
