# Study Planner

**Study Planner** is a web application designed to help students organize their tasks, set goals, and take notes efficiently. The platform offers a user-friendly interface and powerful tools to streamline productivity and time management.

---
#### Video Demo: <https://youtu.be/gEK-pZkLObw?si=Py_1iZk6WPPu6IMm>
## Features

- **Task Management**: Add, edit, view, and delete tasks with priorities, deadlines, and status updates (e.g., to-do, done).
- **Goal Setting**: Define and track progress on personal and academic goals.
- **Notes**: Create, edit, and organize notes to capture ideas and important information.
- **Dashboard**: Access an overview of your tasks, goals, and notes.
- **User Authentication**: Secure registration, login, and session management for personalized scheduling.
- **Responsive Design**: Mobile and desktop-friendly interface.
- **Error Handling**: Flash messages and user-friendly error prompts for a seamless experience.

---

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Authentication**: Secure password hashing using Werkzeug
- **Others**: jQuery, Font Awesome (for icons)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/study-planner.git
   cd study-planner
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create an `instance` folder and initialize the SQLite database:
   ```bash
   mkdir instance
   python app.py
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open the application in your browser:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage

1. **Register**: Create an account using your email, username, and password.
2. **Login**: Access your personalized dashboard.
3. **Dashboard**: View an overview of your tasks, goals, and recent notes.
4. **Manage Tasks**: Add, edit, delete, and update the status of your tasks.
5. **Set Goals**: Define goals and track progress.
6. **Take Notes**: Organize thoughts and important information.

---

## Folder Structure

```
study-planner/
├── app.py                # Main application file
├── models.py             # Database models
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS, images)
├── instance/             # SQLite database location
└── requirements.txt      # Python dependencies
```

---

## Contributions

Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
