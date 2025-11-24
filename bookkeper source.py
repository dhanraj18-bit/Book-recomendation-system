import tkinter as tk
from tkinter import ttk, scrolledtext
import math
from collections import defaultdict

RATINGS_DATA = {
    'Dhanraj': {'The Martian': 5, 'Dune': 4, '1984': 1, 'The Road': 2, 'Project Hail Mary': 5,'Harry Potter':4,'Looking for Alaska':5,'it ends with us':1, 'The Hobbit': 5, 'Pride and Prejudice': 1},
    'Shruti': {'The Martian': 4, 'Dune': 5, '1984': 1, 'The Road': 1, 'The Great Gatsby': 4,'Harry Potter':5,'Looking for Alaska':3,'it ends with us':5, 'The Hobbit': 4, 'Gone Girl': 5},
    'Aditya': {'The Martian': 1, 'Dune': 2, '1984': 5, 'The Road': 5, 'The Secret History': 4,'Harry Potter':3,'Looking for Alaska':4,'it ends with us':2, 'Gone Girl': 5, 'Pride and Prejudice': 5},
    'Uttkarsh': {'Dune': 2, '1984': 4, 'The Road': 5, 'Project Hail Mary': 1, 'Moby Dick': 5,'Harry Potter':5,'Looking for Alaska':3,'it ends with us':2, 'The Great Gatsby': 3, 'The Hobbit': 3},
    'Swastik': {'The Martian': 5, 'Dune': 5, 'Project Hail Mary': 4, 'The Great Gatsby': 3, 'Brave New World': 5,'Harry Potter':5,'Looking for Alaska':3,'it ends with us':4, 'Gone Girl': 4, 'Pride and Prejudice': 3},
    'Aarchie': {'1984': 5, 'The Road': 4, 'The Secret History': 5, 'Moby Dick': 4,'Harry Potter':3,'Looking for Alaska':5,'it ends with us':3, 'The Martian': 2, 'The Great Gatsby': 4}
}

def pearson_correlation(person1_name, person2_name, data):
    p1 = data.get(person1_name, {})
    p2 = data.get(person2_name, {})

    sh_items = {}
    for book in p1:
        if book in p2:
            sh_items[book] = 1

    n = len(sh_items)
    if n == 0:
        return 0

    sum1 = sum([p1[book] for book in sh_items])
    sum2 = sum([p2[book] for book in sh_items])
    sum1Sq = sum([pow(p1[book], 2) for book in sh_items])
    sum2Sq = sum([pow(p2[book], 2) for book in sh_items])
    ps = sum([p1[book] * p2[book] for book in sh_items])

    num = ps - (sum1 * sum2 / n)
    den = math.sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

    if den == 0:
        return 0

    return num / den

def get_recommendations(user_name, data, num_recommendations=10):
    totals = defaultdict(float)
    simSums = defaultdict(float)
    all_users = list(data.keys())

    similarities = []
    for other_user in all_users:
        if other_user == user_name:
            continue
        
        similarity = pearson_correlation(user_name, other_user, data)
        if similarity > 0:
            similarities.append((similarity, other_user))
            for book, rating in data[other_user].items():
                if book not in data.get(user_name, {}):
                    totals[book] += rating * similarity
                    simSums[book] += similarity

    rankings = []
    for book, total in totals.items():
        if simSums[book] > 0:
            rankings.append((total / simSums[book], book))

    rankings.sort(reverse=True)
    similarities.sort(reverse=True)

    return rankings[:num_recommendations], similarities

