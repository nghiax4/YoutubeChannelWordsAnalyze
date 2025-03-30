import { useState } from "react"
import axios from "axios"
import "./App.css"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, Cell } from "recharts"

function parseYearWpmViewsData(yearAndWpmAndViews) {
  return yearAndWpmAndViews.map((item, index) => ({
    year: item[0],
    wpm: item[1],
    views: item[2],
  }))
}

function averageWpmEachYear(yearAndWpmAndViews) {
  const yearToWpmStats = {}

  for (const item of yearAndWpmAndViews) {
    const year = item.year
    const wpm = item.wpm

    if (!yearToWpmStats[year]) {
      yearToWpmStats[year] = { reciprocalSum: 0, count: 0 }
    }

    yearToWpmStats[year].reciprocalSum += 1 / wpm
    yearToWpmStats[year].count += 1
  }

  const result = []
  for (const year in yearToWpmStats) {
    result.push({
      year: parseInt(year),
      avgWpm: yearToWpmStats[year].count / yearToWpmStats[year].reciprocalSum
    })
  }

  return result
}

function App() {
  const [channelId, setChannelId] = useState("UCHEnZhUKjZSLYs3jJ0raKZA")
  const [numDistinctWords, setNumDistinctWords] = useState(0)
  const [totalWords, setTotalWords] = useState(0)
  const [yearVsWpmVsViews, setYearVsWpmVsViews] = useState([])
  const [useAlreadyCalculated, setUseAlreadyCalculated] = useState(false)

  // Function to fetch statistics from the backend
  const fetchStatistics = async () => {
    const response = await axios.post("/api/statistics", { channel_id: channelId, use_already_calculated: useAlreadyCalculated })
    const data = response.data

    setNumDistinctWords(data.numDistinctWords)
    setTotalWords(data.totalWords)
    setYearVsWpmVsViews(parseYearWpmViewsData(data.yearAndWpmAndViews))

    //console.log(data)
    //console.log(parseYearWpmViewsData(data.yearAndWpmAndViews))
    //console.log(averageWpmEachYear(yearVsWpmVsViews))
  }

  return (
    <div>
      <input type="checkbox" checked={useAlreadyCalculated} onChange={(e) => setUseAlreadyCalculated(e.target.checked)} />
      <input type="text" value={channelId} onChange={(e) => setChannelId(e.target.value)} placeholder="Enter channel id" />

      <button onClick={fetchStatistics}>Show data</button>
      <p>Num distinct words: {numDistinctWords}</p>
      <p>Total words: {totalWords}</p>

      <div style={{ width: "50%", height: 200 }}>
        <ResponsiveContainer>
          <LineChart data={averageWpmEachYear(yearVsWpmVsViews)} margin={{ top: 5, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" domain={["dataMin", "dataMax"]} dataKey="year" label={{ value: "Year", position: "insideBottom", offset: -10 }} />
            <YAxis label={{ value: "Average WPM", angle: -90, position: "insideLeft", style: { textAnchor: "middle" } }} />
            <Tooltip />
            <Line type="monotone" dataKey="avgWpm" stroke="#82ca9d" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ width: "50%", height: 200 }}>
        <ResponsiveContainer>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid />
            <XAxis type="number" dataKey="views" />
            <YAxis type="number" dataKey="wpm" />
            <Tooltip />
            <Scatter data={yearVsWpmVsViews}>
              {yearVsWpmVsViews?.map((entry, index) => (
                <Cell key={`cell-${index}`} fill="#000000" />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default App
