import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confPassword, setConfPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    if (password !== confPassword) {
      setError("Passwords do not match!");
      return;
    }

    const user = {
      username: username,
      password: password,
    };
    console.log(user)

    axios.post("http://127.0.0.1:8000/api/signup/", user)
      .then((response) => {
        setError("");
        navigate("/");
      })
      .catch((error) => {
        if (error.response && error.response.data.errors) {
          setError(Object.values(error.response.data.errors).join(" "));
          console.log(error.response.data)
        } else {
             console.log(error.response.data)
          setError("Failed to connect to API.");
        }
      });
  };

  return (
    <div className="card shadow p-4 mt-5" style={{ maxWidth: "400px", margin: "auto" }}>
      <h3 className="text-center mb-3">SIGN UP</h3>

      {error && <div className="alert alert-danger">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Username</label>
          <input
            type="text"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Confirm Password</label>
          <input
            type="password"
            className="form-control"
            value={confPassword}
            onChange={(e) => setConfPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary w-100">
          SIGN UP
        </button>
      </form>

      <p className="text-center mt-3">
        Already have an account? <Link to="/">Login</Link>
      </p>
    </div>
  );
}

export default Signup;
