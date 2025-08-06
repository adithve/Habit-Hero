import { Card, Button, Form, Modal } from "react-bootstrap";
import NavbarComponent from "./NavbarComponent";
import { useNavigate } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";

function Dashboard() {
  const navigate = useNavigate();

  const [habitsData, setHabitsData] = useState([]);
  const [habitStatus, setHabitStatus] = useState({});
  const [notes, setNotes] = useState({});
  const [selectedHabit, setSelectedHabit] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [noteInput, setNoteInput] = useState("");
  const [showEditModal, setShowEditModal] = useState(false);
  const [editHabit, setEditHabit] = useState(null);

  const token = localStorage.getItem("token");
  const name = localStorage.getItem("username");

  const fetchHabits = useCallback(async () => {
    try {
      const response = await fetch("http://localhost:8000/api/habits/", {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      const data = await response.json();
      setHabitsData(data);

      const status = {};
      data.forEach((habit) => {
        status[habit.id] = habit.completed_today;
      });
      setHabitStatus(status);
    } catch (error) {
      console.error("Error fetching habits:", error);
    }
  }, [token]);

  useEffect(() => {
    fetchHabits();
  }, [fetchHabits]);

  const handleToggle = async (habitId) => {
  try {
    const response = await fetch("http://localhost:8000/api/ontoggle/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify({ habit_id: habitId }),
    });

    if (response.ok) {
      const data = await response.json();
      setHabitStatus((prevStatus) => ({
        ...prevStatus,
        [habitId]: data.status === "checked",
      }));
    } else {
      const err = await response.json();
      console.error("Toggle failed:", err);
    }
  } catch (error) {
    console.error("Toggle failed", error);
  }
};


const handleCardClick = (habit) => {
  setSelectedHabit(habit);
  setNoteInput(notes[habit.id] || "");
  setShowModal(true);
};

const handleNoteSave = async () => {
  try {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `http://localhost:8000/api/habit/${selectedHabit.id}/add-note/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ note: noteInput }),
      }
    );

    const data = await response.json(); 
    if (!response.ok) {
      const errorMessage = data.error || "Failed to save note";
      alert(errorMessage);
      return;
    }

    setNotes((prev) => ({
      ...prev,
      [selectedHabit.id]: noteInput,
    }));

    setShowModal(false);
    fetchHabits();

  } catch (error) {
    console.error("Error saving note:", error);
    alert("Something went wrong. Please try again.");
  }
};



  const handleEditClick = (habit) => {
    setEditHabit(habit);
    setShowEditModal(true);
  };

  const handleEditSave = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/habits/${editHabit.id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(editHabit),
      });

      if (response.ok) {
        fetchHabits();
        setShowEditModal(false);
      } else {
        console.error("Error updating habit");
      }
    } catch (error) {
      console.error("Error saving edits:", error);
    }
  };

  const handleDeleteHabit = async (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this habit?");
    if (confirmDelete) {
      try {
        await fetch(`http://localhost:8000/api/delete_habit/${id}/`, {
          method: "DELETE",
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        fetchHabits();
      } catch (error) {
        console.error("Error deleting habit:", error);
      }
    }
  };

  return (
    <div>
      <NavbarComponent />
      <div className="container my-4">
        <h3>Welcome {name}😊</h3>
        <p>{new Date().toLocaleDateString()} — “Small daily improvements are the key to staggering long-term results.”</p>

        <div className="d-flex justify-content-between align-items-center my-3">
          <h5>Your Habits</h5>
          <Button variant="success" onClick={() => navigate("/add-habit")}>
            + Add Habit
          </Button>
        </div>

        <div className="row">
          {habitsData.map((habit) => (
            <div key={habit.id} className="col-md-4 mb-3">
              <Card
                className={`shadow-sm ${habitStatus[habit.id] ? "border-success" : ""}`}
                style={{ cursor: "pointer" }}
                onClick={() => handleCardClick(habit)}
              >
                <Card.Body>
                  <Card.Title>{habit.name}</Card.Title>
                  <Card.Subtitle className="mb-2 text-muted">
                    {habit.category}
                  </Card.Subtitle>
                  
                  {}
          {habit.note_today && (
            <Card.Text className="mt-2 text-secondary">
              <strong>Note:</strong> {habit.note_today}
            </Card.Text>
          )}

                  <Form.Check
                    type="switch"
                    label={habitStatus[habit.id] ? "Completed" : "Not Done"}
                    checked={habitStatus[habit.id] || false}
                    onChange={() => handleToggle(habit.id)}
                    onClick={(e) => e.stopPropagation()}
                  />

                  <div className="mt-3">
                    <div><strong>Start Date:</strong> {habit.start_date}</div>
                    <div><strong>Streak:</strong> {habit.streak} 🔥</div>
                  </div>
                  <div className="d-flex justify-content-between mt-3">
                    <Button
                      variant="outline-primary"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditClick(habit);
                      }}
                    >
                      ✏️ Edit
                    </Button>
                    <Button
                      variant="outline-danger"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteHabit(habit.id);
                      }}
                    >
                      🗑️ Delete
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            </div>
          ))}
        </div>

        {/* Note Modal */}
        <Modal show={showModal} onHide={() => setShowModal(false)}>
          <Modal.Header closeButton>
            <Modal.Title>Add Note</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group>
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={noteInput}
                onChange={(e) => setNoteInput(e.target.value)}
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleNoteSave}>
              Save Note
            </Button>
          </Modal.Footer>
        </Modal>

        {}
        <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
          <Modal.Header closeButton>
            <Modal.Title>Edit Habit</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {editHabit && (
              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Habit Name</Form.Label>
                  <Form.Control
                    type="text"
                    value={editHabit.name}
                    onChange={(e) =>
                      setEditHabit({ ...editHabit, name: e.target.value })
                    }
                  />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Frequency</Form.Label>
                  <Form.Select
                    value={editHabit.frequency}
                    onChange={(e) =>
                      setEditHabit({ ...editHabit, frequency: e.target.value })
                    }
                  >
                    <option>Daily</option>
                    <option>Weekly</option>
                  </Form.Select>
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Category</Form.Label>
                  <Form.Select
                    value={editHabit.category}
                    onChange={(e) =>
                      setEditHabit({ ...editHabit, category: e.target.value })
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
                    value={editHabit.start_date}
                    onChange={(e) =>
                      setEditHabit({ ...editHabit, start_date: e.target.value })
                    }
                  />
                </Form.Group>
              </Form>
            )}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowEditModal(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleEditSave}>
              Save Changes
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    </div>
  );
}

export default Dashboard;
