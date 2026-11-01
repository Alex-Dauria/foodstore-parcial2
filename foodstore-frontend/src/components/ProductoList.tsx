import type { Producto } from "../types/producto";
import ProductoCard from "./ProductoCard";

interface ProductoListProps {
  productos: Producto[];
  onEditar: (producto: Producto) => void;
  onCambiarDisponibilidad: (producto: Producto) => void;
  onAnular: (producto: Producto) => void;
}

export default function ProductoList({
  productos,
  onEditar,
  onCambiarDisponibilidad,
  onAnular,
}: ProductoListProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {productos.map((producto) => (
        <ProductoCard
          key={producto.id}
          producto={producto}
          onEditar={onEditar}
          onCambiarDisponibilidad={onCambiarDisponibilidad}
          onAnular={onAnular}
        />
      ))}
    </div>
  );
}
