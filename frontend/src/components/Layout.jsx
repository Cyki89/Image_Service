import Container from "react-bootstrap/Container";
import { Outlet } from "react-router-dom";
import TopBar from "./navigation/TopBar";

const Layout = () => {
  return (
    <>
      <TopBar />
      <Container className="main-container">
        <Outlet />
      </Container>
    </>
  );
};

export default Layout;
