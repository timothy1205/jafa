import { toast, TypeOptions } from "react-toastify";
import { UserContext, UserData } from "../providers/UserProvider";
import { useContext, useEffect } from "react";
import { getCurrentUser } from "./api";

export function generateToast(msg: string, type: TypeOptions) {
  toast(msg, {
    position: toast.POSITION.BOTTOM_CENTER,
    type: type,
  });
}

export function useExposedUserUpdater() {
  const { setUser, user } = useContext(UserContext);

  const updateUser = async () => {
    // Skip if we're already logged in
    if (user !== null) return;

    const userRes = await getCurrentUser();
    const userData = userRes.data as UserData;
    setUser(userData);
  };

  return updateUser;
}

export function useUserUpdater() {
  const updateUser = useExposedUserUpdater();

  useEffect(() => {
    updateUser();
    // Check user once on startup
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
}
