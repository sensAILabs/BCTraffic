import { DataLogEntry } from "../types/DataLogEntry";
import { SettingsObj } from "../types/SettingsObj";

function get_data(): any {}

function create_experiment_post(settings: SettingsObj): any {}

function add_experiment_row_post(data: DataLogEntry): any {}

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
