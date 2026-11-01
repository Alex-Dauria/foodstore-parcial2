import { useEffect, useState } from "react";
import Navbar from "./components/Navbar";
import ProductoList from "./components/ProductoList";
import ProductoModal from "./components/ProductoModal";
import type { Producto, ProductoCreate } from "./types/producto";
import type { UnidadMedida } from "./types/unidadMedida";

const API_URL = "http://localhost:8000/api/v1";

// Saca el mensaje de error de la respuesta de la API ({"detail": "..."}).
async function leerError(respuesta: Response): Promise<string> {
  try {
    const cuerpo: unknown = await respuesta.json();
    if (typeof cuerpo === "object" && cuerpo !== null && "detail" in cuerpo) {
      if (typeof cuerpo.detail === "string") return cuerpo.detail;
      if (Array.isArray(cuerpo.detail)) return "Hay datos inválidos en el formulario";
    }
  } catch {
    // La respuesta no tenía JSON: se usa el mensaje genérico.
  }
  return `Error ${respuesta.status} al comunicarse con la API`;
}

// fetch lanza TypeError cuando no puede conectarse (por ejemplo, backend apagado).
function mensajeDe(err: unknown): string {
  if (err instanceof TypeError) return "No se pudo conectar con la API. ¿Está corriendo el backend?";
  if (err instanceof Error) return err.message;
  return "Error desconocido";
}

// Arma el cuerpo del PUT a partir de un producto, con todos sus campos propios.
function cuerpoDesde(producto: Producto): ProductoCreate {
  return {
    nombre: producto.nombre,
    descripcion: producto.descripcion,
    precio_base: producto.precio_base,
    unidad_venta_id: producto.unidad_venta_id,
    stock_cantidad: producto.stock_cantidad,
    disponible: producto.disponible,
  };
}

export default function App() {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [unidades, setUnidades] = useState<UnidadMedida[]>([]);
  const [modalAbierto, setModalAbierto] = useState(false);
  const [seleccionado, setSeleccionado] = useState<Producto | null>(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function cargarProductos() {
    const respuesta = await fetch(`${API_URL}/productos?limit=50`);
    if (!respuesta.ok) throw new Error(await leerError(respuesta));
    const datos: Producto[] = await respuesta.json();
    setProductos(datos);
  }

  async function cargarUnidades() {
    const respuesta = await fetch(`${API_URL}/unidades-medida`);
    if (!respuesta.ok) throw new Error(await leerError(respuesta));
    const datos: UnidadMedida[] = await respuesta.json();
    setUnidades(datos);
  }

  async function cargarCatalogo() {
    setCargando(true);
    setError(null);
    try {
      await Promise.all([cargarProductos(), cargarUnidades()]);
    } catch (err) {
      setError(mensajeDe(err));
    } finally {
      setCargando(false);
    }
  }

  // Al montar: carga el catálogo y las unidades de medida.
  useEffect(() => {
    cargarCatalogo();
  }, []);

  function abrirAlta() {
    setSeleccionado(null);
    setModalAbierto(true);
  }

  function abrirEdicion(producto: Producto) {
    setSeleccionado(producto);
    setModalAbierto(true);
  }

  function cerrarModal() {
    setModalAbierto(false);
    setSeleccionado(null);
  }

  // Alta (POST) o edición (PUT). Si la API responde error, se lanza para que el modal lo muestre.
  async function guardarProducto(datos: ProductoCreate) {
    const respuesta = await fetch(
      seleccionado ? `${API_URL}/productos/${seleccionado.id}` : `${API_URL}/productos`,
      {
        method: seleccionado ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
      },
    );
    if (!respuesta.ok) throw new Error(await leerError(respuesta));
    await cargarProductos();
    cerrarModal();
  }

  // PUT con disponible invertido.
  async function cambiarDisponibilidad(producto: Producto) {
    try {
      const respuesta = await fetch(`${API_URL}/productos/${producto.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...cuerpoDesde(producto), disponible: !producto.disponible }),
      });
      if (!respuesta.ok) throw new Error(await leerError(respuesta));
      await cargarProductos();
    } catch (err) {
      setError(mensajeDe(err));
    }
  }

  // DELETE: baja lógica en el backend; el producto sale del listado.
  async function anularProducto(producto: Producto) {
    if (!window.confirm(`¿Anular "${producto.nombre}"?`)) return;
    try {
      const respuesta = await fetch(`${API_URL}/productos/${producto.id}`, { method: "DELETE" });
      if (!respuesta.ok) throw new Error(await leerError(respuesta));
      await cargarProductos();
    } catch (err) {
      setError(mensajeDe(err));
    }
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <Navbar onNuevo={abrirAlta} deshabilitado={cargando || error !== null} />

      <main className="mx-auto max-w-6xl px-4 py-8">
        {cargando ? (
          <p className="py-16 text-center text-slate-500">Cargando productos...</p>
        ) : error ? (
          <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-center">
            <p className="font-semibold text-red-700">Ocurrió un error</p>
            <p className="mt-1 text-sm text-red-600">{error}</p>
            <button
              type="button"
              onClick={cargarCatalogo}
              className="mt-4 rounded-lg bg-red-600 px-4 py-2 text-sm text-white transition hover:bg-red-700"
            >
              Reintentar
            </button>
          </div>
        ) : productos.length === 0 ? (
          <div className="rounded-xl border-2 border-dashed border-slate-300 py-16 text-center text-slate-500">
            <p className="font-medium">No hay productos en el catálogo.</p>
            <p className="text-sm">Usá «+ Nuevo producto» para dar de alta el primero.</p>
          </div>
        ) : (
          <ProductoList
            productos={productos}
            onEditar={abrirEdicion}
            onCambiarDisponibilidad={cambiarDisponibilidad}
            onAnular={anularProducto}
          />
        )}
      </main>

      {modalAbierto && (
        <ProductoModal
          producto={seleccionado}
          unidades={unidades}
          onGuardar={guardarProducto}
          onCancelar={cerrarModal}
        />
      )}
    </div>
  );
}
