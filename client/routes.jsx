import React from "react";
import App from "./src/App";
import Home from "./src/pages/Home";
import SongPage from "./src/pages/SongPage";
import ChordPage from "./src/pages/ChordPage";
import SearchPage from "./src/pages/SearchPage";
import GenrePage from "./src/pages/GenrePage";
import NotFound from "./src/pages/NotFound";

const router = [
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "songs",
        children: [
          {
            index: true,
            element: <Home />, // Redirect to home for now
          },
          {
            path: ":songId",
            element: <SongPage />,
          }
        ]
      },
      {
        path: "chords",
        children: [
          {
            index: true,
            element: <Home />, // Redirect to home for now
          },
          {
            path: ":chordName",
            element: <ChordPage />,
          }
        ]
      },
      {
        path: "search",
        element: <SearchPage />,
      },
      {
        path: "genre/:genreName",
        element: <GenrePage />,
      },
      {
        path: "*",
        element: <NotFound />,
      }
    ],
  },
];

export default router;