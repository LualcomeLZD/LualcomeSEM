# LualcomeSEM
Aplicación web sencilla para calcular facturas de forma rápida desde cualquier dispositivo. Permite ingresar valores, calcular impuestos y totales automáticamente. Pensada para uso práctico diario, especialmente en móviles, sin necesidad de conocimientos técnicos.

## Funcionalidades
- Calcula valor base e IVA desde un total ingresado por el usuario (IVA fijo 19% en backend).
- Genera PDF descargable con datos del emisor, fecha y número consecutivo de factura.
- Interfaz responsive en español, para uso interno de LUALCOME SEM.
- Acceso restringido con login (sin usuarios anónimos).

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
3. Inicia sesión con el usuario administrador.
4. Ingresa el valor total cobrado al cliente y pulsa **Calcular factura**.
5. Descarga el PDF generado.

## Credenciales y configuración
- Usuario y contraseña por defecto:
  - Usuario: `admin`
  - Contraseña: `admin123`
- Puedes sobrescribirlas con variables de entorno:
  - `ADMIN_USER`
  - `ADMIN_PASSWORD`
- La tasa de IVA es fija en el backend (19%) y no es editable desde la interfaz.

## Despliegue en Render
Render usa `gunicorn` para ejecutar la aplicación. Asegúrate de que esté en `requirements.txt` y de incluir el `Procfile` con este contenido:
```text
web: gunicorn app:app
```

## Limitaciones legales
- Este sistema genera facturas comerciales / cuentas de cobro.
- No es facturación electrónica DIAN.
- No integra pagos en línea ni validaciones DIAN.

## Notas
- Si estás en Windows, activa el entorno virtual con:
  ```bash
  .venv\Scripts\activate
  ```
