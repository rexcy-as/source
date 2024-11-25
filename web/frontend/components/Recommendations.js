const Recommendations = ({ sections }) => {
    return (
      <div className="bg-white shadow-md rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-800 mb-4">
          Pilihan Rekomendasi:
        </h3>
        <ul className="space-y-3">
          {sections.map((section) => (
            <li
              key={section.id}
              className="flex justify-between items-center bg-gray-100 p-4 rounded-lg shadow-sm"
            >
              <span>No. Section {section.id}</span>
              <span>Harga: ${section.price}</span>
              <span>Seat Tersedia: {section.seats}</span>
            </li>
          ))}
        </ul>
      </div>
    );
  };
  
  export default Recommendations;
  