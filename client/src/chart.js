import { PieChart, Pie, Legend, ResponsiveContainer, Cell } from 'recharts';

export default function Chart({ routePercentages }) {

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

  const label = ({ name, value }) => `${name}: ${value}`;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          dataKey="value"
          isAnimationActive={false}
          data={data}
          innerRadius={40}
          outerRadius={100}
          // fill="#44C37D"
          // label={label}
          legendType='square'
          stroke='#08432A'
          strokeWidth={2}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[entry.name] || 'blue'} />
          ))}
        </Pie>

        <Legend verticalAlign="top" height={36}/>
      </PieChart>
      

    </ResponsiveContainer>
  );
}
