import { toast, TypeOptions } from "react-toastify";
import { UserContext, User } from "../providers/UserProvider";
import { useContext, useEffect } from "react";
import { getCurrentUser } from "./api";

export function generateToast(msg: string, type: TypeOptions) {
  toast(msg, {
    position: toast.POSITION.BOTTOM_CENTER,
    type: type,
  });
}

export function useExposedUserUpdater() {
  const { setUser, userState } = useContext(UserContext);

  const updateUser = async (force = true) => {
    // Skip if we're already logged in
    if (userState.loaded && !force) return;

    const userRes = await getCurrentUser();
    const userData = userRes.data as User;

    if (!userData || Object.keys(userData).length === 0) {
      setUser({ loaded: true, user: null });
      return;
    }

    setUser({ loaded: true, user: userData });
  };

  return updateUser;
}

export function useUserUpdater() {
  const updateUser = useExposedUserUpdater();

  useEffect(() => {
    updateUser(false);
    // Check user once on startup
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
}
