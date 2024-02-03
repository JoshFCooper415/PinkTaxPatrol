
function getDataFromElementById() {
    const element = document.getElementById('exampleElement');
    if (element) {
      console.log('Data from element:', element.textContent);
    } else {
      console.log('Element with ID "exampleElement" not found');
    }
  }
  
  getDataFromElementById();
  