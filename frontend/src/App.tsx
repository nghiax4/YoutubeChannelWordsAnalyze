import { useState, useEffect } from "react"
import axios from 'axios'

function App() {
  // State variables to hold the statistics
  const [numDifferentWords, setNumDifferentWords] = useState(0);
  const [totalWordsSpoken, setTotalWordsSpoken] = useState(0);
  const [wpmOverYear, setWpmOverYear] = useState([]);
  const [wpmVsViews, setWpmVsViews] = useState([]);
  const [sentimentOverYear, setSentimentOverYear] = useState([]);

  // Fetch statistics from the backend when the component mounts
  useEffect(() => {
    fetchStatistics();
  }, []);

  // Function to fetch statistics from the backend
  const fetchStatistics = async () => {
    try {
      const response = await axios.get('/api/statistics');
      const data = response.data;

      // Example data structure:
      // data = {
      //   numDifferentWords: 1000,
      //   totalWordsSpoken: 50000,
      //   wpmOverYear: [{ year: 2020, wpm: 120 }, { year: 2021, wpm: 130 }],
      //   wpmVsViews: [{ year: 2020, wpm: 120, views: 1000 }, { year: 2021, wpm: 130, views: 1500 }],
      //   sentimentOverYear: [{ year: 2020, sentiment: 0.5 }, { year: 2021, sentiment: 0.6 }]
      // }

      setNumDifferentWords(data.numDifferentWords);
      setTotalWordsSpoken(data.totalWordsSpoken);
      setWpmOverYear(data.wpmOverYear);
      setWpmVsViews(data.wpmVsViews);
      setSentimentOverYear(data.sentimentOverYear);
    } catch (error) {
      console.error("Error fetching statistics:", error);
    }
  };

  return (
    <>
      <div>
        <h1>YouTube Channel Statistics</h1>
        <p>Number of different words ever spoken: {numDifferentWords}</p>
        <p>Total words spoken: {totalWordsSpoken}</p>
        {/* Placeholder for graphs */}
        <div>Graphs will be displayed here</div>
      </div>
    </>
  )
}

export default App
