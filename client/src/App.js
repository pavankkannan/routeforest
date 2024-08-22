import React, {useState, useEffect} from 'react';
import './App.css';
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'

function SearchResultsList({ results, setResults, setInput, setPlayer }) {

  const setNewPlayer = (name) => {
    setPlayer(name.replace(" ", "-"))
    console.log(name)
    setInput("")
    setResults([])
    // document.getElementById("inputField").innerHTML = "";
  }

  return (
    <div className='SearchResultsList'>
      {results.map((result, id) => {
        return (
          <div className='searchResult' key={id} onClick={() => setNewPlayer(result.name)}>
            <img className='searchHeadshot' src={result.headshot} alt=''></img>
            <p>{result.name}</p>
            <p>{result.team} - #{result.jersey}</p>
          </div>
        )
      })}
    </div>
  );
}

function SearchBar({ setResults, input, setInput }) {
  // [input, setInput] = useState("")

  const fetchData = (value) => {
    fetch("/players")
      .then((response) => response.json())
      .then((json) => {
        const results = json.filter((user) => {
          return (
            value && user && user.name && user.name.toLowerCase().includes(value)
          );
        });
        setResults(results)
      });
  };

  const handleChange = (value) => {
    setInput(value);
    fetchData(value.toLowerCase())
    document.getElementById("inputField").focus();

  };

  return (
    <div className='SearchBar'>
      <div className='searchIcon'>
        <img src='static/searchIcon.png' alt=''/>
      </div>
      <input type='text' className='inputField' id='inputField' placeholder='Search for a player' value={input} onChange={(e) => handleChange(e.target.value)}/>
      <div className='clearSearchIcon'>
        { input ? <img src='static/clearSearchIcon.webp' onClick={() => handleChange("")} alt=''/> : null }
      </div>
    </div>
  )

}

function Header({ data }) {
  // const { pName, pNumber, pPosition, pTeam, pHeadshot, pCollege } = data
  const positions = {'QB': 'Quarterback', 'RB': 'Running Back', 'WR': 'Wide Receiver', 'TE': 'Tight End'}
  const teams = {
    'ARI': 'Arizona Cardinals', 'ATL': 'Atlanta Falcons', 'BAL': 'Baltimore Ravens', 'BUF': 'Buffalo Bills', 'CAR': 'Carolina Panthers', 'CHI': 'Chicago Bears', 'CIN': 'Cincinnati Bengals', 'CLE': 'Cleveland Browns', 
    'DAL': 'Dallas Cowboys', 'DEN': 'Denver Broncos', 'DET': 'Detroit Lions', 'GB': 'Green Bay Packers', 'HOU': 'Houston Texans', 'IND': 'Indianapolis Colts', 'JAX': 'Jacksonville Jaguars', 'KC': 'Kansas City Chiefs', 
    'OAK': 'Oakland Raiders', 'LAC': 'Los Angeles Chargers', 'LAR': 'Los Angeles Rams', 'MIA': 'Miami Dolphins', 'MIN': 'Minnesota Vikings', 'NE': 'New England Patriots', 'NO': 'New Orleans Saints', 'NYG': 'New York Giants', 
    'NYJ': 'New York Jets', 'PHI': 'Philadelphia Eagles', 'PIT': 'Pittsburgh Steelers', 'SF': 'San Francisco 49ers', 'SEA': 'Seattle Seahawks', 'TB': 'Tampa Bay Buccaneers', 'TEN': 'Tennessee Titans', 'WAS': 'Washington Commanders'
  };
  
  return (
    <div className='Header'>
      <img src={data.headshot} id="headshot" alt="headshot"/>
      <div className='headerInfo'>
        <h1>{data.name}</h1>
        <p>{teams[data.team]}</p>
        <p>{positions[data.position]} - #{data.number}</p>
        <p>{data.college}</p>
      </div>
    </div>
    
  )
}

function TopStats({ data }) {
  const [recsPos, recsAll] = data.recsRank
  const [recYardsPos, recYardsAll] = data.recYardsRank
  const [tdsPos, tdsAll] = data.tdsRank

  function ordinal(number) {
    const suffixes = { 1: 'st', 2: 'nd', 3: 'rd' };
    const lastTwoDigits = number % 100;
  
    if (lastTwoDigits >= 11 && lastTwoDigits <= 13) {
      return number + 'th';
    }
  
    const lastDigit = number % 10;
    const suffix = suffixes[lastDigit] || 'th';
    
    return number + suffix;
  }

  return (
    <div className='TopStats'>
      <div className='topStat'>
        <p className='topStatLabel'>Receptions</p>
        <p className='topStatText'>{data.totReceptions}</p>
        <div className='ranks'>
          <p className='rankText'>Among {data.position}s: <span>{ordinal(recsPos)}</span></p>
          <p className='rankText'>Overall: <span>{ordinal(recsAll)}</span></p>
        </div>
      </div>
      <div id="middle" className='topStat'>
        <p className='topStatLabel'>Rec. Yards</p>
        <p className='topStatText'>{data.totYards}</p>
        <div className='ranks'>
          <p className='rankText'>Among {data.position}s: <span>{ordinal(recYardsPos)}</span></p>
          <p className='rankText'>Overall: <span>{ordinal(recYardsAll)}</span></p>
        </div>
      </div>
      <div className='topStat'>
        <p className='topStatLabel'>TDS</p>
        <p className='topStatText'>{data.totTDs}</p>
        <div className='ranks'>
          <p className='rankText'>Among {data.position}s: <span>{ordinal(tdsPos)}</span></p>
          <p className='rankText'>Overall: <span>{ordinal(tdsAll)}</span></p>
        </div>
      </div>
    </div>
  )
}

