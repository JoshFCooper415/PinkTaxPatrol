/* global chrome */
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {

  const [currentOption, setPriceDrop] = useState(0);
  const [currentProductOption, setProductName] = useState(0);
  const [currentID, setProductId] = useState(0);
  const [currentProduct, setProduct] = useState(0);
  const [currentLink, setLink] = useState('')


  const options = ['product 1', 'product 2', 'product 3'];
  //PRICE
  const priceOptions = [5, 2.4, 10];
  //NAME
  const nameOptions = ['shirt roeijgore gjierojgo erojieogjeoijge roeijgoe erogjeoij', 'razor', 'shampoo'];
  //ASIN
  const idOptions = ['a', 'b', 'cdfgijeiofjgaj'] 
  //PRODUCT LINK
  const productOptions = ['https://www.amazon.com/dp/B08KT2Z93D', 'https://www.amazon.com/dp/B00477OXKA', 'https://www.amazon.com/dp/B0037LOPQY'] 
  
  useEffect(() => {
    chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
      if (request.action === 'updateAppState') {
        const { productName, priceDrop, ASIN, links } = request.data;

        // Update the state accordingly
        setProductName(productName[currentProductOption]);
        setPriceDrop(priceDrop[currentOption]);
        setProductId(ASIN[currentID]);
        setLink(links[currentProductOption]);
      }
    });
  }, [currentOption, currentProductOption, currentID, currentProduct]);

  // left and right moving
  const handleLeft = (e) => {
    e.stopPropagation();
    const newIndex = (currentOption - 1 + options.length) % options.length;
    setPriceDrop(newIndex);
    setProductName(newIndex);
    setProductId(newIndex);
  };

  const handleRight = (e) => {
    e.stopPropagation();
    const newIndex = (currentOption + 1) % options.length;
    setPriceDrop(newIndex);
    setProductName(newIndex);
    setProductId(newIndex);
  }

  const redirectToLink = () => {
    chrome.tabs.create({ url: productOptions[currentProductOption] });
  }

  return (
    <div className="App">
      <header className="App-header">

        <div className="product-container" onClick={redirectToLink}>
          
          <p className="product-name">
            <strong>Product Name:</strong> {nameOptions[currentProductOption]}
          </p>

          <p className='price-drop'>
            <strong>Price Drop:</strong> ${priceOptions[currentOption]}
          </p>

          <p className='product-id'>
            <strong>Product ID:</strong> {idOptions[currentID]}
          </p>

        </div>

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
