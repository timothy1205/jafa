import { useContext } from "react";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";
import { handleError, logout } from "../../../services/api";
import { generateToast } from "../../../services/utils";
import { UserContext } from "../../../providers/UserProvider";

function LogoutButton() {
  const { setUser } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (e) {
      handleError(e);
    }

    setUser({ loaded: true, user: null });
    navigate("/");
    generateToast("Logged out", "success");
  };

  return <Button onClick={handleLogout}>Logout</Button>;
}

export default LogoutButton;
