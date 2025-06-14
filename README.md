# 📝 Taskify – Your Personal Task Manager

🌐 **Live Demo**: [Click here to try Taskify](https://taskify-cs70.onrender.com/)

## 📌 Introduction

**Taskify** is a simple, web-based Todo List manager built using Flask. It’s designed for anyone who wants a clutter-free way to stay organized whether you're a student, working professional, or just someone trying to plan their day better.

---

## 🎯 Why I Created Taskify

I built **Taskify** out of my own struggle with time management. Between college, personal goals, and side projects, I constantly felt overwhelmed. The apps I tried didn’t work the way I needed. So, I created something simple for me.

But when I shared it with friends, I realized I wasn’t alone. Everyone was fighting the same battle. That’s when Taskify became more than just a personal project it became a tool to help anyone bring order to chaos.

I built Taskify to solve these problems in the simplest way possible  a minimal, fast, and functional task management app that helps you:

- Stay focused  
- Manage tasks based on **priority and due date**  
- Track progress using **Not Started, In Progress, and Completed** status  
- Get things done without the distraction of complex UI  

Whether it’s for managing homework, project tasks, or daily to-dos , Taskify helps bring clarity and control back to your schedule.
Especially **graph-like visualization** helped me see patterns in my productivity when I was most active, where I was falling behind, and how I could better prioritize tasks going forward. It turned abstract to-dos into measurable progress, which kept me motivated.



## ✨ Key Features

Taskify is packed with just the right tools — nothing more, nothing less — to help you stay on track:

- 🔐 **Secure Sign Up & Login** – Every user gets their own private task space.
- 📝 **Personalized Task Lists** – Organize your tasks your way.
- ⏱️ **Priority & Due Date Options** – Focus on what matters, when it matters.
- 🔄 **Status Tracking** – Mark tasks as Not Started, In Progress, or Completed.
- 📊 **Graph-based Visual Stats** – See your progress in charts and gain insight into your productivity.
- 📅 **Calendar View** – Never lose sight of upcoming deadlines.
- 🧼 **Minimal, Distraction-Free UI** – Clean design that keeps you focused.




## 🧑‍💻 Tech Stack

Taskify is built with a focus on simplicity, performance, and rapid development.

| Layer        | Technologies Used            |
| ------------ | ---------------------------- |
| Backend    | Python, Flask                |
| Frontend   | HTML, CSS, Jinja Templates   |
| Database   | SQLite (local) / PostgreSQL (production) |
| Email      | Flask-Mail (Gmail SMTP)      |
| Env Mgmt   | python-dotenv                |
| Others     | Flask-WTF (forms), SQLAlchemy (ORM) |





## 🚀 Installation & Setup

Follow these steps to run **Taskify** on your local machine:

### Clone the Repository

```bash
git clone https://github.com/Beno-Jeffry-B/Mutli-user-TodoList.git
cd Mutli-user-TodoList
```

### Create & Activate a Virtual Environment
# Windows
```
python -m venv venv
venv\Scripts\activate
```
# MacOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Environment Setup
1.Create a .env file in the root directory.

2.Add your config variables like:

```
APP_SECRET_KEY=your_secret_key
DATABASE_URL = your_db_url
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
```

### Run the App Locally
```
python run.py
```
Open your browser and go to:
http://localhost:5000

## 🤝 Contributing

Contributions are welcome! 🎉  
If you find a bug, have a suggestion, or want to improve this project, feel free to:

- Fork the repository
- Create a new branch (`git checkout -b feature-name`)
- Commit your changes (`git commit -m 'Add some feature'`)
- Push to the branch (`git push origin feature-name`)
- Open a Pull Request

Let’s build something better together 🚀

## 🔮 Upcoming updates

Taskify is just getting started. Here’s what’s coming next:

- 📧 **Smart Email Notifications**  
  Get automatic email reminders before task deadlines so you never miss what’s important.

- 👥 **Collaborative Workspaces**  
  Multiple users can log in and manage tasks under a **shared team ID** perfect for group projects.  
  Real-time updates across the team will be enabled using **socket programming**, keeping everyone in sync.

So stay tuned more powerful updates are on the way! 🚀

---