class BookRecommenderApp:
    def _init_(self, master):
        self.master = master
        master.title("Book Recommendation System")
        master.geometry("800x750")
        master.config(bg="#f0f0f0")

        self.user_var = tk.StringVar(master)
        self.user_list = sorted(RATINGS_DATA.keys())
        if self.user_list:
            self.user_var.set(self.user_list[0])

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#f0f0f0", font=('Arial', 11))
        style.configure("TButton", font=('Arial', 10, 'bold'), padding=6, foreground="white", background="#4a90e2")
        style.map("TButton", background=[('active', '#357ae8')])

        main_frame = ttk.Frame(master, padding="20 20 20 20", style="TLabel")
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="Collaborative Book Recommender", 
                  font=('Arial', 18, 'bold'), foreground="#333333").pack(pady=(0, 20))
        ttk.Label(main_frame, text="[Image of collaborative filtering process]", 
                  font=('Arial', 9, 'italic'), foreground="#666666").pack(pady=5)

        select_frame = ttk.Frame(main_frame, padding="10", style="TLabel")
        select_frame.pack(fill='x', pady=10)

        ttk.Label(select_frame, text="Select Target User:", font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        u_drop = ttk.OptionMenu(select_frame, self.user_var, self.user_var.get(), *self.user_list)
        u_drop.config(width=20)
        u_drop.pack(side=tk.LEFT, padx=10)

        rn_btn = ttk.Button(select_frame, text="Get Recommendations", command=self.run_recommendation, style="TButton")
        rn_btn.pack(side=tk.LEFT, padx=10)

        results_frame = ttk.Frame(main_frame, padding="10 0 10 0", style="TLabel")
        results_frame.pack(fill='both', expand=True, pady=10)

        ratings_group = ttk.LabelFrame(results_frame, text="1. Current User Ratings", padding="10")
        ratings_group.pack(side=tk.LEFT, fill='both', expand=True, padx=5)
        
        self.ratings_text = scrolledtext.ScrolledText(ratings_group, wrap=tk.WORD, height=8, font=('Arial', 10), bd=2, relief=tk.SUNKEN)
        self.ratings_text.pack(fill='both', expand=True)

        similar_group = ttk.LabelFrame(results_frame, text="2. Most Similar Users (Pearson Score)", padding="10")
        similar_group.pack(side=tk.LEFT, fill='both', expand=True, padx=5)

        self.similar_text = scrolledtext.ScrolledText(similar_group, wrap=tk.WORD, height=8, font=('Arial', 10), bd=2, relief=tk.SUNKEN)
        self.similar_text.pack(fill='both', expand=True)
        
        rec_group = ttk.LabelFrame(main_frame, text="3. Top Book Recommendations (Predicted Rating)", padding="10")
        rec_group.pack(fill='x', pady=10)
        
        self.rec_text = scrolledtext.ScrolledText(rec_group, wrap=tk.WORD, height=10, font=('Arial', 11, 'bold'), bd=2, relief=tk.SUNKEN, foreground="#c0392b")
        self.rec_text.pack(fill='x')
        
        if self.user_list:
            self.run_recommendation()

    def run_recommendation(self):
        user = self.user_var.get()
        if not user:
            return
        try:
            recommendations, similarities = get_recommendations(user, RATINGS_DATA)
        except Exception as e:
            self.update_text_area(self.ratings_text, f"Error calculating: {e}")
            self.update_text_area(self.similar_text, "")
            self.update_text_area(self.rec_text, "")
            return

        self.update_current_ratings(user)

        similar_output = ""
        if similarities:
            for score, sim_user in similarities:
                similar_output += f"{sim_user}: {score:.4f}\n"
        else:
            similar_output = "No users found with positive correlation."
        self.update_text_area(self.similar_text, similar_output)

        rec_output = ""
        if recommendations:
            for i, (score, book) in enumerate(recommendations):
                rec_output += f"{i+1}. {book} (Predicted Score: {score:.3f})\n"
        else:
            rec_output = "No unrated books found to recommend."
        self.update_text_area(self.rec_text, rec_output)

    def update_current_ratings(self, user):
        ratings_output = f"Ratings for {user}:\n"
        usr_rat = RATINGS_DATA.get(user, {})
        if usr_rat:
            for book, rating in usr_rat.items():
                ratings_output += f"  - {book}: {'★' * rating} ({rating}/5)\n"
        else:
            ratings_output += "No ratings found."
        self.update_text_area(self.ratings_text, ratings_output)

    def update_text_area(self, text_widget, content):
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, content)

if _name_ == '_main_':
    root = tk.Tk()
    app = BookRecommenderApp(root)
    root.mainloop()
