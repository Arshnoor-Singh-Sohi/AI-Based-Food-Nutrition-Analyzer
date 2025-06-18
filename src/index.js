import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import { reportWebVitals } from './reportWebVitals';

// This is React's modern way of starting your application
// Think of this as the engine that brings your App component to life
const container = document.getElementById('root');
const root = createRoot(container);

// This tells React to render your entire application inside the 'root' div
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Performance monitoring - this helps you understand how fast your app loads
reportWebVitals();