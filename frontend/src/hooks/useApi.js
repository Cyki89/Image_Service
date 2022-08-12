import { useContext } from "react";
import ApiContext from "../context/ApiContext";

const useApi = () => {
  return useContext(ApiContext);
};

export default useApi;
