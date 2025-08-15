import React from "react";
import App from "./src/App";
import Home from "./src/pages/Home";


const router = [
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element: <Home />,
      }
    ],
  },
];

export default router;