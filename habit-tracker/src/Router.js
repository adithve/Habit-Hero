import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from "./App";
import Signup from "./components/Signup";
import Dashboard from "./components/Dashboard";
import Analytics from "./components/Analytics";
import AddHabit from "./components/AddHabit";

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/add-habit" element={<AddHabit />} /> 
      </Routes>
    </Router>
  );
}

export default AppRouter;
