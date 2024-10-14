import React from "react";
import logo from "./logo.svg";
import Counter from "./components/Counter";
import { useState } from "react";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <Counter title="Automiasdasd" count={count} setCount={setCount} />
    </div>
  );
}

export default App;
