import React from "react";
import { useState } from "react";
import { Button } from "antd";
import { DownOutlined, UpOutlined } from "@ant-design/icons";

interface CounterProps {
  title: string;
  count: number;
  setCount: (count: number) => void;
}

export default function Counter({ title, count, setCount }: CounterProps) {
  const increment = () => setCount(count + 1);
  const decrement = () => {
    if (count > 0) {
      setCount(count - 1);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-4 m-4 bg-slate-200 rounded-lg max-w-96">
      <h1 className="text-2xl font-bold mb-2">{title}</h1>
      <Button type="primary" onClick={() => increment()}>
        <UpOutlined />
      </Button>
      <div className="p-2 px-6 mt-2 mb-2 rounded-lg bg-blue-200 font-bold">
        {count}
      </div>
      <Button type="primary" onClick={() => decrement()}>
        <DownOutlined />
      </Button>
    </div>
  );
}
