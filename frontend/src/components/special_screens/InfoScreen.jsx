const InfoScreen = ({ children }) => {
  return (
    <div className="info-screen">
      <div className="info-msg">
        {children}
        <span className="info-mark">i</span>
      </div>
    </div>
  );
};

export default InfoScreen;
