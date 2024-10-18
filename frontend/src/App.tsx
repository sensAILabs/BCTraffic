import React from "react";
import { useState } from "react";
import { Routes, Route } from "react-router-dom";

import SetupPage from "./pages/SetupPage";
import ExperimentPage from "./pages/ExperimentPage";
import ErrorPage from "./pages/ErrorPage";

import { SettingsObj } from "./types/SettingsObj";

function App() {
  const [settingsObj, setSettingsObj] = useState<SettingsObj | undefined>(
    undefined
  );

  return (
    <Routes>
      <Route path="/" element={<SetupPage setSettingsObj={setSettingsObj} />} />
      <Route
        path="/experiment"
        element={<ExperimentPage settingsObj={settingsObj} />}
      />
      <Route path="*" element={<ErrorPage />} />
    </Routes>
  );
}

export default App;
