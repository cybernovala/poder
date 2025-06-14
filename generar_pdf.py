from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io

def generar_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Título
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "PODER SIMPLE", ln=True, align="C")

    # Texto justificado, seguido
    pdf.set_font("Arial", "", 14)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.ln(10)

    texto = (
        f"Yo, {data['autorizador']}, RUT {data['rut_autorizador']}, autorizo a "
        f"{data['autorizado']}, RUT {data['rut_autorizado']}, para realizar el siguiente trámite: "
        f"{data['tramite']}."
    )
    
    pdf.multi_cell(0, 10, texto, align="J")

    # Fecha ingresada por el usuario
    pdf.ln(20)
    pdf.cell(0, 10, data["fecha"], ln=True, align="R")

    # Exportar PDF en memoria
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    buffer = io.BytesIO(pdf_bytes)

    # Protección con contraseña
    reader = PdfReader(buffer)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt("@@1234@@")

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
