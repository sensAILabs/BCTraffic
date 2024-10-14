import React from "react";
import { useState } from "react";
import Counter from "../components/Counter";

export default function ExperimentPage() {
  const [count, setCount] = useState(0);
  const [title, setTitle] = useState("Counter");

  return (
    <div>
      <h1>ExperimentPage</h1>
      <Counter title={title} count={count} setCount={setCount} />
    </div>
  );
}
