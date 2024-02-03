/* global chrome */
import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  var count = 0;
  
  const [isPink, setIsPink] = useState(false);
  const [currentOption, setCurrentOption] = useState(0);
  const options = ['product 1', 'product 2', 'product 3'];
  const [imageSrc, setImageSrc] = useState("/smile1.png");

  const handleClick = () => {
    setIsPink(!isPink);
  };

  const updateImage = (index) => {
    setImageSrc("/smile" + (index+1) + ".png")
  }

  // left and right moving
  const handleLeft = () => {
    const newIndex = (currentOption - 1 + options.length) % options.length;
    setCurrentOption(newIndex);
    updateImage(newIndex);
  };

  const handleRight = () => {
    const newIndex = (currentOption + 1) % options.length;
    setCurrentOption(newIndex);
    updateImage(newIndex);
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <img class = "product_image" id = "product" src={imageSrc} alt="Product"></img>
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
