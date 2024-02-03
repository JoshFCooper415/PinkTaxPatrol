import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {
  const handleClick = () => {
    setIsRed(!isRed);
  };

  const [isRed, setIsRed] = useState(false);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and fun away yayyyy to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <button onClick={handleClick} className="App-button" style={{backgroundColor: isRed ? 'red' : 'initial'}}>
          Click Me
        </button>
      </header>
    </div>
  );
}

export default App;
