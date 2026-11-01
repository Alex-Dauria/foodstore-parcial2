// Mismos campos que CategoriaPublic de la API.
export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string | null;
  activo: boolean;
  anulado_at: string | null;
}
