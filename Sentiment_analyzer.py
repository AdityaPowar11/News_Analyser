import customtkinter as ctk
from textblob import TextBlob
from newspaper import Article
import nltk
from PIL import Image

nltk.download('punkt')

# Initialize app
ctk.set_appearance_mode("system")  # Supports "light", "dark", and "system"
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("News Summarizer")
root.geometry("900x600")

# Load light and dark mode icons
light_icon = ctk.CTkImage(light_image=Image.open("light.png"), size=(30, 30))
dark_icon = ctk.CTkImage(light_image=Image.open("moon.png"), size=(30, 30))

# Function to toggle between light and dark mode
def toggle_mode():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Dark":
        ctk.set_appearance_mode("light")
        toggle_btn.configure(image=dark_icon)
    else:
        ctk.set_appearance_mode("dark")
        toggle_btn.configure(image=light_icon)

# Summarize function
def summarize():
    url = url_entry.get().strip()
    if not url:
        return

    article = Article(url)
    try:
        article.download()
        article.parse()
        article.nlp()
    except Exception:
        summary_textbox.configure(state="normal")
        summary_textbox.delete("1.0", "end")
        summary_textbox.insert("1.0", "Error processing article. Check the URL.")
        summary_textbox.configure(state="disabled")
        return

    title_entry.configure(state="normal")
    author_entry.configure(state="normal")
    date_entry.configure(state="normal")
    summary_textbox.configure(state="normal")
    sentiment_entry.configure(state="normal")

    title_entry.delete(0, "end")
    title_entry.insert(0, article.title)

    author_entry.delete(0, "end")
    author_entry.insert(0, ", ".join(article.authors))

    date_entry.delete(0, "end")
    date_entry.insert(0, str(article.publish_date) if article.publish_date else "N/A")

    summary_textbox.delete("1.0", "end")
    summary_textbox.insert("1.0", article.summary)

    analysis = TextBlob(article.text)
    sentiment_entry.delete(0, "end")
    sentiment_entry.insert(0, f"Polarity: {'Positive' if analysis.polarity > 0 else 'Negative' if analysis.polarity < 0 else 'Neutral'}")

    title_entry.configure(state="disabled")
    author_entry.configure(state="disabled")
    date_entry.configure(state="disabled")
    summary_textbox.configure(state="disabled")
    sentiment_entry.configure(state="disabled")

# UI Components
frame = ctk.CTkFrame(root, corner_radius=15)
frame.pack(pady=20, padx=20, fill="both", expand=True)

url_label = ctk.CTkLabel(frame, text="Enter URL:")
url_label.pack(pady=5)
url_entry = ctk.CTkEntry(frame, width=700)
url_entry.pack(pady=5)

summarize_btn = ctk.CTkButton(frame, text="Summarize", command=summarize)
summarize_btn.pack(pady=10)

# Toggle mode button at the corner
toggle_btn = ctk.CTkButton(root, text="", image=dark_icon, command=toggle_mode, width=40, height=40)
toggle_btn.place(relx=0.95, rely=0.05, anchor="ne")

title_label = ctk.CTkLabel(frame, text="Title:")
title_label.pack(pady=5)
title_entry = ctk.CTkEntry(frame, width=700, state="disabled")
title_entry.pack(pady=5)

author_label = ctk.CTkLabel(frame, text="Authors:")
author_label.pack(pady=5)
author_entry = ctk.CTkEntry(frame, width=700, state="disabled")
author_entry.pack(pady=5)

date_label = ctk.CTkLabel(frame, text="Publication Date:")
date_label.pack(pady=5)
date_entry = ctk.CTkEntry(frame, width=700, state="disabled")
date_entry.pack(pady=5)

summary_label = ctk.CTkLabel(frame, text="Summary:")
summary_label.pack(pady=5)
summary_textbox = ctk.CTkTextbox(frame, width=700, height=200, state="disabled")
summary_textbox.pack(pady=5)

sentiment_label = ctk.CTkLabel(frame, text="Sentiment Analysis:")
sentiment_label.pack(pady=5)
sentiment_entry = ctk.CTkEntry(frame, width=700, state="disabled")
sentiment_entry.pack(pady=5)

root.mainloop()
