import React from "react";
import { useAtomValue } from "jotai";
import { useResetAtom } from "jotai/utils";
import { jwtDecode } from "jwt-decode";
import { toast } from "react-hot-toast";
import { useNavigate, NavLink } from "react-router-dom";

import { jwtAtom } from "../atoms/store";

const AuthTopNav = () => {
  const jwt = useAtomValue(jwtAtom);

  const decoded = jwtDecode(jwt?.access);

  const navigate = useNavigate();

  const resetJwt = useResetAtom(jwtAtom);
  const onLogout = () => {
    toast.success(`User with ID ${decoded?.user_id} successfully logout`);
    resetJwt();
    localStorage.clear();
    navigate("/login");
  };

  // console.log('DECODE', decoded)
  return (
    <ul>
      <li>
        <NavLink to={"/about"}>About</NavLink>
      </li>
      <li>
        <NavLink to={"/dashboard"}>Dashboard</NavLink>
      </li>
      <li>
        <NavLink to={"/profile"}>User ID: {decoded.user_id}</NavLink>
      </li>

      <li>
        <button onClick={onLogout} className="outline">
          Logout
        </button>
      </li>
    </ul>
  );
};

export default AuthTopNav;
