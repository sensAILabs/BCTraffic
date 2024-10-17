import React from "react";

interface TableRowCardProps {
  title: string;
  start_time: string;
  end_time: string;
  duration: string;
  location: string;
  bus_vals: Number;
  truck_vals: Number;
  van_vals: Number;
  car_vals: Number;
  tractor_vals: Number;
  motorcycle_vals: Number;
}

export default function TableRowCard({
  title,
  start_time,
  end_time,
  duration,
  location,
  bus_vals,
  truck_vals,
  van_vals,
  car_vals,
  tractor_vals,
  motorcycle_vals,
}: TableRowCardProps) {
  return (
    <div>
      <h1>{title}</h1>
      <p>Start Time: {start_time}</p>
      <p>End Time: {end_time}</p>
      <p>Duration: {duration}</p>
      <p>Location: {location}</p>
      <p>Counter Vals: {JSON.stringify(counter_vals)}</p>
    </div>
  );
}
