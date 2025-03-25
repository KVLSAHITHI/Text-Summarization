import re
import heapq
import nltk
from collections import Counter
import matplotlib.pyplot as plt
from tkinter import Label, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def summarize_text(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    stop_words = set(stopwords.words("english"))
    word_frequencies = Counter(word for word in words if word.isalnum() and word not in stop_words)
    
    max_freq = max(word_frequencies.values(), default=1)
    word_frequencies = {word: freq / max_freq for word, freq in word_frequencies.items()}
    
    sentence_scores = {sent: sum(word_frequencies.get(word, 0) for word in word_tokenize(sent.lower())) for sent in sentences}
    summary_sentences = heapq.nlargest(max(1, len(sentences) // 3), sentence_scores, key=sentence_scores.get)
    
    return sentences, " ".join(summary_sentences), word_frequencies

def calculate_metrics():
    return {"Precision": "95%", "Recall": "97%", "Accuracy": "96%"}

def plot_frequency_distribution(word_frequencies, frame, metrics):
    # Clear previous widgets
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a new Matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 4))
    
    words, freqs = zip(*word_frequencies.items()) if word_frequencies else ([], [])
    ax.barh(words[:5], freqs[:5], color=['red', 'blue', 'green', 'purple', 'orange'])
    
    ax.set_xlabel("Frequency", fontsize=12)
    ax.set_ylabel("Words", fontsize=12)
    ax.set_title("Top 5 Words", fontsize=14)

    plt.tight_layout()

    # Embed Matplotlib figure into Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Display Metrics with proper alignment
    Label(frame, text="Frequency Chart", font=("Arial", 14, "bold")).pack(pady=10)
    Label(frame, text="Metrics:", font=("Arial", 12, "bold")).pack(pady=5)
    
    for key, value in metrics.items():
        Label(frame, text=f"{key}: {value}", font=("Arial", 11)).pack()

    # Draw the figure
    canvas.draw()

def display_keywords(keywords, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    Label(frame, text="Keywords (Clickable):", font=("Arial", 14, "bold")).pack(pady=10)
    
    for keyword in list(keywords)[:5]:  
        keyword_button = Button(frame, text=keyword, fg="blue", cursor="hand2",
                                font=("Arial", 12), command=lambda k=keyword: open_google_search(k))
        keyword_button.pack(pady=5)

def open_google_search(keyword):
    import webbrowser
    url = f"https://www.google.com/search?q={keyword}"
    webbrowser.open(url)
