import React from 'react';
import ReactDOM from 'react-dom';
import './static/styles/global.scss'
import App from './components/App.js';

ReactDOM.render(<App />, document.getElementById("root"));

// createRoot(document.getElementById("root")).render(
//     <StrictMode>
//       <BrowserRouter>
//         <App />
//     </BrowserRouter>
//   </StrictMode>
// );