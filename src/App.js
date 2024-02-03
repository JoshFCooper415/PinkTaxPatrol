import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {

  var count = 0;
  // red button stuff
  const handleClick = () => {
    setIsRed(!isRed);
  };
  const [isRed, setIsRed] = useState(false);
  // end red button stuff

  // ok let's do option choosing
  const [currentOption, setCurrentOption] = useState(0);
  const options = ['product 1', 'product 2', 'product 3'];

  const updateImage = function(count) {
    document.getElementById('product image').src = "smile" + (count % options.length) + ".jpg"
  }

  const handleLeft = () => {
    count = (count -1 + options.length)
    setCurrentOption(count);

  };

  const handleRight = () => {
    count = (count + 1) % options.length
    setCurrentOption(count);
    updateImage(count);
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <div className='image'>
          <img id='product image' src='' />
        </div>

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

        {/* Render the current option*/}
        <div>{options[currentOption]}</div>
        {/* Navigation buttons */}
        <div className="navigation" >
          <button onClick={handleLeft}>&lt; Left</button>
          <button onClick={handleRight}>Right &gt;</button>
        </div>

      </header>
    </div>
  );
}

export default App;

