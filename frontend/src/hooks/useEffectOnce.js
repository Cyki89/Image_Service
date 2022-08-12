import { useEffect, useRef } from "react";

const useEffectOnce = (callback, deps) => {
  const effectRun = useRef(false);
  useEffect(() => {
    if (effectRun.current === true) return;

    callback();

    return () => (effectRun.current = true);
    // eslint-disable-next-line
  }, [...deps]);
};

export default useEffectOnce;
