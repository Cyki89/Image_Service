import ErrorScreen from "../special_screens/ErrorScreen";

const Unauthorized = () => {
  return (
    <ErrorScreen>You don't have permissions to see this content.</ErrorScreen>
  );
};

export default Unauthorized;
