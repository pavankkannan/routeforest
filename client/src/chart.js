import { useState } from 'react';
import { PieChart, Pie, Legend, Label, ResponsiveContainer, Cell } from 'recharts';

export default function Chart({ routePercentages, totRec }) {
  const [clickedCell, setClickedCell] = useState("Click on a Cell");

  const data = Object.entries(routePercentages).map(([name, value]) => ({
    name,
    value
  }));

  const colors = {
    "FLAT": "#fbf8cc",
    "SCREEN": "#fde4cf",
    "CORNER": "#ffcfd2",
    "HITCH": "#f1c0e8",
    "IN": "#cfbaf0",
    "GO": "#a3c4f3",
    "CROSS": "#90dbf4",
    "ANGLE": "#8eecf5",
    "OUT": "#98f5e1",
    "SLANT": "#b9fbc0",
    "POST": "#fffffc",
    "WHEEL": "#52575D",
    "undefined": "grey",
    "OTHER": 'white'
  }

  const handleCellClick = (entry) => {
    setClickedCell(`${entry.name}: ${entry.value} catches (${Math.round((entry.value/totRec) * 100)}%)`);
  };

  // const label = ({ name, value }) => `${name}: ${value}`;
  return (
    <ResponsiveContainer width="100%" height={400}>
      <p
        style={{color: '#44C37D', fontSize: '18px', textAlign: 'center', marginTop: '40px', marginBottom: '-45px', fontWeight: 'bold'}}
      >
      Route Tree Breakdown</p>
      <PieChart>
        <Pie
          dataKey="value"
          isAnimationActive={false}
          data={data}
          innerRadius={80}
          outerRadius={140}
          // fill="#44C37D"
          // label={label}
          legendType='square'
          stroke='#08432A'
          strokeWidth={2}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[entry.name] || 'blue'} style={{outline: 'none'}} onClick={() => handleCellClick(entry)}/>
          ))}
          <Label 
            value={clickedCell} 
            position="center" 
            style={{ fontSize: '14px', fill: 'white', fontWeight: 'bold' }} 
          />
        </Pie>

        {/* <Legend verticalAlign="top" height={36}/> */}
      </PieChart>
      

    </ResponsiveContainer>
  );
}
