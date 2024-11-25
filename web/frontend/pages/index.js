// /web/frontend/pages/index.js

import { useState } from 'react';

const Home = () => {
  const [url, setUrl] = useState('');
  const [scrapedData, setScrapedData] = useState(null);

  const handleScrape = async () => {
    const response = await fetch('http://localhost:8000/api/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    const data = await response.json();
    setScrapedData(data);
  };

  return (
    <div>
      <h1>Scrape Event Data</h1>
      <input 
        type="text" 
        placeholder="Enter event URL" 
        value={url} 
        onChange={(e) => setUrl(e.target.value)} 
      />
      <button onClick={handleScrape}>Scrape Data</button>

      {scrapedData && (
        <div>
          <h2>{scrapedData.event_name}</h2>
          <ul>
            {scrapedData.tickets.map((ticket, index) => (
              <li key={index}>{ticket}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Home;
