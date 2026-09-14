import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class FullRAGGuidePDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, 'Document Q&A RAG Bot - Complete Architecture Guide (Basic to Advance)', border=0, align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_draw_color(220, 220, 220)
            self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
            self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.set_draw_color(220, 220, 220)
        self.line(self.get_x(), self.get_y() - 2, self.get_x() + 190, self.get_y() - 2)
        self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

def clean_text(text):
    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove markdown bold/italic/code tags
    text = text.replace('**', '').replace('*', '').replace('`', '')
    # Remove math symbols and non-ascii characters
    clean = ""
    for ch in text:
        if 32 <= ord(ch) <= 126 or ch in ['\n', '\r', '\t']:
            clean += ch
        elif ch in ['\u2192', '\u2190', '\u21d2']:
            clean += " -> "
        elif ch in ['\u2022', '\u25cf', '\u25aa']:
            clean += "-"
        elif ch in ['\u2018', '\u2019']:
            clean += "'"
        elif ch in ['\u201c', '\u201d']:
            clean += '"'
        elif ch == '\u2013' or ch == '\u2014':
            clean += '-'
    return clean

def build_pdf():
    pdf = FullRAGGuidePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # -------------------------------------------------------------
    # PAGE 1: Professional Cover Page
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.set_y(40)
    
    # Title Box
    pdf.set_font('helvetica', 'B', 26)
    pdf.set_text_color(24, 60, 96) # Deep Navy
    pdf.cell(0, 14, 'Document Q&A RAG Bot', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(40, 120, 180) # Accent Blue
    pdf.cell(0, 10, 'Complete Architecture Guide: From Scratch to Advanced Production', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)
    
    # Divider line
    pdf.set_draw_color(40, 120, 180)
    pdf.set_line_width(0.8)
    pdf.line(pdf.get_x() + 30, pdf.get_y(), pdf.get_x() + 160, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(12)
    
    # Core Specifications Box
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    
    overview_text = (
        "This enterprise engineering guide covers the entire technical architecture "
        "of the Retrieval-Augmented Generation (RAG) system built with Pinecone Serverless "
        "Vector Database, Google Gemini 3.5 Flash, and Streamlit.\n\n"
        "It details everything from basic foundational concepts (chunking, embeddings, "
        "vector search) to advanced production engineering (real-time SSE streaming, "
        "multi-turn context rephrasing, multimodal vision OCR, and automatic rate-limit failovers)."
    )
    pdf.set_x(25)
    pdf.multi_cell(160, 6.5, overview_text, border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(18)
    
    # Tech Stack Badges Box
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(30, 30, 30)
    badges = [
        "Vector Database: Pinecone Cloud Serverless (AWS us-east-1 | 768-dim)",
        "Embedding Model: Google gemini-embedding-001 (Task-Type Specialized)",
        "Generative LLM: Google Gemini 3.5 Flash (SSE Real-Time Streaming)",
        "Vision OCR: Gemini Flash Multimodal Vision (Scanned/Handwritten PDFs)",
        "User Interface: Interactive Web App with Conversational Memory (Streamlit)",
        "Repository: github.com/ANAND9051/rag-bot"
    ]
    
    pdf.set_fill_color(245, 247, 250)
    pdf.set_draw_color(210, 220, 230)
    pdf.rect(25, pdf.get_y(), 160, 48, 'FD')
    pdf.set_y(pdf.get_y() + 4)
    
    for badge in badges:
        pdf.set_x(30)
        pdf.cell(150, 6.5, f"- {badge}", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
    pdf.set_y(240)
    pdf.set_font('helvetica', 'I', 9)
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 6, 'Author & Engineer: Anand | System: rag_bot', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, 'Generated for: Full Stack AI Engineering Reference', border=0, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # -------------------------------------------------------------
    # CONTENT SECTIONS
    # -------------------------------------------------------------
    source_guide_path = r"C:\Users\anand\.gemini\antigravity-cli\brain\daef354f-a8d3-4f1b-bdca-2778743f1255\rag_project_guide_basic_to_advance.md"
    
    with open(source_guide_path, "r", encoding="utf-8") as f:
        content_lines = f.readlines()

    pdf.add_page()
    in_code = False
    in_mermaid = False

    for raw_line in content_lines:
        line = raw_line.rstrip()
        clean = clean_text(line).strip()

        # Skip mermaid diagrams
        if clean.startswith('```mermaid'):
            in_mermaid = True
            continue
        if in_mermaid:
            if clean.startswith('```'):
                in_mermaid = False
            continue

        # Handle code blocks
        if clean.startswith('```'):
            in_code = not in_code
            if in_code:
                pdf.ln(2)
            else:
                pdf.ln(2)
            continue

        if in_code:
            pdf.set_font('courier', '', 8.5)
            pdf.set_text_color(40, 40, 40)
            # Safe print code
            safe_code = clean_text(raw_line).rstrip()
            pdf.set_fill_color(245, 245, 248)
            pdf.cell(0, 4.5, f"  {safe_code}", border=0, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            continue

        # Skip Table of Contents from markdown (we have a cover page)
        if clean.startswith('## Table of Contents') or clean.startswith('## 📑 Table of Contents'):
            continue
        if re.match(r'^\d+\.\s+\[.*\]\(#.*\)', clean):
            continue

        # Headings
        if clean.startswith('# '):
            pdf.ln(6)
            pdf.set_font('helvetica', 'B', 18)
            pdf.set_text_color(24, 60, 96)
            pdf.cell(0, 11, clean[2:], border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
        elif clean.startswith('## '):
            pdf.ln(5)
            pdf.set_font('helvetica', 'B', 13)
            pdf.set_text_color(31, 78, 121)
            pdf.cell(0, 9, clean[3:], border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)
        elif clean.startswith('### '):
            pdf.ln(3.5)
            pdf.set_font('helvetica', 'B', 10.5)
            pdf.set_text_color(50, 90, 130)
            pdf.cell(0, 7, clean[4:], border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)
        # Lists
        elif clean.startswith('- ') or clean.startswith('* '):
            item_text = clean[2:].strip()
            pdf.set_font('helvetica', '', 9.5)
            pdf.set_text_color(35, 35, 35)
            pdf.multi_cell(0, 5, f"  o  {item_text}", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        elif re.match(r'^\d+\.\s', clean):
            match = re.match(r'^(\d+\.\s)', clean)
            prefix = match.group(1)
            item_text = clean[len(prefix):].strip()
            pdf.set_font('helvetica', '', 9.5)
            pdf.set_text_color(35, 35, 35)
            pdf.multi_cell(0, 5, f"  {prefix} {item_text}", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # Horizontal dividers
        elif clean == '---':
            pdf.ln(2)
            pdf.set_draw_color(220, 220, 220)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
            pdf.ln(3)
        # Empty lines
        elif not clean:
            pdf.ln(2.5)
        # Table lines or blockquotes
        elif clean.startswith('|') or clean.startswith('>'):
            clean_tbl = clean.replace('|', '  ').replace('>', '  ').strip()
            if clean_tbl and not clean_tbl.startswith('---'):
                pdf.set_font('helvetica', 'I', 9)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 5, f"    {clean_tbl}", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # Standard paragraph text
        else:
            pdf.set_font('helvetica', '', 9.5)
            pdf.set_text_color(35, 35, 35)
            pdf.multi_cell(0, 5.2, clean, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Save outputs
    output_path1 = "docs/RAG_Bot_Complete_Guide_Basic_to_Advance.pdf"
    output_path2 = "RAG_Bot_Complete_Guide_Basic_to_Advance.pdf"
    pdf.output(output_path1)
    pdf.output(output_path2)
    print(f"[SUCCESS] PDF successfully generated at:\n   1. {output_path1}\n   2. {output_path2}")

if __name__ == "__main__":
    build_pdf()
