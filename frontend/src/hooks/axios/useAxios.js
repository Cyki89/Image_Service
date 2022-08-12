import { useState } from "react";

import useApi from "../useApi";
import useEffectOnce from "../useEffectOnce";

const useAxios = (configObj) => {
  const { setApiAvailable } = useApi();
  const { axiosInstance, method, url, requestConfig = {} } = configObj;

  const [response, setResponse] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffectOnce(() => {
    const fetchData = async () => {
      try {
        const res = await axiosInstance[method.toLowerCase()](url, {
          ...requestConfig,
        });
        setResponse(res.data);
      } catch (err) {
        console.log(err);
        if (!err.response.data) return setApiAvailable(false);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    // eslint-disable-next-line
  }, []);

  return [response, error, loading];
};

export default useAxios;
