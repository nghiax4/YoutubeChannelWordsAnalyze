import { useState } from "react";
import axios from "axios";
import "./App.css";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, Cell } from "recharts";

function parseYearWpmViewsData(yearAndWpmAndViews) {
  return yearAndWpmAndViews.map((item, index) => ({
    year: item[0],
    wpm: item[1],
    views: item[2],
  }));
}

function averageWpmEachYear(yearAndWpmAndViews) {
  const yearToWpmStats = {};

  for (const item of yearAndWpmAndViews) {
    const year = item.year;
    const wpm = item.wpm;

    if (!yearToWpmStats[year]) {
      yearToWpmStats[year] = { reciprocalSum: 0, count: 0 };
    }

    yearToWpmStats[year].reciprocalSum += 1 / wpm;
    yearToWpmStats[year].count += 1;
  }

  const result = [];
  for (const year in yearToWpmStats) {
    result.push({
      year: parseInt(year),
      avgWpm: yearToWpmStats[year].count / yearToWpmStats[year].reciprocalSum,
    });
  }

  return result;
}

function App() {
  const [channelId, setChannelId] = useState("UCHEnZhUKjZSLYs3jJ0raKZA");
  const [numDistinctWords, setNumDistinctWords] = useState(0);
  const [totalWords, setTotalWords] = useState(0);
  const [yearVsWpmVsViews, setYearVsWpmVsViews] = useState([]);
  const [useAlreadyCalculated, setUseAlreadyCalculated] = useState(false);

  const [loading, setLoading] = useState(false);
  const [initialLoadComplete, setInitialLoadComplete] = useState(false);

  // Function to fetch statistics from the backend
  const fetchStatistics = async () => {
    setLoading(true);

    const response = await axios.post("/api/statistics", {
      channel_id: channelId,
      use_already_calculated: useAlreadyCalculated,
    });
    const data = response.data;

    setNumDistinctWords(data.numDistinctWords);
    setTotalWords(data.totalWords);
    setYearVsWpmVsViews(parseYearWpmViewsData(data.yearAndWpmAndViews));

    setLoading(false);
    setInitialLoadComplete(true);

    //console.log(data)
    //console.log(parseYearWpmViewsData(data.yearAndWpmAndViews))
    //console.log(averageWpmEachYear(yearVsWpmVsViews))
  };

  return (
    <div className="min-h-screen bg-white p-6">
      <h1 className="mb-1 text-center text-xl font-bold">Analyze How Youtubers Speak</h1>
      <h2 className="mb-10 text-center text-gray-500">Enter channel id and it will show some graphs</h2>

      <div className="mb-10 flex flex-col gap-2 rounded-lg border border-gray-300 p-3">
        <div className="flex flex-row gap-2">
          <input className="accent-black" type="checkbox" checked={useAlreadyCalculated} onChange={(e) => setUseAlreadyCalculated(e.target.checked)} />
          <p className="font-semibold">Use cached data</p>
        </div>
        <input className="rounded-lg border border-gray-300 p-2" type="text" value={channelId} onChange={(e) => setChannelId(e.target.value)} placeholder="Enter channel id" />
        <button className="rounded bg-black px-4 py-2 text-white" onClick={fetchStatistics}>
          Show data
        </button>
      </div>

      <div className="mb-5 flex flex-col gap-3 rounded-lg border border-gray-300 p-5">
        <h3>Unique Words</h3>
        <h1 className="text-3xl font-bold">{numDistinctWords}</h1>
      </div>

      <div className="mb-10 flex flex-col gap-3 rounded-lg border border-gray-300 p-5">
        <h3>Total Words</h3>
        <h1 className="text-3xl font-bold">{totalWords}</h1>
      </div>

      {loading && <div className="animate-pulse text-center text-xl text-gray-600">Loading...</div>}

      <div className={`${initialLoadComplete && !loading ? "opacity-100" : "pointer-events-none opacity-0"} transition-opacity duration-700`}>
        <h1 className="mb-10 border-b pb-2 text-center text-2xl font-semibold text-gray-800">Data Overview</h1>

        <div style={{ width: "100%", height: 200 }}>
          <ResponsiveContainer>
            <LineChart data={averageWpmEachYear(yearVsWpmVsViews)} margin={{ top: 5, right: 0, left: 0, bottom: 15 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={["dataMin", "dataMax"]} dataKey="year" label={{ value: "Year", position: "insideBottom", offset: -10 }} />
              <YAxis label={{ value: "Average WPM", angle: -90, position: "insideLeft", style: { textAnchor: "middle" } }} />
              <Tooltip />
              <Line type="monotone" dataKey="avgWpm" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ width: "100%", height: 200 }}>
          <ResponsiveContainer>
            <ScatterChart margin={{ top: 20, right: 0, left: 0, bottom: 15 }}>
              <CartesianGrid />
              <XAxis type="number" dataKey="views" label={{ value: "Views", position: "insideBottom", offset: -10 }} />
              <YAxis type="number" dataKey="wpm" label={{ value: "WPM", angle: -90, position: "insideLeft", style: { textAnchor: "middle" } }} />
              <Tooltip />
              <Scatter data={yearVsWpmVsViews}>
                {yearVsWpmVsViews?.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={`hsl(${(entry.year * 137) % 360}, 65%, 55%)`} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default App;
