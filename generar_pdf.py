from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
import io

def generar_pdf(data):
    try:
        print("📄 Iniciando generación de PDF...")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_xy(10, 20)
        pdf.cell(0, 10, "PODER SIMPLE", ln=True, align="C")

        pdf.set_font("Helvetica", "", 14)
        pdf.ln(10)

        texto = f"""
YO, {data['autorizador']}, RUT {data['rut_autorizador']}, 
AUTORIZO A {data['autorizado']}, RUT {data['rut_autorizado']}, 
PARA REALIZAR EL SIGUIENTE TRÁMITE: {data['tramite']}.
"""
        print("✏️ Texto a incluir:", texto)

        for line in texto.strip().split('\n'):
            pdf.multi_cell(0, 10, line.strip())

        # Fecha final
        fecha_actual = datetime.now().strftime("LOS ÁNGELES, %d DE %B DE %Y").upper()
        pdf.ln(20)
        pdf.cell(0, 10, fecha_actual, ln=True, align="R")

        print("📆 Fecha agregada:", fecha_actual)

        # Guardar PDF en buffer correctamente
        buffer = io.BytesIO()
        pdf.output(buffer, 'F')  # ✅ modo archivo real
        buffer.seek(0)

        print("🔒 Aplicando contraseña...")

        # Aplicar contraseña
        reader = PdfReader(buffer)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt("@@1234@@")
        output = io.BytesIO()
        writer.write(output)

        print("✅ PDF generado con éxito")
        return output.getvalue()

    except Exception as e:
        print("❌ Error interno en generar_pdf:", str(e))
        raise
