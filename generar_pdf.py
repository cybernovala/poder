from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
import locale
import io

def generar_pdf(data):
    # Establecer locale en español
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except:
            locale.setlocale(locale.LC_TIME, '')  # fallback al del sistema

    pdf = FPDF()
    pdf.add_page()

    # Título centrado
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "PODER SIMPLE", ln=True, align="C")
    pdf.ln(10)

    # Cuerpo justificado
    pdf.set_font("Arial", "", 14)
    texto = f"""
YO, {data['autorizador']}, RUT {data['rut_autorizador']}, 
AUTORIZO A {data['autorizado']}, RUT {data['rut_autorizado']}, 
PARA REALIZAR EL SIGUIENTE TRÁMITE: {data['tramite']}.
"""

    pdf.multi_cell(0, 10, texto.strip(), align="J")

    # Fecha en español, capitalizada
    pdf.ln(20)
    fecha_actual = datetime.now().strftime("Los Ángeles, %-d de %B de %Y").capitalize()
    pdf.cell(0, 10, fecha_actual, ln=True, align="R")

    # Generar PDF en memoria
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    buffer = io.BytesIO(pdf_bytes)

    # Proteger con contraseña
    reader = PdfReader(buffer)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt("@@1234@@")

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
