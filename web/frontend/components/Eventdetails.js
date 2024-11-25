const EventDetails = ({ name, date, totalSections, totalSeats }) => {
    return (
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-800">
          Event: <span className="text-green-600">{name}</span>
        </h2>
        <p className="text-gray-600">
          Diselenggarakan pada: <span className="font-medium">{date}</span>
        </p>
        <p className="text-gray-600">
          Jumlah Section & Seat Tersedia:{" "}
          <span className="font-medium">
            {totalSections} Section, {totalSeats} Seat
          </span>
        </p>
      </div>
    );
  };
  
  export default EventDetails;
  