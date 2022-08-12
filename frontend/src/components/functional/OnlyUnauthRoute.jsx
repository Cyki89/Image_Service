import { Navigate, Outlet } from "react-router-dom";

import useApi from "../../hooks/useApi";
import useAuth from "../../hooks/useAuth";

const OnlyUnauthRoute = () => {
  const { apiAvailable } = useApi();
  const { user } = useAuth();

  const context = () => {
    if (!apiAvailable) return <Navigate to="/unconnected" />;
    if (user) return <Navigate to="/authenticated" />;
    return <Outlet />;
  };

  return context();
};
export default OnlyUnauthRoute;
