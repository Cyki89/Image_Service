import { createContext, useState } from "react";

const ApiContext = createContext();

export default ApiContext;

export const ApiProvider = ({ children }) => {
  const [apiAvailable, setApiAvailable] = useState(true);

  const contextData = {
    apiAvailable,
    setApiAvailable,
  };

  return (
    <ApiContext.Provider value={contextData}>{children}</ApiContext.Provider>
  );
};
