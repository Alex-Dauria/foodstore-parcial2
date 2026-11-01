interface NavbarProps {
  onNuevo: () => void;
  deshabilitado: boolean;
}

export default function Navbar({ onNuevo, deshabilitado }: NavbarProps) {
  return (
    <nav className="bg-orange-600 text-white shadow">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <div>
          <h1 className="text-2xl font-bold">Food Store</h1>
          <p className="text-sm text-orange-100">Catálogo de productos</p>
        </div>
        <button
          type="button"
          onClick={onNuevo}
          disabled={deshabilitado}
          className="rounded-lg bg-white px-4 py-2 font-semibold text-orange-700 transition hover:bg-orange-100 disabled:opacity-50 disabled:hover:bg-white"
        >
          + Nuevo producto
        </button>
      </div>
    </nav>
  );
}
