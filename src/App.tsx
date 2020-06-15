import React, { useState } from "react";
import logo from "./logo.svg";
import TimelineViz from "./visualizations/Timeline";

import data from "./data/test.json";

function App() {
  const [date, setDate] = useState("2019-10-10");

  return (
    <div>
      <h1>Welcome to RL Esports!</h1>
      <TimelineViz initialData={data} date={date} />
    </div>
  );
}

export default App;
