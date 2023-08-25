import { PropsWithChildren, createContext, useMemo, useState } from "react";

interface User {
  username: string;
  registration_date: string;
}

export type UserData = User | null;

interface UserContextData {
  user: UserData;
  setUser: React.Dispatch<React.SetStateAction<UserData>>;
}

// Should never be null when used, force TS to ignore it
export const UserContext = createContext<UserContextData>(null!);

export default function UserProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<UserData>(null);

  const cachedContextData = useMemo<UserContextData>(
    () => ({ user, setUser }),
    [user, setUser]
  );
  return (
    <UserContext.Provider value={cachedContextData}>
      {children}
    </UserContext.Provider>
  );
}
