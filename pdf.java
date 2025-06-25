from fpdf import FPDF

questions = [
    "Where can I download the latest academic calendar?",
    "Who is the HOD of the AI department?",
    "How do I register for backlog exams?",
    "Where is the exam control room located?",
    "What documents are required for bonafide certificate?",
    "Can I get previous year question papers?",
    "What is the grading scheme in this university?",
    "Where can I submit my final year project?",
    "What’s the format for internal viva reports?",
    "Where is the robotics lab located?",
    "How can I get to the main auditorium from E-Block?",
    "Where is the girls’ hostel?",
    "Is the terrace of the library open for students?",
    "Where is the examination center?",
    "Is Jain food available in mess?",
    "How do I change my mess preference?",
    "Are there vegan options in the canteen?",
    "Who is the mess manager?",
    "What’s the weekend mess schedule?",
    "Can I opt out of mess for a month?",
    "How can I apply for hostel leave?",
    "Is laundry service available in hostel?",
    "Who is the warden for girls’ hostel?",
    "Are guests allowed in hostel rooms?",
    "What’s the curfew time in hostels?",
    "How to apply for room change in hostel?",
    "How to join the debate club?",
    "When is the next technical fest?",
    "How do I submit entries for art competitions?",
    "What’s the process to start a new student club?",
    "Where do club meetings happen?",
    "What’s the fine for late return of books?",
    "Can I borrow reference books?",
    "How to reserve a book online?",
    "Is there a digital library available?",
    "Can alumni access the library?",
    "How do I renew my library membership?",
    "Where is the campus clinic?",
    "What’s the contact number of campus doctor?",
    "Is mental health counseling available?",
    "Where to report harassment cases?",
    "Are first aid kits available in classrooms?",
    "How do I get a bus pass?",
    "What time does the last college bus leave?",
    "Is there parking space for two-wheelers?",
    "Are there bus services during semester break?",
    "Who manages the LMS platform?",
    "How to access internal college portal?",
    "Where is the IT helpdesk on campus?",
    "How to connect to college Wi-Fi?",
    "How to print documents in the computer lab?",
    "Where do I get my hall ticket?",
    "What’s the process for getting transcripts?",
    "Who is the exam controller?",
    "Can I view answer sheets after results?",
    "How to request duplicate marksheet?",
    "Where is the registrar office?",
    "Can I change my elective subject?",
    "Who approves scholarship forms?",
    "How to apply for internship NOC?",
    "Who created you, Qonnect?",
    "Can you sing a song for me?",
    "What’s the meaning of life?",
    "Are you single, Qonnect?",
    "What’s your opinion on AI taking over?",
]

# Create the PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Qonnect Bot Mega Question List", ln=True, align='C')
pdf.ln(10)

for i, q in enumerate(questions, 1):
    pdf.multi_cell(0, 10, f"{i}. {q}")

# Save the PDF
pdf.output("qonnect_knowledge_curated.pdf")
print("✅ PDF Created: qonnect_knowledge_curated.pdf")
