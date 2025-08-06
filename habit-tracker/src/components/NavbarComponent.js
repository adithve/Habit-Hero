import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const NavbarComponent = () => {
  const navigate = useNavigate();
  const [isCollapsed, setIsCollapsed] = useState(true);

const handleLogout = async () => {
  try {
    const token = localStorage.getItem("token");

    const response = await fetch("http://localhost:8000/api/logout/", {
      method: "POST",
      headers: {
        "Authorization": `Token ${token}`,
      },
    });

    if (response.ok) {
      localStorage.removeItem("token");
      navigate("/");
    } else {
      console.error("Logout failed");
    }
  } catch (error) {
    console.error("Error during logout:", error);
  }
};


  const toggleNavbar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary" style={{ padding: "10px 20px" }}>
      <span className="navbar-brand fw-bold">Habit Tracker</span>

      {}
      <button
        className="navbar-toggler"
        type="button"
        onClick={toggleNavbar}
        aria-controls="navbarNav"
        aria-expanded={!isCollapsed}
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      {}
      <div className={`collapse navbar-collapse ${!isCollapsed ? "show" : ""}`} id="navbarNav">
        <ul className="navbar-nav ms-auto align-items-center">
          <li className="nav-item">
            <button
              className="btn btn-outline-light me-2"
              onClick={() => navigate("/dashboard")}
            >
              Dashboard
            </button>
          </li>
          <li className="nav-item">
            <button
              className="btn btn-outline-light me-2"
              onClick={() => navigate("/analytics")}
            >
              Analytics
            </button>
          </li>
          <li className="nav-item">
            <button className="btn btn-danger" onClick={handleLogout}>
              Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default NavbarComponent;
