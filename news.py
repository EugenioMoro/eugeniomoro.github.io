from datetime import datetime
import os

def get_date():
    choice = input("Use today's date? (y/n): ").strip().lower()
    if choice == 'y':
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S%z'), datetime.now().strftime('%Y%m%d_%H%M%S')
    else:
        year = input("Enter year (YYYY): ").strip()
        month = input("Enter month (MM): ").strip().zfill(2)
        day = input("Enter day (DD): ").strip().zfill(2)
        time = input("Enter time (HH:MM:SS) or leave empty for current time: ").strip()
        if not time:
            time = datetime.now().strftime('%H:%M:%S')
        full_date = f"{year}-{month}-{day} {time}"
        return full_date, f"{year}{month}{day}_{time.replace(':', '')}"

def get_content():
    print("Enter the content of the news (end with an empty line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

def generate_news():
    date, filename_date = get_date()
    content = get_content()
    news_text = f"""---
layout: post
date: {date}
inline: true
related_posts: false
---

{content}
"""
    
    choice = input("Save to file (f) or print on screen (p)? ").strip().lower()
    if choice == 'f':
        os.makedirs("_news", exist_ok=True)
        filename = f"_news/news_{filename_date}.md"
        with open(filename, "w") as f:
            f.write(news_text)
        print(f"News saved to {filename}")
    else:
        print("\nGenerated News:\n")
        print(news_text)

if __name__ == "__main__":
    generate_news()
