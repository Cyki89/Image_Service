import { useState } from "react";
import { Outlet } from "react-router-dom";

import useApi from "../../hooks/useApi";
import useAuth from "../../hooks/useAuth";
import useEffectOnce from "../../hooks/useEffectOnce";

import LoadingScreen from "../special_screens/LoadingScreen";

const PersistLogin = () => {
  const { setApiAvailable } = useApi();
  const { authenticateUser, user, getCsrf } = useAuth();
  const [isLoading, setIsLoading] = useState(true);

  useEffectOnce(() => {
    const setUserOrGetCsrf = async () => {
      try {
        await authenticateUser();
        await getCsrf();
      } catch (err) {
        if (err.status === 401) await getCsrf();
        else setApiAvailable(false);
      } finally {
        setIsLoading(false);
      }
    };

    !user ? setUserOrGetCsrf() : setIsLoading(false);
  }, []);

  return <>{isLoading ? <LoadingScreen /> : <Outlet />}</>;
};

export default PersistLogin;
