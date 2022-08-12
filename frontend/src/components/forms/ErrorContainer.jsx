import React from "react";

const ErrorContainer = ({ errors }) => {
  return (
    <div className="error-container">
      <div className="error-msg">
        {errors}
        <span className="error-mark">!</span>
      </div>
    </div>
  );
};

export default ErrorContainer;
