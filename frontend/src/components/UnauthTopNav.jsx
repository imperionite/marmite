import React from "react";
import { NavLink } from "react-router-dom";

const UnauthTopNav = () => {
  return (
    <ul>
      <li>
        <NavLink to={"/"}>Home</NavLink>
      </li>

      <li>
        <NavLink to={"/signup"}>Signup</NavLink>
      </li>
      <li>
        <NavLink to={"/login"} role="button">
          Login
        </NavLink>
      </li>
    </ul>
  );
};

export default UnauthTopNav;
