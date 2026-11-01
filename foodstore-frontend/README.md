# Food Store — Frontend (Catálogo de Productos)

Interfaz web del Parcial 2 de Programación IV para administrar los productos del catálogo. Hecha con **React + TypeScript** (Vite) y **Tailwind CSS 4**. Consume la API con `fetch` nativo y maneja el estado con `useState` y `useEffect`.

Autor: Alex Pedro Dauria

Repositorio: https://github.com/Alex-Dauria/foodstore-parcial2

## Requisitos

- Node.js 20.19 o superior (o 22.12 o superior) con npm
- El backend (`foodstore-backend`) corriendo en http://localhost:8000

## Instalar y ejecutar

Desde la carpeta `foodstore-frontend/`:

```bash
npm install
npm run dev
```

Abrir http://localhost:5173 en el navegador.

La dirección de la API está en la constante `API_URL` de `src/App.tsx` (`http://localhost:8000/api/v1`). Si el backend corre en otro puerto, hay que cambiarla ahí.

## Qué se puede hacer

- Ver los productos activos con su precio y su stock con el símbolo de la unidad («$ 12,50 / kg», «stock: 3,5 kg») y los indicadores de disponibilidad y de stock.
- **+ Nuevo producto**: abre el modal vacío, con el selector de unidad cargado desde `GET /api/v1/unidades-medida`.
- **Editar**: abre el modal con los datos del producto.
- **Disponibilidad**: pausa o reanuda la venta (PUT con `disponible` invertido).
- **Anular**: baja lógica del producto (DELETE); deja de aparecer en el listado.
- Si la API rechaza el guardado (por ejemplo, 409 por nombre repetido), el mensaje se muestra dentro del modal sin cerrarlo.
- Estados de carga, de error (con botón Reintentar) y de lista vacía.

## Estructura

```
foodstore-frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.tsx          # Barra de navegación con el botón de alta
│   │   ├── ProductoList.tsx    # Recibe Producto[] por props y lo recorre con .map()
│   │   ├── ProductoCard.tsx    # Tarjeta: precio, stock, indicadores y botones
│   │   └── ProductoModal.tsx   # Modal de alta/edición con su formulario
│   ├── types/                  # Producto, UnidadMedida y Categoria (mismos campos que la API)
│   ├── App.tsx                 # Estado del catálogo y llamadas a la API
│   ├── main.tsx
│   └── index.css               # Tailwind y cursor de mano para lo clickeable
├── index.html
├── package.json
└── tsconfig.json               # strict: true
```

El estado vive en `App.tsx`; los componentes hijos reciben los datos y las acciones por props tipadas y no consultan la API por su cuenta.
