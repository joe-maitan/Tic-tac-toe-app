import React, { createContext, useContext } from 'react';

const hostAddress = process.env.FLASK_HOST;
const portNumber = process.env.FLASK_SERVER_PORT;

const apiBaseUrl = `http://${hostAddress}:${portNumber}`;

// Create the context with apiBaseUrl as its default value
const ApiContext = createContext(apiBaseUrl);

export const ApiProvider = ({ children }) => {
  return (
    <ApiContext.Provider value={apiBaseUrl}>
      {children}
    </ApiContext.Provider>
  );
};

// Custom hook to use the ApiContext
export const useApi = () => {
  return useContext(ApiContext);
};