import { api, LoginResponse } from './api'

export async function login(username: string, password: string) {
  return api.post<LoginResponse>('/login/', { username, password })
}

