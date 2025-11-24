import tkinter as tk
from tkinter import ttk, scrolledtext
import math
from collections import defaultdict

# 1. Simulated Dataset (Core Data)
# to ensure positive correlations exist for all unrated books.
RATINGS_DATA = {
    'Dhanraj': {'The Martian': 5, 'Dune': 4, '1984': 1, 'The Road': 2, 'Project Hail Mary': 5,'Harry Potter':4,'Looking for Alaska':5,'it ends with us':1, 'The Hobbit': 5, 'Pride and Prejudice': 1},
    'Shruti': {'The Martian': 4, 'Dune': 5, '1984': 1, 'The Road': 1, 'The Great Gatsby': 4,'Harry Potter':5,'Looking for Alaska':3,'it ends with us':5, 'The Hobbit': 4, 'Gone Girl': 5},
    'Aditya': {'The Martian': 1, 'Dune': 2, '1984': 5, 'The Road': 5, 'The Secret History': 4,'Harry Potter':3,'Looking for Alaska':4,'it ends with us':2, 'Gone Girl': 5, 'Pride and Prejudice': 5},
    'Uttkarsh': {'Dune': 2, '1984': 4, 'The Road': 5, 'Project Hail Mary': 1, 'Moby Dick': 5,'Harry Potter':5,'Looking for Alaska':3,'it ends with us':2, 'The Great Gatsby': 3, 'The Hobbit': 3},
    'Swastik': {'The Martian': 5, 'Dune': 5, 'Project Hail Mary': 4, 'The Great Gatsby': 3, 'Brave New World': 5,'Harry Potter':5,'Looking for Alaska':3,'it ends with us':4, 'Gone Girl': 4, 'Pride and Prejudice': 3},
    'Aarchie': {'1984': 5, 'The Road': 4, 'The Secret History': 5, 'Moby Dick': 4,'Harry Potter':3,'Looking for Alaska':5,'it ends with us':3, 'The Martian': 2, 'The Great Gatsby': 4}
}

# 2. Similarity Calculation (Pearson Correlation)
def pearson_correlation(person1_name, person2_name, data):
    """Calculates the Pearson correlation coefficient between two users."""
    p1 = data.get(person1_name, {})
    p2 = data.get(person2_name, {})
    
    # Find books rated by both users
    sh_items ={}
    for book in p1:
        if book in p2:
            sh_items[book] = 1

    n = len(sh_items)
    if n == 0:
        return 0

    # Calculate sums, sum of squares,and sum of products
    sum1 = sum([p1[book] for book in sh_items])
    sum2 = sum([p2[book] for book in sh_items])

    sum1Sq = sum([pow(p1[book], 2) for book in sh_items])
    sum2Sq = sum([pow(p2[book], 2) for book in sh_items])

    ps = sum([p1[book] * p2[book] for book in sh_items])

    # Calculate Pearson correlation formula
    num = ps - (sum1 * sum2 / n)
    den = math.sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

    if den==0:
        return 0

    return num/den

# 3. Recommendation Function 
def get_recommendations(user_name, data, num_recommendations=10):
    """
    Generates book recommendations for a given user using weighted scores.
    """
    totals = defaultdict(float) # Weighted sum of scores
    simSums = defaultdict(float) # Sum of similarities for normalization
    all_users = list(data.keys())
    
    # Calculate similarity to all other users
    similarities = []
    for other_user in all_users:
        if other_user == user_name:
            continue
        
        similarity = pearson_correlation(user_name, other_user, data)
        if similarity > 0:
             similarities.append((similarity, other_user))
             
             # Calculate weighted scores for unrated books
             for book, rating in data[other_user].items():
                 # Only consider books the target user hasn't rated
                 if book not in data.get(user_name, {}):
                     totals[book] += rating * similarity
                     simSums[book] += similarity

    # 1. Create the normalized list of recommendations: total score / simSums
    rankings = []
    for book, total in totals.items():
        # Ensure simSums[book] is not zero before dividing
        if simSums[book] > 0:
            rankings.append((total / simSums[book], book))

    # Sort the list from highest score to lowest
    rankings.sort(reverse=True)
    
    # 2. Sort the similar users list
    similarities.sort(reverse=True)

    return rankings[:num_recommendations], similarities

# 4. Tkinter Interface Implementation

