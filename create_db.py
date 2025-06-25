import sqlite3

conn = sqlite3.connect("faqs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

# Insert sample Q&A
faqs = [
    ("What is Qonnect?", "Qonnect is an AI-powered support assistant."),
    ("How do I reset my password?", "Go to settings > account > reset password."),
    ("Can I update my email?", "Yes, from your profile settings."),
    ("What is the refund policy?", "You can request a refund within 14 days of purchase.")
]

cursor.executemany("INSERT INTO faqs (question, answer) VALUES (?, ?)", faqs)
conn.commit()
conn.close()

print("Database created and seeded ✅")
