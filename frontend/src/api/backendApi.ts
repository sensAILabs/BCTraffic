import { DataLogEntry } from "../types/DataLogEntry";
import { SettingsObj } from "../types/SettingsObj";

function get_data(): any {}

async function create_experiment_post(settings: SettingsObj): Promise<any> {
  fetch("http://localhost:5000/experiment", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(settings),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Create experiment failed");
      }
      return response.json();
    })
    .then((data) => console.log("Success:", data))
    .catch((error) => console.error("Error:", error));
}

async function add_experiment_row_post(
  data: DataLogEntry,
  row: number
): Promise<any> {
  fetch(`http://localhost:5000/experiment/${row}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Add experiment row failed");
      }
      return response.json();
    })
    .then((data) => console.log("Success:", data))
    .catch((error) => console.error("Error:", error));
}

// Get for root

// {
//     "experiment_name": "string",
//     "creator_name": "string",
//     "sampling_rate": 0,
//     "comment": 0,
//     "sender_type": "pc"
//   }
// Get response to determine experiment_id

// {
//     "latitude": 0,
//     "longitude": 0,
//     "allowed_speed": 0,
//     "current_speed": 0,
//     "temperature": 0,
//     "humidity": 0,
//     "start_time": 0,
//     "end_time": 0,
//     "counters": [
//       {
//         "counter_type": "gasoline",
//         "count": 0
//       }
//     ],
//     "record_file": "string"
//   }
