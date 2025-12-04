<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Login</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding">
      <ion-item>
        <ion-input v-model="username" label="Usuário" label-placement="floating" autocomplete="username" />
      </ion-item>
      <ion-item>
        <ion-input v-model="password" type="password" label="Senha" label-placement="floating" autocomplete="current-password" />
      </ion-item>
      <ion-button expand="block" :disabled="loading" @click="onLogin">Entrar</ion-button>
      <ion-toast :is-open="toastOpen" :message="toastMessage" :duration="2500" @didDismiss="toastOpen = false" />
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonItem, IonInput, IonButton, IonToast } from '@ionic/vue'
import { login } from '@/services/auth'
import { setSession } from '@/services/session'

const username = ref('')
const password = ref('')
const loading = ref(false)
const toastOpen = ref(false)
const toastMessage = ref('')
const router = useRouter()

async function onLogin() {
  loading.value = true
  try {
    const res = await login(username.value, password.value)
    setSession(res.user_id, res.username)
    toastMessage.value = res.message
    toastOpen.value = true
    setTimeout(() => router.replace('/presenca'), 300)
  } catch (e: any) {
    const msg = e?.data?.error || 'Falha no login.'
    toastMessage.value = msg
    toastOpen.value = true
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
</style>

