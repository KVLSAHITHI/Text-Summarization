import tkinter as tk
from tkinter import scrolledtext, Menu
from summarizer import summarize_text, calculate_metrics, plot_frequency_distribution, display_keywords

def show_main_ui():
    """ Switch from welcome screen to main UI """
    welcome_frame.pack_forget()
    keywords_frame.pack_forget()
    canvas_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def show_keywords():
    """ Switch to the Keywords screen """
    main_frame.pack_forget()
    canvas_frame.pack_forget()
    keywords_frame.pack(fill="both", expand=True)
    
    article_text = text_input.get("1.0", tk.END).strip()
    if article_text:
        _, _, word_frequencies = summarize_text(article_text)
        display_keywords(word_frequencies.keys(), keywords_frame)

def show_graph():
    """ Switch to the Graph screen """
    main_frame.pack_forget()
    keywords_frame.pack_forget()
    canvas_frame.pack(fill="both", expand=True)
    
    article_text = text_input.get("1.0", tk.END).strip()
    if article_text:
        _, _, word_frequencies = summarize_text(article_text)
        metrics = calculate_metrics()
        plot_frequency_distribution(word_frequencies, canvas_frame, metrics)

def summarize_text_gui():
    """ Perform text summarization and display the summary """
    article_text = text_input.get("1.0", tk.END).strip()
    if not article_text:
        return
    
    _, summary, _ = summarize_text(article_text)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, summary)

# Create a Tkinter window
window = tk.Tk()
window.title("Text Summarizer")
window.geometry("900x600")

# ---------------- WELCOME SCREEN ---------------- #
welcome_frame = tk.Frame(window)
welcome_frame.pack(fill="both", expand=True)

welcome_label = tk.Label(
    welcome_frame, text="Welcome to the Text Summarizer!\nClick 'Start' to begin.",
    font=("Arial", 16, "bold"), pady=20
)
welcome_label.pack()

start_button = tk.Button(
    welcome_frame, text="Start", command=show_main_ui, font=("Arial", 14, "bold"), bg="green", fg="white", padx=10, pady=5
)
start_button.pack()

# ---------------- MAIN SCREEN ---------------- #
main_frame = tk.Frame(window)

# Menu Bar (Right-aligned)
menu_bar = Menu(window, tearoff=0)

menu_items = tk.Menu(menu_bar, tearoff=0)
menu_items.add_command(label="Home", command=show_main_ui)
menu_items.add_command(label="Keywords", command=show_keywords)
menu_items.add_command(label="Graph", command=show_graph)

menu_bar.add_cascade(label="☰ Menu", menu=menu_items)
window.config(menu=menu_bar)

# Input Label
label_input = tk.Label(main_frame, text="Enter the text to summarize:", font=("Arial", 12, "bold"))
label_input.pack(pady=(10, 5))

# Text Input Box
text_input = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=10, font=("Arial", 12))
text_input.pack(pady=10, padx=50)

# Output Label
label_output = tk.Label(main_frame, text="Summarized Text:", font=("Arial", 12, "bold"))
label_output.pack(pady=(10, 5))

# Text Output Box
text_output = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=10, font=("Arial", 12))
text_output.pack(pady=10, padx=50)

# Summarize Button
summarize_button = tk.Button(main_frame, text="Summarize", command=summarize_text_gui, bg="orange", font=("Arial", 12))
summarize_button.pack(pady=10)

# ---------------- OTHER PAGES ---------------- #
# Keywords Frame
keywords_frame = tk.Frame(window, padx=20, pady=20)

# Graph Frame
canvas_frame = tk.Frame(window, padx=20, pady=20)

window.mainloop()
