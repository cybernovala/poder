from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io

def generar_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)

    # Título centrado
    pdf.cell(0, 10, "PODER SIMPLE", ln=True, align="C")

    pdf.set_font("Arial", "", 14)
    pdf.ln(10)

    # Texto justificado
    texto = f"""
YO, {data['autorizador']}, RUT {data['rut_autorizador']},
AUTORIZO A {data['autorizado']}, RUT {data['rut_autorizado']},
PARA REALIZAR EL SIGUIENTE TRÁMITE: {data['tramite']}.
"""

    pdf.multi_cell(0, 10, texto.strip(), align="J")

    # Fecha ingresada por el usuario
    pdf.ln(20)
    pdf.cell(0, 10, data['fecha'], ln=True, align="R")

    # Exportar PDF a bytes
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    buffer = io.BytesIO(pdf_bytes)

    # Aplicar contraseña
    reader = PdfReader(buffer)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt("@@1234@@")

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
