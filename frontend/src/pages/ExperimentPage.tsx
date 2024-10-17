import React from "react";
import { useState } from "react";
import Counter from "../components/Counter";

export default function ExperimentPage() {
  const [count, setCount] = useState(0);
  const [title, setTitle] = useState("Counter");

  // Have a list of table rows and just display with a map
  // Create a counter row at the bottom

  // How to get audio + video data?

  return (
    <div>
      <h1>ExperimentPage</h1>
      <Counter title={title} count={count} setCount={setCount} />
    </div>
  );
}
