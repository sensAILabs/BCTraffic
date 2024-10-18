import React, { useEffect } from "react";
import { useState } from "react";
import Counter from "../components/Counter";

import { DataLogEntry } from "../types/DataLogEntry";
import { SettingsObj } from "../types/SettingsObj";

enum VehicleType {
  Car = "Car",
  Truck = "Truck",
  Bus = "Bus",
  Motorcycle = "Motorcycle",
  Van = "Van",
  Tractor = "Tractor",
}

interface ExperimentPageProps {
  settingsObj?: SettingsObj;
}

export default function ExperimentPage({ settingsObj }: ExperimentPageProps) {
  // TODO: stop and break if settingsObj is undefined

  const [dataLog, setDataLog] = useState<DataLogEntry[]>([]);

  // TODO: How to get allowed speed and current speed?

  // Weather API states
  const [temperature, setTemperature] = useState<number>(-1000);
  const [humidity, setHumidity] = useState<number>(-1000);

  // TODO: audio file

  // Counters
  const [carCount, setCarCount] = useState(0);
  const [truckCount, setTruckCount] = useState(0);
  const [vanCount, setVanCount] = useState(0);
  const [busCount, setBusCount] = useState(0);
  const [tractorCount, setTractorCount] = useState(0);
  const [motorcycleCount, setMotorcycleCount] = useState(0);

  // Have a list of table rows and just display with a map
  // Create a counter row at the bottom

  // How to get audio + video data?

  // Set interval
  useEffect(() => {
    const timestamp: string = new Date().toISOString();
    const latitude = 0;
    const longitude = 0;

    const newEntry: DataLogEntry = {
      start_timestamp: timestamp,
      end_timestamp: timestamp,
      latitude: latitude,
      longitude: longitude,
      allowed_speed: 0,
      current_speed: 0,
      temperature: temperature,
      humidity: humidity,
      record_file: "",
      counters: [
        { counter_type: "Cars", count: carCount },
        { counter_type: "Trucks", count: truckCount },
        { counter_type: "Vans", count: vanCount },
        { counter_type: "Buses", count: busCount },
        { counter_type: "Tractors", count: tractorCount },
        { counter_type: "Motorcycles", count: motorcycleCount },
      ],
    };

    setDataLog((prevDataLog: DataLogEntry[]) => [...prevDataLog, newEntry]);
  });

  return (
    <div>
      <h1>ExperimentPage</h1>
      <div>{/* Make map of table row components */}</div>

      <div>
        <Counter title={"Car"} count={carCount} setCount={setCarCount} />
        <Counter title={"Truck"} count={truckCount} setCount={setTruckCount} />
        <Counter title={"Van"} count={vanCount} setCount={setVanCount} />
        <Counter title={"Bus"} count={busCount} setCount={setBusCount} />
        <Counter
          title={"Tractor"}
          count={tractorCount}
          setCount={setTractorCount}
        />
        <Counter
          title={"Motorcycle"}
          count={motorcycleCount}
          setCount={setMotorcycleCount}
        />
      </div>
    </div>
  );
}
