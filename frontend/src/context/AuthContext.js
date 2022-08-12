import { createContext, useState } from "react";
import axios from "../api/axios";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  const [csrf, setCsrf] = useState();
  const [user, setUser] = useState();

  const getCsrf = async () => {
    const response = await axios.get("auth/csrf/", {
      withCredentials: true,
    });
    const csrfToken = response.headers["x-csrftoken"];
    setCsrf(csrfToken);
  };

  const authenticateUser = async () => {
    try {
      const response = await axios.get("auth/authentication/", {
        withCredentials: true,
      });
      setUser(response.data);
    } catch (err) {
      if (err.status === 401) setUser(null);
    }
  };

  const contextData = {
    csrf,
    getCsrf,
    user,
    setUser,
    authenticateUser,
  };

  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  );
};
