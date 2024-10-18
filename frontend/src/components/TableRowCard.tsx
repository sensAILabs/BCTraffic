interface TableRowCardProps {
  title: string;
  start_time: string;
  end_time: string;
  duration: string;
  location: string;
  bus_vals: number;
  truck_vals: number;
  van_vals: number;
  car_vals: number;
  tractor_vals: number;
  motorcycle_vals: number;
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
    <div className="bg-white shadow-md rounded-lg p-6 space-y-4">
      <h1 className="text-xl font-bold">{title}</h1>

      <div className="grid grid-cols-2 gap-4">
        {/* Start Time */}
        <div>
          <label className="block text-gray-600">Start Time</label>
          <p className="text-lg">{start_time}</p>
        </div>

        {/* End Time */}
        <div>
          <label className="block text-gray-600">End Time</label>
          <p className="text-lg">{end_time}</p>
        </div>

        {/* Duration */}
        <div>
          <label className="block text-gray-600">Duration</label>
          <p className="text-lg">{duration}</p>
        </div>

        {/* Location */}
        <div>
          <label className="block text-gray-600">Location</label>
          <p className="text-lg">{location}</p>
        </div>

        {/* Cars */}
        <div>
          <label className="block text-gray-600">Cars</label>
          <p className="text-lg">{car_vals}</p>
        </div>

        {/* Buses */}
        <div>
          <label className="block text-gray-600">Buses</label>
          <p className="text-lg">{bus_vals}</p>
        </div>

        {/* Trucks */}
        <div>
          <label className="block text-gray-600">Trucks</label>
          <p className="text-lg">{truck_vals}</p>
        </div>

        {/* Vans */}
        <div>
          <label className="block text-gray-600">Vans</label>
          <p className="text-lg">{van_vals}</p>
        </div>

        {/* Tractors */}
        <div>
          <label className="block text-gray-600">Tractors</label>
          <p className="text-lg">{tractor_vals}</p>
        </div>

        {/* Motorcycles */}
        <div>
          <label className="block text-gray-600">Motorcycles</label>
          <p className="text-lg">{motorcycle_vals}</p>
        </div>
      </div>
    </div>
  );
}