function RecYards({ data }) {

  function calcPercent(stat) {
    const calc = Math.round(stat / data.totYards * 100);
    return Math.max(0, Math.min(100, calc));
  }
  

  const airYdPercent = calcPercent(data.totAirYards)
  const yacPercent = calcPercent(data.totYAC)
  
  return (
    <div className='RecYards'>
      <p><span style={{color: 'lightblue', fontWeight: "bold"}}>Air Yards</span> vs <span style={{color: "lightcoral", fontWeight: "bold"}}>Yards After Catch</span></p>
      <div className='recYardsLabel'>
        <div>
          <p>{airYdPercent}%</p>
        </div>
        <div>
          <p>{yacPercent}%</p>
        </div>
      </div>
      <div className='recYardsGraph'>
        <div style={{ width: `${airYdPercent}%` }} className='airYards'></div>
        <div style={{ width: `${yacPercent}%` }} className='yac'></div>
      </div>
      <div className='recYardsLabel'>
        <div>
          <p>{data.totAirYards} Yards</p>
        </div>
        <div>
          <p>{data.totYAC} Yards</p>
        </div>
      </div>
    </div>
  )
}

function CatchStatistics({ data }) {
  const [mode, toggleMode] = useState("charts")
  const handleClick = (value) => {
    toggleMode(value)
  };

    // for (var key in list) {
    //   console.log(key, list[key]);
    // }

  return (
    <div className='CatchStatistics'>
      <div className='modeHeader'>

        <div className='modeOption'>
          <p 
            style={{ 
              color: mode === "charts" ? 'white' : '#40916E', 
            }} 
            onClick={() => handleClick("charts")}> 
            Charts
          </p>
          <div className='modeBottomBorder'
            style={{
              backgroundColor: mode === 'charts' ? 'white' : '#40916E',
              borderRadius: mode === 'charts' ? '20px' : '20px 0 0 20px',
              zIndex: mode === 'charts' ? '1' : '0'
            }}
          />
        </div>

        <div className='modeOption'>
          <p 
            style={{ 
              color: mode === "field" ? 'white' : '#40916E', 
            }} 
            onClick={() => handleClick("field")}> 
            Field View
          </p>
          <div className='modeBottomBorder'
            style={{
              backgroundColor: mode === 'field' ? 'white' : '#40916E',
              borderRadius: mode === 'field' ? '20px' : '0 20x 20px 0',
              zIndex: mode === 'field' ? '1' : '0'
            }}
          />
        </div>

      </div>
      {mode === "charts" && 
        <div>
          <RecYards data={data}/>
          <img src={`/static/pie.png?t=${Date.now()}`} className="pie" alt='pie'/>
        </div>
      }
      {mode === "field" && 
        <div>
          <img src={`/static/annotatedField2.png?t=${Date.now()}`} className="field" alt='field'/>
        </div>
      }
    </div>
  )
}

function PlayerData({ playerName, isLoading, setIsLoading }) {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch(`/players/${playerName}`)
      .then(
        res => res.json()
      ).then(
        data => {
          setData(data)
          setIsLoading("false")
          // console.log(data)
        }
      )
  }, [playerName,])
  if (data == null || data.name !== playerName.replace("-", " ")) {
    return (
      <div className='PlayerData'>
        Loading...
      </div>
    )

  }
  return (
    <div className='PlayerData'>
      {/* <p><Skeleton/></p>
      <p>{data.name || <Skeleton/>}</p> */}
      <Header data={data} isLoading={isLoading} setIsLoading={setIsLoading}/>
      <TopStats data={data}/>
      <CatchStatistics data={data}/>
    </div>
  )
}


function App() {
  const [player, setPlayer] = useState("Julio-Jones")
  const [results, setResults] = useState([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState("true")

  return (
    <div className='App'>
      <SearchBar setResults={setResults} input={input} setInput={setInput}/>
      <div>
        <SearchResultsList results={results} setResults={setResults} setInput={setInput} setPlayer={setPlayer}/>
        <PlayerData playerName={player} isLoading={isLoading} setIsLoading={setIsLoading}/>
      </div>
    </div>
  )
}

export default App