class BookRecommenderApp:
    def __init__(self, master):
        self.master = master
        master.title("Book Recommendation System")
        master.geometry("800x750") 
        master.config(bg="#f0f0f0")

        # Variables 
        self.user_var = tk.StringVar(master)
        self.user_list = sorted(RATINGS_DATA.keys())
        if self.user_list:
             self.user_var.set(self.user_list[0]) # Default user

        # Styling (Themed Tkinter for better look)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#f0f0f0", font=('Arial', 11))
        style.configure("TButton", font=('Arial', 10, 'bold'), padding=6, foreground="white", background="#4a90e2")
        style.map("TButton", background=[('active', '#357ae8')])

        # Main Frame (Centralized Container)
        main_frame = ttk.Frame(master, padding="20 20 20 20", style="TLabel")
        main_frame.pack(fill='both', expand=True)

        # Title
        ttk.Label(main_frame, text="Collaborative Book Recommender", 
                  font=('Arial', 18, 'bold'), foreground="#333333").pack(pady=(0, 20))
        # Explaining the process visually
        ttk.Label(main_frame, text="[Image of collaborative filtering process]", 
                  font=('Arial', 9, 'italic'), foreground="#666666").pack(pady=5)
        

        # User Selection
        select_frame = ttk.Frame(main_frame, padding="10", style="TLabel")
        select_frame.pack(fill='x', pady=10)

        ttk.Label(select_frame, text="Select Target User:", font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        u_drop = ttk.OptionMenu(select_frame, self.user_var, self.user_var.get(), *self.user_list)
        u_drop.config(width=20)
        u_drop.pack(side=tk.LEFT, padx=10)

        rn_btn = ttk.Button(select_frame, text="Get Recommendations", command=self.run_recommendation, style="TButton")
        rn_btn.pack(side=tk.LEFT, padx=10)

        # +Results Display Frames
        results_frame = ttk.Frame(main_frame, padding="10 0 10 0", style="TLabel")
        results_frame.pack(fill='both', expand=True, pady=10)

        # Current Ratings Display
        ratings_group = ttk.LabelFrame(results_frame, text="1. Current User Ratings", padding="10")
        ratings_group.pack(side=tk.LEFT, fill='both', expand=True, padx=5)
        
        self.ratings_text = scrolledtext.ScrolledText(ratings_group, wrap=tk.WORD, height=8, font=('Arial', 10), bd=2, relief=tk.SUNKEN)
        self.ratings_text.pack(fill='both', expand=True)

        # Similar Users Display
        similar_group = ttk.LabelFrame(results_frame, text="2. Most Similar Users (Pearson Score)", padding="10")
        similar_group.pack(side=tk.LEFT, fill='both', expand=True, padx=5)

        self.similar_text = scrolledtext.ScrolledText(similar_group, wrap=tk.WORD, height=8, font=('Arial', 10), bd=2, relief=tk.SUNKEN)
        self.similar_text.pack(fill='both', expand=True)
        
        # Recommendations Display (Larger section below)
        rec_group = ttk.LabelFrame(main_frame, text="3. Top Book Recommendations (Predicted Rating)", padding="10")
        rec_group.pack(fill='x', pady=10)
        
        self.rec_text = scrolledtext.ScrolledText(rec_group, wrap=tk.WORD, height=10, font=('Arial', 11, 'bold'), bd=2, relief=tk.SUNKEN, foreground="#c0392b")
        self.rec_text.pack(fill='x')
        
        # Run initial recommendation for the default user
        if self.user_list:
            self.run_recommendation()


    def run_recommendation(self):
        """Fetches data from and updates all text areas."""
        user = self.user_var.get()
        if not user:
            return

        # 1. Get Recommendation Results (using global functions/data)
        try:
            # Since get_recommendations default is now 999, this will get all of them
            recommendations, similarities = get_recommendations(user, RATINGS_DATA)
        except Exception as e:
            # Simple error handling for GUI
            self.update_text_area(self.ratings_text, f"Error calculating: {e}")
            self.update_text_area(self.similar_text, "")
            self.update_text_area(self.rec_text, "")
            return

        # 2. Update Current Ratings Text Area
        self.update_current_ratings(user)

        # 3. Update Similar Users Text Area
        similar_output = ""
        if similarities:
            # Used 4 decimal places for more precision in similarity scores
            for score, sim_user in similarities:
                similar_output += f"{sim_user}: {score:.4f}\n" 
        else:
            similar_output = "No users found with positive correlation."
        self.update_text_area(self.similar_text, similar_output)

        # 4. Update Recommendations Text Area
        rec_output = ""
        if recommendations:
            # Used 3 decimal places for predicted scores
            for i, (score, book) in enumerate(recommendations):
                rec_output += f"{i+1}. {book} (Predicted Score: {score:.3f})\n" 
        else:
            rec_output = "No unrated books found to recommend."
        self.update_text_area(self.rec_text, rec_output)


    def update_current_ratings(self, user):
        """for displaying the selected user's existing ratings."""
        ratings_output = f"Ratings for {user}:\n"
        usr_rat = RATINGS_DATA.get(user, {})
        if usr_rat:
            for book, rating in usr_rat.items():
                ratings_output += f"  - {book}: {'★' * rating} ({rating}/5)\n"
        else:
            ratings_output += "No ratings found."
        self.update_text_area(self.ratings_text, ratings_output)


    def update_text_area(self, text_widget, content):
        """to clear and insert new content."""
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, content)

if __name__ == '__main__':
    root = tk.Tk()
    app = BookRecommenderApp(root)
    root.mainloop()

