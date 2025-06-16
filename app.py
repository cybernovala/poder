from flask import Flask, request, send_file
from flask_cors import CORS
from generar_pdf import generar_pdf
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://cybernovala.github.io"}})

@app.route("/generar_poder", methods=["POST"])
def generar_poder():
    try:
        data = request.get_json()
        print("🔍 Datos recibidos:", data)

        pdf_bytes = generar_pdf(data)

        return send_file(
            io.BytesIO(pdf_bytes),
            download_name="poder_simple_cybernova.pdf",
            as_attachment=True,
            mimetype="application/pdf"
        )
    except Exception as e:
        print("❌ Error al generar el PDF:", str(e))
        return {"error": "Fallo interno al generar el PDF"}, 500

if __name__ == "__main__":
    app.run()
