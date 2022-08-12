import { Link } from "react-router-dom";

import useApi from "./../../hooks/useApi";

const NavLink = ({ title, to }) => {
  const { apiAvailable } = useApi();
  return (
    <Link className="navbar-link" to={to} reloadDocument={!apiAvailable}>
      {title}
    </Link>
  );
};

export default NavLink;
