import type { Categoria } from "./categoria";
import type { UnidadMedida } from "./unidadMedida";

// Mismos campos que ProductoPublic de la API.
export interface Producto {
  id: number;
  nombre: string;
  descripcion: string | null;
  precio_base: number;
  stock_cantidad: number;
  disponible: boolean;
  activo: boolean;
  anulado_at: string | null;
  unidad_venta_id: number;
  unidad_venta: UnidadMedida;
  categorias: Categoria[];
  hay_stock: boolean;
}

// Cuerpo de POST y PUT /api/v1/productos (ProductoCreate / ProductoUpdate de la API).
export interface ProductoCreate {
  nombre: string;
  descripcion: string | null;
  precio_base: number;
  unidad_venta_id: number;
  stock_cantidad: number;
  disponible: boolean;
}
