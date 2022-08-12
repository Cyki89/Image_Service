const ErrorScreen = ({ children }) => {
  return (
    <div className="error-screen">
      <div className="error-msg">
        {children}
        <span className="error-mark">!</span>
      </div>
    </div>
  );
};

export default ErrorScreen;
