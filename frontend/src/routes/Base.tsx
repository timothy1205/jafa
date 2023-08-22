import { Outlet } from "react-router-dom";
import Header from "../components/general/Header";
import Providers from "../providers/Providers";

function Base() {
  return (
    <Providers>
      <Header />
      <Outlet />
    </Providers>
  );
}

export default Base;
