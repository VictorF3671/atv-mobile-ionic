<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Marcar Presença</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="ion-padding">
      <div v-if="!session.user_id">
        <ion-button expand="block" router-link="/login">Fazer Login</ion-button>
      </div>
      <div v-else>
        <ion-item>
          <ion-label>Usuário</ion-label>
          <ion-note slot="end">{{ session.username }}</ion-note>
        </ion-item>
        <ion-item>
          <ion-label>Data</ion-label>
          <ion-note slot="end">{{ today }}</ion-note>
        </ion-item>
        <ion-button expand="block" :disabled="loading" @click="marcar">Marcar presença de hoje</ion-button>
        <ion-button expand="block" fill="clear" router-link="/historico">Ver histórico</ion-button>
      </div>
      <ion-toast :is-open="toastOpen" :message="toastMessage" :duration="2500" @didDismiss="toastOpen = false" />
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonItem, IonLabel, IonNote, IonToast } from '@ionic/vue'
import { useSession } from '@/services/session'
import { criarPresenca } from '@/services/presencas'

const session = useSession()
const loading = ref(false)
const toastOpen = ref(false)
const toastMessage = ref('')

const today = computed(() => new Date().toISOString().slice(0, 10))

async function marcar() {
  if (!session.value.user_id) return
  loading.value = true
  try {
    const res = await criarPresenca({ user: session.value.user_id, data: today.value })
    toastMessage.value = `Registrado em ${res.data}`
    toastOpen.value = true
  } catch (e: any) {
    const msg = e?.data?.non_field_errors?.[0] || e?.data?.error || 'Falha ao registrar presença.'
    toastMessage.value = msg
    toastOpen.value = true
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
</style>

