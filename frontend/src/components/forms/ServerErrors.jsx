import ErrorContainer from "./ErrorContainer";

const ServerErrors = ({ error }) => {
  return (
    error?.response?.status >= 500 && (
      <ErrorContainer errors={error.response.statusText} />
    )
  );
};

export default ServerErrors;
