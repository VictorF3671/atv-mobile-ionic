import { api, Presenca } from './api'

export function listarPresencas() {
  return api.get<Presenca[]>('/presencas/')
}

export function criarPresenca(payload: { user: number; data: string }) {
  return api.post<Presenca>('/presencas/', payload)
}

export function detalharPresenca(id: number) {
  return api.get<Presenca>(`/presencas/${id}/`)
}

export function atualizarPresenca(id: number, payload: { user: number; data: string }) {
  return api.put<Presenca>(`/presencas/${id}/`, payload)
}

export function atualizarParcialPresenca(id: number, payload: Partial<{ user: number; data: string }>) {
  return api.patch<Presenca>(`/presencas/${id}/`, payload)
}

export function deletarPresenca(id: number) {
  return api.delete<void>(`/presencas/${id}/`)
}

