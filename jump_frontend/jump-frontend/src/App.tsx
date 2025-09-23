import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios';

interface HistoryItem {
  date: string;
  index_text: string;
  index_value: string;
  created_at: string;
}

function App() {
  const [date, setDate] = useState("");
  const [history, setHistory] = useState<HistoryItem[]>([]);

  const fetchHistory = async () => { 
    const response = await axios.get("http://localhost:8000/history");
    setHistory(response.data);
  }

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    if(!date) return;
    await axios.get(`http://localhost:8000/carbon/${date}`);
    fetchHistory();
  }

  useEffect(() => {
    fetchHistory();
  }, []);



  return (
    <>
      <div>
        <h2>caron intensity lookup</h2>
        <form onSubmit={handleSubmit}>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          <button type='submit'>Submit</button>
        </form>
        <h3>history</h3>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Index</th>
              <th>Value</th>
              <th>Checked</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h, i) => (
              <tr key={i}>
                <td>{h.date}</td>
                <td>{h.index_text}</td>
                <td>{h.index_value}</td>
                <td>{h.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

export default App
