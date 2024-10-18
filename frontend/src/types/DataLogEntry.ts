import { Count } from "./Count";

export interface DataLogEntry {
  start_timestamp: string;
  end_timestamp: string;
  latitude: number;
  longitude: number;
  allowed_speed: number;
  current_speed: number;
  temperature: number;
  humidity: number;
  record_file: string;
  counters: Count[];
}
