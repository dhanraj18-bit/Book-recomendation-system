📚 Book Recommendation System — Vityarthi Project (VIT Bhopal)

This repository contains my Vityarthi Project, developed as part of my academic work at VIT Bhopal University.
It is a Book Recommendation System created using Python and Tkinter, backed by a Collaborative Filtering algorithm based on the Pearson Correlation Coefficient.


---

👨‍🎓 Project Details

Field	Information

Student Name	Dhanraj Chaudhary
Registration Number	25BCE10624
Program	Vityarthi
University	VIT Bhopal University



---

📌 Note on AI Usage

I used AI tools only to add comments in the code for better readability and documentation.
💡 All core logic, design, implementation, dataset selection, and GUI development were done by me.


---

🚀 Project Summary

The system recommends books to a selected user by comparing their ratings with other users.
It uses Collaborative Filtering to identify users with similar preferences and predicts book ratings to suggest the most suitable books.


---

🌟 Features

Simple and modern interface using Tkinter

Dropdown selection for choosing target user

Displays:

Current ratings of the selected user

Most similar users with Pearson correlation score

Top recommended books with predicted ratings


Works fully offline with no external database

Easily expandable dataset



---

🧠 Working Principle

1. Detects similarity between users using Pearson Correlation


2. Calculates weighted score for unrated books based on similar users


3. Ranks books by predicted rating


4. Recommends top results




---

🗂 Dataset Structure

RATINGS_DATA = {
  'User1': {'BookA': rating, 'BookB': rating, ...},
  'User2': {...}
}


---

📁 Project Structure

📁 Book-Recommendation-System
│ 📄 main.py
│ 📄 README.md
│ 📄 LICENSE


---

🖥 How to Run

Prerequisites

Python 3.7 or later


Command

python main.py


---

🔮 Future Enhancements

Add real-time input for new ratings

Connect to database (Firebase / SQL)

Export recommendations to PDF

Add login and personalization

Extend system for movies / music / products



---

🤝 Contributions

Contributions, enhancements, and feature suggestions are welcome.
Feel free to fork this repository and create pull requests.


---

📜 License

This project is shared under the MIT License, with a special note that it was developed as an educational project for the Vityarthi program at VIT Bhopal University.
