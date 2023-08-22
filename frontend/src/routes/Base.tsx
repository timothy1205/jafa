import { Outlet } from "react-router-dom";
import Header from "../components/general/Header";

function Base() {
  return (
    <>
      <Header />
      <Outlet />
    </>
  );
}

export default Base;
