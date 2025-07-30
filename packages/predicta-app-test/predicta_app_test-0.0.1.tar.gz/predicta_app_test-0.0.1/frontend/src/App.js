import React, { useState } from "react";
import "./App.css";

function App() {
  const [data, setData] = useState([]);

  const fetchData = () => {
    fetch("/message")  // Replace with full URL if needed
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("Error fetching data:", err));
  };

  return (
    <div className="App">
      <h1>React + FastAPI Demo</h1>
      <button onClick={fetchData}>Fetch Data</button>

      {data.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>x</th>
              <th>y</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i}>
                <td>{row.x}</td>
                <td>{row.y}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
