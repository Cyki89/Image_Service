import ErrorScreen from "../special_screens/ErrorScreen";

const Authenticated = () => {
  return (
    <ErrorScreen>
      You are already authenticated. You must logout to use other credentials.
    </ErrorScreen>
  );
};

export default Authenticated;
