import { PropsWithChildren, createContext, useMemo, useState } from "react";

interface Loaded {
  loaded: boolean;
}

export interface User {
  username: string;
  registration_date: string;
}

interface UserState {
  loaded: boolean;
  user: User | null;
}

interface UserContextData {
  userState: UserState;
  setUser: React.Dispatch<React.SetStateAction<UserState>>;
}

// Should never be null when used, force TS to ignore it
export const UserContext = createContext<UserContextData>(null!);

export default function UserProvider({ children }: PropsWithChildren) {
  const [userState, setUser] = useState<UserState>({
    user: null,
    loaded: false,
  });

  const cachedContextData = useMemo<UserContextData>(
    () => ({ userState, setUser }),
    [userState, setUser]
  );
  return (
    <UserContext.Provider value={cachedContextData}>
      {children}
    </UserContext.Provider>
  );
}
