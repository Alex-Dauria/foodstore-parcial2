import { useState } from "react";
import type { ChangeEvent, FormEvent } from "react";
import type { Producto, ProductoCreate } from "../types/producto";
import type { UnidadMedida } from "../types/unidadMedida";

interface ProductoModalProps {
  producto: Producto | null; // null = alta, con datos = edición
  unidades: UnidadMedida[];
  onGuardar: (datos: ProductoCreate) => Promise<void>;
  onCancelar: () => void;
}

// Los inputs trabajan con texto; se convierten a número al enviar.
interface FormularioProducto {
  nombre: string;
  descripcion: string;
  precio_base: string;
  unidad_venta_id: string;
  stock_cantidad: string;
  disponible: boolean;
}

const FORMULARIO_VACIO: FormularioProducto = {
  nombre: "",
  descripcion: "",
  precio_base: "",
  unidad_venta_id: "",
  stock_cantidad: "",
  disponible: true,
};

function formularioDesde(producto: Producto): FormularioProducto {
  return {
    nombre: producto.nombre,
    descripcion: producto.descripcion ?? "",
    precio_base: String(producto.precio_base),
    unidad_venta_id: String(producto.unidad_venta_id),
    stock_cantidad: String(producto.stock_cantidad),
    disponible: producto.disponible,
  };
}

const claseInput =
  "mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-200";
const claseLabel = "block text-sm font-medium text-slate-700";

export default function ProductoModal({ producto, unidades, onGuardar, onCancelar }: ProductoModalProps) {
  // Vacío al crear, con los datos del producto al editar.
  const [formulario, setFormulario] = useState<FormularioProducto>(
    producto ? formularioDesde(producto) : FORMULARIO_VACIO,
  );
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function manejarCambio(e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) {
    setFormulario({ ...formulario, [e.target.name]: e.target.value });
  }

  async function manejarEnvio(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setGuardando(true);
    setError(null);
    try {
      await onGuardar({
        nombre: formulario.nombre,
        descripcion: formulario.descripcion.trim() === "" ? null : formulario.descripcion,
        precio_base: Number(formulario.precio_base),
        unidad_venta_id: Number(formulario.unidad_venta_id),
        stock_cantidad: Number(formulario.stock_cantidad), // vacío -> 0
        disponible: formulario.disponible,
      });
      // Si salió bien, App cierra el modal.
    } catch (err) {
      // Un 409 (nombre repetido) u otro error se muestra acá, sin cerrar el modal.
      setError(err instanceof Error ? err.message : "No se pudo guardar el producto");
    } finally {
      setGuardando(false);
    }
  }

  return (
    <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/50 p-4">
      <form onSubmit={manejarEnvio} className="w-full max-w-lg space-y-4 rounded-xl bg-white p-6 shadow-xl">
        <h2 className="text-xl font-semibold text-slate-800">
          {producto ? "Editar producto" : "Nuevo producto"}
        </h2>

        {error && (
          <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>
        )}

        <div>
          <label htmlFor="nombre" className={claseLabel}>
            Nombre
          </label>
          <input
            id="nombre"
            name="nombre"
            value={formulario.nombre}
            onChange={manejarCambio}
            required
            minLength={3}
            className={claseInput}
          />
        </div>

        <div>
          <label htmlFor="descripcion" className={claseLabel}>
            Descripción (opcional)
          </label>
          <textarea
            id="descripcion"
            name="descripcion"
            value={formulario.descripcion}
            onChange={manejarCambio}
            rows={2}
            className={claseInput}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="precio_base" className={claseLabel}>
              Precio base ($)
            </label>
            <input
              id="precio_base"
              name="precio_base"
              type="number"
              min="0"
              step="0.01"
              value={formulario.precio_base}
              onChange={manejarCambio}
              required
              className={claseInput}
            />
          </div>
          <div>
            <label htmlFor="unidad_venta_id" className={claseLabel}>
              Unidad de venta
            </label>
            <select
              id="unidad_venta_id"
              name="unidad_venta_id"
              value={formulario.unidad_venta_id}
              onChange={manejarCambio}
              required
              className={claseInput}
            >
              <option value="">Seleccioná una unidad</option>
              {unidades.map((unidad) => (
                <option key={unidad.id} value={unidad.id}>
                  {unidad.nombre} ({unidad.simbolo})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label htmlFor="stock_cantidad" className={claseLabel}>
            Stock (en la unidad de venta)
          </label>
          <input
            id="stock_cantidad"
            name="stock_cantidad"
            type="number"
            min="0"
            step="0.001"
            placeholder="0"
            value={formulario.stock_cantidad}
            onChange={manejarCambio}
            className={claseInput}
          />
        </div>

        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input
            type="checkbox"
            checked={formulario.disponible}
            onChange={(e) => setFormulario({ ...formulario, disponible: e.target.checked })}
            className="h-4 w-4 accent-orange-600"
          />
          Disponible para la venta
        </label>

        <div className="flex justify-end gap-2 pt-2">
          <button
            type="button"
            onClick={onCancelar}
            disabled={guardando}
            className="rounded-lg border border-slate-300 px-4 py-2 text-slate-700 transition hover:bg-slate-100 disabled:opacity-50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={guardando}
            className="rounded-lg bg-orange-600 px-4 py-2 font-semibold text-white transition hover:bg-orange-700 disabled:opacity-50 disabled:hover:bg-orange-600"
          >
            {guardando ? "Guardando..." : "Guardar"}
          </button>
        </div>
      </form>
    </div>
  );
}
