import { useEffect } from "react";
import { useNavigate, Navigate } from "react-router-dom";

import { axiosPrivate } from "../../api/axios";

import useApi from "../../hooks/useApi";
import useAuth from "../../hooks/useAuth";
import useAxios from "../../hooks/axios/useAxios";

import LoadingScreen from "../special_screens/LoadingScreen";
import ErrorScreen from "../special_screens/ErrorScreen";
import InfoScreen from "../special_screens/InfoScreen";

const Logout = () => {
  const { apiAvailable } = useApi();
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const [response, error, loading] = useAxios({
    axiosInstance: axiosPrivate,
    method: "get",
    url: "auth/logout/",
  });

  useEffect(() => {
    if (response) setUser(null);
    // eslint-disable-next-line
  }, [response]);

  const context = () => {
    if (!apiAvailable) return <Navigate to="/unconnected" />;
    if (loading) return <LoadingScreen />;
    if (error) {
      if (error.response?.status === 401)
        return <Navigate to="/unauthenticated" />;

      return <ErrorScreen>Unexpeceted Error: {error.message}</ErrorScreen>;
    }
    return <InfoScreen>You are succefully logged out!</InfoScreen>;
  };

  return context();
};

export default Logout;
