import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Experimental_CssVarsProvider as CssVarsProvider } from "@mui/material/styles";
import Base from "./routes/Base";
import Root, { rootLoader } from "./routes/Root";
import Subforum, { subforumLoader } from "./routes/Subforum";
import reportWebVitals from "./reportWebVitals";
import Login from "./routes/Login";
import SubmitSubforum from "./routes/Submit/SubmitSubforum";
import SubmitPost from "./routes/Submit/SubmitPost";
import "./index.css";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

const router = createBrowserRouter([
  {
    element: <Base />,
    children: [
      {
        path: "/:page?",
        element: <Root />,
        loader: rootLoader,
      },
      {
        path: "subforum/:subforum?/:page?",
        element: <Subforum />,
        loader: subforumLoader,
      },
      {
        path: "login",
        element: <Login />,
      },
      {
        path: "submit/subforum",
        element: <SubmitSubforum />,
      },
      {
        path: "submit/post",
        element: <SubmitPost />,
      },
    ],
  },
]);

root.render(
  <React.StrictMode>
    <CssVarsProvider>
      <RouterProvider router={router} />
      <ToastContainer limit={5} theme="dark" />
    </CssVarsProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
