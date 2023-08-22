import { PropsWithChildren } from "react";
import UserProvider from "./UserProvider";

export default function Providers({ children }: PropsWithChildren) {
  return <UserProvider>{children}</UserProvider>;
}
