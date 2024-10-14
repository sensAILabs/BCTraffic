import React from "react";

interface SetupPageProps {
  setSettingsObj: (settingsObj: any) => void;
}

export default function SetupPage({ setSettingsObj }: SetupPageProps) {
  return (
    <div>
      <h1>SetupPage</h1>
    </div>
  );
}
