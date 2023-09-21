import { useContext } from "react";
import { UserContext } from "../../../providers/UserProvider";
import { useUserUpdater } from "../../../services/utils";
import LoginButton from "../../login/LoginButton";
import LogoutButton from "../../login/LogoutButton";
import "./index.css";
import CreateDropdown from "../CreateDropdown";

interface LoggedInAreaProps {
  username: string;
}

function LoggedInArea({ username }: LoggedInAreaProps) {
  return (
    <>
      <CreateDropdown />
      <p className="usernamelogin-username">{username}</p>
    </>
  );
}

export default function UserArea() {
  const { userState } = useContext(UserContext);

  useUserUpdater();

  let loggedInArea = <></>;
  let button;
  if (userState.loaded && userState.user !== null) {
    // Logged in
    loggedInArea = <LoggedInArea username={userState.user.username} />;
    button = <LogoutButton />;
  } else {
    // Logged out
    button = <LoginButton />;
  }

  return (
    <div className="userarea">
      {loggedInArea}
      {button}
    </div>
  );
}
