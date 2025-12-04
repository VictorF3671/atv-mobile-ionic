import { api, User } from './api'

export function listarUsuarios() {
  return api.get<User[]>('/usuarios/')
}

export function criarUsuario(payload: { username: string; email: string; first_name: string; last_name: string; password: string }) {
  return api.post<User>('/usuarios/', payload)
}

export function detalharUsuario(id: number) {
  return api.get<User>(`/usuarios/${id}/`)
}

export function atualizarUsuario(id: number, payload: { username: string; email: string; first_name: string; last_name: string; password: string }) {
  return api.put<User>(`/usuarios/${id}/`, payload)
}

export function atualizarParcialUsuario(id: number, payload: Partial<Omit<User, 'id' | 'is_active'>>) {
  return api.patch<User>(`/usuarios/${id}/`, payload)
}

export function deletarUsuario(id: number) {
  return api.delete<void>(`/usuarios/${id}/`)
}

