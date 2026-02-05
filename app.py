from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
import os
from pathlib import Path
from typing import Dict

from flask import Flask, redirect, render_template, request, session, url_for, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "lualcome-sem-secret")

DATA_DIR = Path("data")
SEQUENCE_FILE = DATA_DIR / "sequence.json"

ISSUER = {
    "razon_social": "LUALCOME SEM",
    "nit": "1081924702",
    "pais": "Colombia",
    "responsable_iva": "No responsable de IVA",
    "actividad_economica": "8020",
}

TAX_RATE = Decimal("19")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


@dataclass
class InvoiceTotals:
    total: Decimal
    base: Decimal
    iva: Decimal


def _to_decimal(value: str, default: Decimal = Decimal("0")) -> Decimal:
    try:
        cleaned = value.replace(",", ".").strip()
        if cleaned == "":
            return default
        return Decimal(cleaned)
    except (InvalidOperation, AttributeError):
        return default


def _calculate_totals(total: Decimal) -> InvoiceTotals:
    if total < 0:
        total = Decimal("0")
    divider = Decimal("1") + (TAX_RATE / Decimal("100"))
    base = (total / divider).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    iva = (total - base).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return InvoiceTotals(total=total, base=base, iva=iva)


def _ensure_sequence_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not SEQUENCE_FILE.exists():
        SEQUENCE_FILE.write_text(json.dumps({"last": 0}), encoding="utf-8")


def _next_invoice_number() -> int:
    _ensure_sequence_file()
    data = json.loads(SEQUENCE_FILE.read_text(encoding="utf-8"))
    last = int(data.get("last", 0))
    next_number = last + 1
    SEQUENCE_FILE.write_text(json.dumps({"last": next_number}), encoding="utf-8")
    return next_number


def _login_required():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return None


def _create_pdf(invoice: Dict[str, str], totals: InvoiceTotals, number: int) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filename = DATA_DIR / f"factura_{number}.pdf"
    pdf = canvas.Canvas(str(filename), pagesize=letter)
    width, height = letter

    y = height - 2 * cm
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(2 * cm, y, "Factura comercial / Cuenta de cobro")

    y -= 1 * cm
    pdf.setFont("Helvetica", 11)
    pdf.drawString(2 * cm, y, f"Razón social: {ISSUER['razon_social']}")
    y -= 0.6 * cm
    pdf.drawString(2 * cm, y, f"NIT: {ISSUER['nit']}")
    y -= 0.6 * cm
    pdf.drawString(2 * cm, y, f"Actividad económica: {ISSUER['actividad_economica']}")
    y -= 0.6 * cm
    pdf.drawString(2 * cm, y, f"Responsable: {ISSUER['responsable_iva']}")

    y -= 1 * cm
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(2 * cm, y, f"Factura No. {number:05d}")
    pdf.drawString(10 * cm, y, f"Fecha: {invoice['fecha_emision']}")

    y -= 1 * cm
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(2 * cm, y, "Detalle de valores")
    y -= 0.7 * cm
    pdf.setFont("Helvetica", 11)
    pdf.drawString(2 * cm, y, f"Valor base: ${totals.base}")
    y -= 0.5 * cm
    pdf.drawString(2 * cm, y, f"IVA ({TAX_RATE}%): ${totals.iva}")
    y -= 0.5 * cm
    pdf.drawString(2 * cm, y, f"Total: ${totals.total}")

    y -= 1.2 * cm
    pdf.setFont("Helvetica", 9)
    legal_text = (
        "Este documento corresponde a una factura comercial / cuenta de cobro.\n"
        "No constituye factura electrónica DIAN.\n"
        "El emisor se encuentra inscrito en el Registro Único Tributario (RUT)."
    )
    for line in legal_text.split("\n"):
        pdf.drawString(2 * cm, y, line)
        y -= 0.4 * cm

    pdf.showPage()
    pdf.save()
    return filename


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        error = "Credenciales inválidas."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    login_check = _login_required()
    if login_check:
        return login_check

    totals = InvoiceTotals(total=Decimal("0"), base=Decimal("0"), iva=Decimal("0"))
    if request.method == "POST":
        total_input = _to_decimal(request.form.get("total", "0"))
        totals = _calculate_totals(total_input)
        invoice_number = _next_invoice_number()
        invoice_data = {
            "numero": invoice_number,
            "fecha_emision": datetime.now().strftime("%Y-%m-%d"),
        }
        session["last_invoice"] = {
            **invoice_data,
            "totals": {k: str(v) for k, v in asdict(totals).items()},
        }
        session["last_pdf"] = str(_create_pdf(invoice_data, totals, invoice_number))

    return render_template(
        "index.html",
        issuer=ISSUER,
        tax_rate=TAX_RATE,
        totals=totals,
        last_invoice=session.get("last_invoice"),
    )


@app.route("/descargar")
def descargar():
    login_check = _login_required()
    if login_check:
        return login_check
    pdf_path = session.get("last_pdf")
    if not pdf_path or not Path(pdf_path).exists():
        return redirect(url_for("index"))
    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
