// This function helps monitor your app's performance
// It measures things like how fast your app loads and responds to user interactions
const reportWebVitals = onPerfEntry => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);  // Measures visual stability
      getFID(onPerfEntry);  // Measures interactivity
      getFCP(onPerfEntry);  // Measures loading performance
      getLCP(onPerfEntry);  // Measures loading performance
      getTTFB(onPerfEntry); // Measures server responsiveness
    });
  }
};

export { reportWebVitals };