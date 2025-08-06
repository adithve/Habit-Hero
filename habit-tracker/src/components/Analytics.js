import React, { useState, useEffect } from "react";
import axios from "axios";

const categories = ["All", "Mental Health", "Fitness", "Productivity"];

const Analytics = () => {
  const [habits, setHabits] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [bestDate, setBestDate] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:8000/api/habits/analytics/", {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        setHabits(response.data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError("Failed to load analytics data.");
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  useEffect(() => {
    const fetchBestDate = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://localhost:8000/api/best-date/", {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        setBestDate(res.data.best_date);
      } catch (err) {
        console.error("Error fetching best date:", err);
      }
    };

    fetchBestDate();
  }, []);

  const filteredHabits = habits.filter((habit) => {
    return selectedCategory === "All" || habit.category === selectedCategory;
  });

  return (
    <div className="container my-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h3>Analytics and Insights</h3>
        {bestDate && (
          <div className="text-muted">
            <strong>Your Best Day was on:</strong> {bestDate}
          </div>
        )}
      </div>
      <p className="text-muted">
        Visualize your performance and gain insights by filtering habits.
      </p>

      {}
      <div className="mb-3 d-flex flex-wrap align-items-center">
        <label className="me-2 fw-bold">Category:</label>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`btn btn-sm me-2 mb-2 ${
              selectedCategory === cat ? "btn-primary" : "btn-outline-primary"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {}
      {loading ? (
        <p>Loading analytics...</p>
      ) : error ? (
        <p className="text-danger">{error}</p>
      ) : filteredHabits.length === 0 ? (
        <p className="text-muted">No habits found for selected filters.</p>
      ) : (
        filteredHabits.map((habit, index) => (
          <div
            key={index}
            className="card mb-4 shadow-sm"
            style={{ borderLeft: "6px solid #007bff" }}
          >
            <div className="card-body">
              <h5 className="card-title text-primary">{habit.name}</h5>
              <p className="card-text mb-1">
                <strong>Category:</strong> {habit.category}
              </p>
              <p className="card-text mb-1">
                <strong>Current Streak:</strong> {habit.current_streak} days
              </p>
              <p className="card-text mb-1">
                <strong>Success Rate:</strong> {habit.success_rate}
              </p>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default Analytics;
