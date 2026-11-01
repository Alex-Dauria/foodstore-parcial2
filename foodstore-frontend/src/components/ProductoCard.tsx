import type { Producto } from "../types/producto";

interface ProductoCardProps {
  producto: Producto;
  onEditar: (producto: Producto) => void;
  onCambiarDisponibilidad: (producto: Producto) => void;
  onAnular: (producto: Producto) => void;
}

// Formato argentino: 12.5 -> "12,50" (precio) y 3.5 -> "3,5" (stock).
function formatearPrecio(valor: number): string {
  return valor.toLocaleString("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatearStock(valor: number): string {
  return valor.toLocaleString("es-AR", { maximumFractionDigits: 3 });
}

export default function ProductoCard({
  producto,
  onEditar,
  onCambiarDisponibilidad,
  onAnular,
}: ProductoCardProps) {
  const simbolo = producto.unidad_venta.simbolo;

  return (
    <article className="flex flex-col rounded-xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
      <h2 className="text-lg font-semibold text-slate-800">{producto.nombre}</h2>
      {producto.descripcion && <p className="mt-1 text-sm text-slate-500">{producto.descripcion}</p>}
      {producto.categorias.length > 0 && (
        <p className="mt-1 text-xs text-slate-400">
          {producto.categorias.map((categoria) => categoria.nombre).join(" · ")}
        </p>
      )}

      <p className="mt-3 text-xl font-bold text-orange-700">
        $ {formatearPrecio(producto.precio_base)} / {simbolo}
      </p>
      <p className="text-sm text-slate-600">
        stock: {formatearStock(producto.stock_cantidad)} {simbolo}
      </p>

      <div className="mt-3 flex flex-wrap gap-2 text-xs font-medium">
        <span
          className={`rounded-full px-2 py-1 ${
            producto.disponible ? "bg-green-100 text-green-800" : "bg-slate-200 text-slate-700"
          }`}
        >
          {producto.disponible ? "Disponible" : "Venta pausada"}
        </span>
        <span
          className={`rounded-full px-2 py-1 ${
            producto.hay_stock ? "bg-blue-100 text-blue-800" : "bg-red-100 text-red-800"
          }`}
        >
          {producto.hay_stock ? "Con stock" : "Sin stock"}
        </span>
      </div>

      <div className="mt-4 flex flex-wrap gap-2 border-t border-slate-100 pt-4">
        <button
          type="button"
          onClick={() => onEditar(producto)}
          className="rounded-lg bg-slate-800 px-3 py-1.5 text-sm text-white transition hover:bg-slate-700"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onCambiarDisponibilidad(producto)}
          title={producto.disponible ? "Pausar la venta" : "Reanudar la venta"}
          className="rounded-lg bg-amber-500 px-3 py-1.5 text-sm text-white transition hover:bg-amber-600"
        >
          Disponibilidad
        </button>
        <button
          type="button"
          onClick={() => onAnular(producto)}
          className="rounded-lg bg-red-600 px-3 py-1.5 text-sm text-white transition hover:bg-red-700"
        >
          Anular
        </button>
      </div>
    </article>
  );
}
