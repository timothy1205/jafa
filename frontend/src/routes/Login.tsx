import { useContext } from "react";
import { Navigate } from "react-router-dom";
import LoginRegister from "../components/login/LoginRegister";
import { UserContext } from "../providers/UserProvider";

function Login() {
  const { user } = useContext(UserContext);

  if (user !== null) return <Navigate to="/" replace={true} />;

  return <LoginRegister />;
}

export default Login;
