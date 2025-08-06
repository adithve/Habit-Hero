import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

function AddHabit() {
  const [newHabit, setNewHabit] = useState({
    name: "",
    frequency: "Daily",
    category: "Fitness",
    startDate: "",
  });

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    if (!token || !username) {
      alert("You must be logged in to add a habit.");
      return;
    }
    console.log("entered inside the function")
    const payload = {
      name: newHabit.name,
      frequency: newHabit.frequency.toLowerCase(), 
      category: newHabit.category,
      start_date: newHabit.startDate,
      username: username,
    };
    console.log(payload)

    try {
      const response = await fetch("http://127.0.0.1:8000/api/add_habit/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to add habit");
        
      }

      const data = await response.json();
      console.log("Habit added successfully:", data);
      navigate("/dashboard");
    } catch (error) {
      console.error("Error adding habit:", error.response.data);
      alert("Failed to add habit. Please try again.");
    }
  };

  return (
    <div className="container mt-4">
      <h3>Add New Habit</h3>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Habit Name</Form.Label>
          <Form.Control
            type="text"
            value={newHabit.name}
            onChange={(e) =>
              setNewHabit({ ...newHabit, name: e.target.value })
            }
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Frequency</Form.Label>
          <Form.Select
            value={newHabit.frequency}
            onChange={(e) =>
              setNewHabit({ ...newHabit, frequency: e.target.value })
            }
          >
            <option>Daily</option>
            <option>Weekly</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Category</Form.Label>
          <Form.Select
            value={newHabit.category}
            onChange={(e) =>
              setNewHabit({ ...newHabit, category: e.target.value })
            }
          >
            <option>Fitness</option>
            <option>Mental Health</option>
            <option>Productivity</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Start Date</Form.Label>
          <Form.Control
            type="date"
            value={newHabit.startDate}
            onChange={(e) =>
              setNewHabit({ ...newHabit, startDate: e.target.value })
            }
            required
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Save Habit
        </Button>
        <Button
          variant="secondary"
          className="ms-2"
          onClick={() => navigate("/dashboard")}
        >
          Cancel
        </Button>
      </Form>
    </div>
  );
}

export default AddHabit;
