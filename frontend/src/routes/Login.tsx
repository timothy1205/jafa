import { useContext } from "react";
import { Navigate } from "react-router-dom";
import LoginRegister from "../components/login/LoginRegister";
import { UserContext } from "../providers/UserProvider";

function Login() {
  const { userState } = useContext(UserContext);

  if (userState.user !== null) return <Navigate to="/" replace={true} />;

  return <LoginRegister />;
}

export default Login;
