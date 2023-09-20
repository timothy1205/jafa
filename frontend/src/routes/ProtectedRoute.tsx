import { PropsWithChildren, useContext, useEffect } from "react";
import { UserContext } from "../providers/UserProvider";
import { useNavigate } from "react-router-dom";

function ProtectedRoute({ children }: PropsWithChildren) {
  const { userState } = useContext(UserContext);
  const navigate = useNavigate();
  useEffect(() => {
    if (userState.loaded && userState.user === null)
      navigate("/login", { replace: true });
  });

  return <>{userState.loaded ? children : <></>}</>;
}

export default ProtectedRoute;
