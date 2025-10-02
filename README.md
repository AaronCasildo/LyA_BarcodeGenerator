# 🏷️ Generador de Códigos de Barras

> Una aplicación de escritorio simple y poderosa para generar códigos de barras EAN-13 en lote con una interfaz gráfica.

![Versión de Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Licencia](https://img.shields.io/badge/licencia-MIT-green)
![Plataforma](https://img.shields.io/badge/plataforma-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## Características

- **Generación Masiva**: Crea cientos de códigos de barras en segundos
- **Formato PNG**: Imágenes de alta calidad listas para imprimir
- **Auto-Organización**: Carpetas automáticas con marca de tiempo para cada lote
- **Progreso en Tiempo Real**: Barra de progreso visual durante la generación
- **Apertura Automática**: Abre automáticamente la carpeta de destino al completar
- **Estándar EAN-13**: Formato de código de barras estándar de la industria con dígito verificador automático

---

## Interfaz Principal
<img width="300" alt="image" src="https://github.com/user-attachments/assets/d8022a8b-8201-4a5f-a08d-a9b44ae7bbef" />

## Códigos de Barras Generados
<img width="300" alt="Code_008" src="https://github.com/user-attachments/assets/ef80aa63-b851-42de-9277-f37b4bafb7da" />

---


## ⚙️ Configuración

La aplicación mantiene configuración interna para:
- Número de códigos de barras a generar
- Ruta de la carpeta de destino

La configuración es por sesión (no persiste entre ejecuciones).

### 📂 Estructura de Salida

Los códigos de barras generados se organizan en carpetas con marca de tiempo:

```
Carpeta_Seleccionada/
└── Barcodes_2025-10-01_14-30-45/
    ├── Code_001.png
    ├── Code_002.png
    ├── Code_003.png
    └── ...
```
---


## 🖥️ Soporte de Plataformas

| Plataforma | Estado | Notas |
|------------|--------|-------|
| Windows | ✅ Soporte Completo | Usa `os.startfile()` para abrir carpetas |
| macOS | ✅ Soporte Completo | Usa el comando `open` |
| Linux | ✅ Soporte Completo | Usa el comando `xdg-open` |


---

## Casos de Uso

- **Retail**: Genera códigos de barras de productos para inventario
- **Eventos**: Crea códigos de barras únicos para boletos
- **Gestión de Activos**: Etiqueta equipos de la empresa
- **Almacenamiento**: Rastrea artículos y ubicaciones
- **Pruebas**: Genera códigos de barras de muestra para desarrollo


---

## Ideas para futuro desarrollo del proyecto

- Agregar diferentes formatos de códigos de barras (QR, Code128, etc.)
- Implementar rangos personalizados de números de códigos
- Agregar exportación a CSV con números de códigos
- Crear funcionalidad de impresión en lote
- Agregar opciones de personalización de códigos (colores, tamaños)

---

<div align="center">

**⭐ Si encuentras este proyecto útil, ¡considera darle una estrella! ⭐**

</div>
