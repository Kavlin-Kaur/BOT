from fpdf import FPDF
from pypdf import PdfReader

# Read Q&A pairs from the text file
qa_pairs = []
with open('qonnect_knowledge_qa.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    q, a = '', ''
    for line in lines:
        if line.startswith('Q: '):
            q = line.strip()
        elif line.startswith('A: '):
            a = line.strip()
            if q and a:
                qa_pairs.append((q, a))
                q, a = '', ''

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', size=12)
pdf.cell(200, 10, txt='Qonnect Knowledge Base - Q&A', ln=True, align='C')
pdf.ln(10)

for i, (q, a) in enumerate(qa_pairs, 1):
    pdf.multi_cell(0, 10, f'{i}. {q}\n   {a}\n')

pdf.output('qonnect_knowledge.pdf')
print('✅ PDF created successfully: qonnect_knowledge.pdf')

# After creating the PDF, extract and print the text for debugging
reader = PdfReader('qonnect_knowledge.pdf')
print('\n--- Extracted PDF Text ---')
for page in reader.pages:
    print(page.extract_text())
print('--- End of Extracted PDF Text ---')
