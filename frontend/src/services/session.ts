import { ref } from 'vue'

type Session = {
  user_id: number | null
  username: string | null
}

const userIdKey = 'user_id'
const usernameKey = 'username'

function readSession(): Session {
  const id = localStorage.getItem(userIdKey)
  const username = localStorage.getItem(usernameKey)
  return { user_id: id ? Number(id) : null, username: username || null }
}

const sessionState = ref<Session>(readSession())

export function setSession(user_id: number, username: string) {
  localStorage.setItem(userIdKey, String(user_id))
  localStorage.setItem(usernameKey, username)
  sessionState.value = { user_id, username }
}

export function clearSession() {
  localStorage.removeItem(userIdKey)
  localStorage.removeItem(usernameKey)
  sessionState.value = { user_id: null, username: null }
}

export function useSession() {
  return sessionState
}

