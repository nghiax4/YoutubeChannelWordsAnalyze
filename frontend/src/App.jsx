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

function App() {
  const [numDistinctWords, setNumDistinctWords] = useState(0)
  const [totalWords, setTotalWords] = useState(0)
  const [yearVsWpmVsViews, setYearVsWpmVsViews] = useState(null)

  // Function to fetch statistics from the backend
  const fetchStatistics = async () => {
    const response = await axios.get("/api/statistics")
    const data = response.data

    setNumDistinctWords(data.numDistinctWords)
    setTotalWords(data.totalWords)
    setYearVsWpmVsViews(parseYearWpmViewsData(data.yearAndWpmAndViews))

    console.log(data)
    console.log(parseYearWpmViewsData(data.yearAndWpmAndViews))
  }

  return (
    <div>
      <button onClick={fetchStatistics}>Show data</button>
      <p>Num distinct words: {numDistinctWords}</p>
      <p>Total words: {totalWords}</p>

      <div style={{ width: "50%", height: 200 }}>
        <ResponsiveContainer>
          <LineChart data={yearVsWpmVsViews} margin={{ top: 5, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" domain={["dataMin", "dataMax"]} dataKey="year" label={{ value: "Label for X Axis", position: "insideBottom", offset: -10 }} />
            <YAxis label={{ value: "Label for Y Axis", angle: -90, position: "insideLeft", style: { textAnchor: "middle" } }} />
            <Tooltip />
            <Line type="monotone" dataKey="wpm" stroke="#82ca9d" />
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

      <div></div>
    </div>
  )
}

export default App
