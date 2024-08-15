# Django Product API

Este proyecto es una API de productos desarrollada con Django, que permite la creación, actualización y compra de productos. También incluye funcionalidades como alertas de stock bajo y pruebas unitarias.

## Características

- **Crear Productos:** Añadir nuevos productos con un stock inicial de 100 unidades.
- **Actualizar Productos:** Modificar los detalles de los productos existentes.
- **Comprar Productos:** Reducir el stock al realizar compras.
- **Alertas de Stock Bajo:** Genera una alerta cuando el stock de un producto es inferior a 10 unidades.
- **Pruebas Unitarias:** Pruebas automatizadas para validar la funcionalidad de la API.

## Requisitos Previos

Asegúrate de tener instalados los siguientes requisitos:

- Docker
- Docker Compose (opcional, si usas servicios adicionales como bases de datos)
- Python 3.11 (opcional, si ejecutas localmente)

## Instalación y Configuración

### Clonar el repositorio

```bash
git clone https://github.com/nejicadena/api-examen-3b
cd api-examen-3b
```

## Configuración con Docker

```bash
docker build -t examen-3b .
```

### Construir la imagen Docker:

```bash
docker run -p 8000:8000 examen-3b
```

## Pruebas

```bash
docker run examen-3b python manage.py test
```