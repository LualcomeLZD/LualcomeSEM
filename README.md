# LualcomeSEM
Aplicación web sencilla para calcular facturas de forma rápida desde cualquier dispositivo. Permite ingresar valores, calcular impuestos y totales automáticamente. Pensada para uso práctico diario, especialmente en móviles, sin necesidad de conocimientos técnicos.

## Funcionalidades
- Agrega múltiples productos o servicios con cantidad y precio unitario.
- Calcula subtotal e IVA (por defecto 19% en Colombia), además de descuentos por producto.
- Interfaz adaptada a pantallas pequeñas para uso desde el celular.

## Requisitos
- Python 3.10 o superior.

## Instalación
1. Crea y activa un entorno virtual (opcional, pero recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
1. Ejecuta la app:
   ```bash
   python app.py
   ```
2. Abre `http://localhost:5000` en tu navegador.
3. Ingresa productos, impuestos y descuentos, luego pulsa **Calcular factura**.

## Notas
- Si estás en Windows, activa el entorno virtual con:
  ```bash
  .venv\Scripts\activate
  ```
