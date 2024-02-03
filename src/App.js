import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {
  // red button stuff
  const handleClick = () => {
    setIsPink(!isPink);
  };
  const [isPink, setIsPink] = useState(false);

  // ok let's do option choosing
  const [currentOption, setCurrentOption] = useState(0);
  const options = ['product 1', 'product 2', 'product 3'];

  // left and right moving
  const handleLeft = () => {
    setCurrentOption(prev => (prev -1 + options.length) % options.length);
  };

  const handleRight = () => {
    setCurrentOption(prev => (prev + 1) % options.length);
  }

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
        <button onClick={handleClick} className="App-button" style={{backgroundColor: isPink ? '#bd4880' : 'initial'}}>
          Click Me
        </button>

        {/* Render the current option*/}
        <div>{options[currentOption]}</div>
        {/* Navigation buttons */}
        <div className="navigation">
          <button onClick={handleLeft} className="left-triangle"></button>
          <button onClick={handleRight} className="right-triangle"></button>
        </div>
      </header>
    </div>
  );
}

export default App;

