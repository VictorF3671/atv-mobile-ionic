const BASE_URL = 'http://127.0.0.1:8000'
const API_PREFIX = 'api'

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

async function request<T>(path: string, options?: { method?: HttpMethod; body?: unknown; headers?: Record<string, string> }) {
  const url = `${BASE_URL}${API_PREFIX}${path}`
  const res = await fetch(url, {
    method: options?.method ?? 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {})
    },
    body: options?.body ? JSON.stringify(options.body) : undefined
  })

  const contentType = res.headers.get('content-type') || ''
  const isJson = contentType.includes('application/json')
  const data = isJson ? await res.json() : null

  if (!res.ok) {
    const error = isJson ? data : { error: res.statusText }
    throw { status: res.status, data: error }
  }

  return data as T
}

export const api = {
  get: <T>(path: string) => request<T>(path, { method: 'GET' }),
  post: <T>(path: string, body: unknown) => request<T>(path, { method: 'POST', body }),
  put: <T>(path: string, body: unknown) => request<T>(path, { method: 'PUT', body }),
  patch: <T>(path: string, body: unknown) => request<T>(path, { method: 'PATCH', body }),
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' })
}

export type LoginResponse = {
  message: string
  user_id: number
  username: string
}

export type User = {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  is_active: boolean
}

export type Presenca = {
  id: number
  user: number
  user_username: string
  data: string
  criado_em: string
}

