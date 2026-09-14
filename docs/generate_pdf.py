import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class RAGGuidePDF(FPDF):
    def header(self):
        # Header is skipped on page 1 (cover page)
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, 'Retrieval-Augmented Generation (RAG) Learning Guide', border=0, align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

def clean_markdown_line(line):
    # Remove markdown link syntax [text](url) -> text
    line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
    # Remove code tick marks `text` -> text
    line = line.replace('`', '')
    # Remove bold markers **text** -> text
    line = line.replace('**', '')
    # Remove italic markers *text* -> text
    line = line.replace('*', '')
    
    # Strip emojis and non-ASCII characters to prevent Helvetica font encoding errors
    clean_line = ""
    for char in line:
        if 32 <= ord(char) <= 126:
            clean_line += char
        elif char in ['\n', '\r', '\t']:
            clean_line += char
            
    # Clean up starting lists markers if they are clean_line
    if clean_line.startswith('* ') or clean_line.startswith('- '):
        clean_line = clean_line[2:]
        
    return clean_line.strip()

def build_pdf():
    pdf = RAGGuidePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # -------------------------------------------------------------
    # PAGE 1: Cover Page
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.set_y(60)
    pdf.set_font('helvetica', 'B', 28)
    pdf.set_text_color(31, 78, 121) # Primary Dark Blue
    pdf.cell(0, 15, 'RAG Learning Guide', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, 'A Complete Guide to Retrieval-Augmented Generation', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, 'from Scratch using Python & Gemini API', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    
    pdf.set_y(160)
    pdf.set_font('helvetica', 'I', 10)
    pdf.cell(0, 10, 'Prepared for: AI Automation Engineering Learning', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, 'Created at: C:/Users/anand/rag_bot/docs/', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Files to process in order
    files = [
        ("docs/what_is_this_project.md", "1. What is this Project?"),
        ("docs/technologies_used.md", "2. Technologies & Concepts"),
        ("docs/how_the_code_works.md", "3. Code Walkthrough")
    ]
    
    in_code_block = False
    in_mermaid_block = False
    
    for file_path, title in files:
        if not os.path.exists(file_path):
            print(f"[ERROR] Source file not found: {file_path}")
            continue
            
        # Add new page for each main document section
        pdf.add_page()
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line_str = line.strip()
            
            # --- Skip Mermaid Diagrams ---
            if line_str.startswith('```mermaid'):
                in_mermaid_block = True
                continue
            if in_mermaid_block:
                if line_str.startswith('```'):
                    in_mermaid_block = False
                continue
            
            # --- Handle Python Code Blocks ---
            if line_str.startswith('```'):
                in_code_block = not in_code_block
                continue
                
            if in_code_block:
                # Filter code block lines for safe printable characters
                safe_code_line = ""
                for char in line:
                    if 32 <= ord(char) <= 126 or char in ['\n', '\r', '\t']:
                        safe_code_line += char
                pdf.set_font('courier', '', 9)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(0, 4.5, safe_code_line, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                continue
                
            # --- Handle Normal Markdown Formatting ---
            # 1. Headers
            if line_str.startswith('# '):
                header_text = clean_markdown_line(line_str[2:])
                pdf.ln(5)
                pdf.set_font('helvetica', 'B', 18)
                pdf.set_text_color(31, 78, 121)
                pdf.cell(0, 12, header_text, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(2)
            elif line_str.startswith('## '):
                header_text = clean_markdown_line(line_str[3:])
                pdf.ln(4)
                pdf.set_font('helvetica', 'B', 14)
                pdf.set_text_color(31, 78, 121)
                pdf.cell(0, 10, header_text, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(2)
            elif line_str.startswith('### '):
                header_text = clean_markdown_line(line_str[4:])
                pdf.ln(3)
                pdf.set_font('helvetica', 'B', 11)
                pdf.set_text_color(60, 60, 60)
                pdf.cell(0, 8, header_text, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(1)
            # 2. Lists (Bullet & Numbered)
            elif line_str.startswith('* ') or line_str.startswith('- '):
                list_text = clean_markdown_line(line_str)
                pdf.set_font('helvetica', '', 10)
                pdf.set_text_color(30, 30, 30)
                pdf.multi_cell(0, 5.5, f"  -  {list_text}", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            elif re.match(r'^\d+\.\s', line_str):
                match = re.match(r'^(\d+\.\s)', line_str)
                prefix = match.group(1)
                list_text = clean_markdown_line(line_str[len(prefix):])
                pdf.set_font('helvetica', '', 10)
                pdf.set_text_color(30, 30, 30)
                pdf.multi_cell(0, 5.5, f"  {prefix} {list_text}", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            # 3. Horizontal Lines
            elif line_str == '---':
                pdf.ln(2)
                pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
                pdf.ln(4)
            # 4. Spacing
            elif not line_str:
                pdf.ln(3.5)
            # 5. Regular text / paragraphs
            else:
                para_text = clean_markdown_line(line_str)
                if not para_text:
                    continue
                # Ignore table formatting lines or blockquote syntax
                if para_text.startswith('|') or para_text.startswith('>'):
                    para_text = para_text.replace('|', '').replace('>', '').strip()
                    if not para_text:
                        continue
                pdf.set_font('helvetica', '', 10)
                pdf.set_text_color(30, 30, 30)
                pdf.multi_cell(0, 5.5, para_text, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                
    pdf.output("docs/rag_learning_guide.pdf")
    print("[SUCCESS] PDF Generated at docs/rag_learning_guide.pdf")

if __name__ == "__main__":
    build_pdf()
