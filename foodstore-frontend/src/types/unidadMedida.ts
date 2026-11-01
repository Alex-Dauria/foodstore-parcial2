export type TipoUnidad = "peso" | "volumen" | "contable";

// Mismos campos que UnidadMedidaPublic de la API.
export interface UnidadMedida {
  id: number;
  nombre: string;
  simbolo: string;
  tipo: TipoUnidad;
}
