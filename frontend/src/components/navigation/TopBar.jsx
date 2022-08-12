import useAuth from "./../../hooks/useAuth";

import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

import logo from "./../../logo.svg";
import NavLink from "./NavLink";

const TopBar = () => {
  const { user } = useAuth();

  return (
    <Navbar collapseOnSelect className="navbar" expand="lg" variant="dark">
      <Container>
        <Navbar.Brand className="navbar-brand" href="#">
          <img
            src={logo}
            width="35"
            height="35"
            className="d-inline-block align-bottom"
            alt=""
          />
          Upload Image Service
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <NavLink title="Home" to="/" />
            <NavLink title="Upload Image" to="/upload" />
            <NavLink title="Image List" to="/images" />
          </Nav>
          <Nav>
            {user ? (
              <>
                <NavLink title={user.username} to="/profile" />
                <NavLink title="Logout" to="/logout" replace={true} />
              </>
            ) : (
              <>
                <NavLink title="Login" to="/login" />
                <NavLink title="Register" to="/register" />
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default TopBar;
