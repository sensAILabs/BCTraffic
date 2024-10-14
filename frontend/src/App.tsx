import React from "react";
import { useState } from "react";
import { Routes, Route } from "react-router-dom";

import SetupPage from "./pages/SetupPage";
import ExperimentPage from "./pages/ExperimentPage";
import ErrorPage from "./pages/ErrorPage";

function App() {
  const [settingsObj, setSettingsObj] = useState({});

  return (
    <Routes>
      <Route path="/" element={<SetupPage setSettingsObj={setSettingsObj} />} />
      <Route path="/experiment" element={<ExperimentPage />} />
      <Route path="*" element={<ErrorPage />} />
    </Routes>
  );
}

export default App;
