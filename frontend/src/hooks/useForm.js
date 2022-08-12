import { useState } from "react";

function useForm(initial_values = {}) {
  const [data, setData] = useState(() => initial_values);

  const handleInputChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.files[0] });
  };

  return [data, handleInputChange, handleFileChange];
}

export default useForm;
