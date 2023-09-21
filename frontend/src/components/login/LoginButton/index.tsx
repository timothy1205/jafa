import { Link } from "react-router-dom";
import "./index.css";

function LoginButton() {
  return (
    <Link className="loginbutton" to="/login">
      Login
    </Link>
  );
}

export default LoginButton;
