import { useState, useEffect } from "react";

import { showErrorNotification } from "../../utils/notifications";

const useAxiosFunction = () => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [controller, setController] = useState();

  const axiosFetch = async (configObj) => {
    const { axiosInstance, method, url, requestConfig = {} } = configObj;

    try {
      setLoading(true);
      setError("");
      setResponse(null);

      const ctrl = new AbortController();
      setController(ctrl);

      const res = await axiosInstance[method.toLowerCase()](url, {
        ...requestConfig,
        signal: ctrl.signal,
      });
      setResponse(res.data);
    } catch (err) {
      console.log(err);

      // unconnected api
      if (!err.response.data)
        return showErrorNotification(`${err.message}. Try again in a minute.`);

      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    return () => controller && controller.abort();
  }, [controller]);

  return [response, error, loading, axiosFetch];
};

export default useAxiosFunction;
