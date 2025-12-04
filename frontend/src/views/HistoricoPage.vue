<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Histórico de Presenças</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-list>
        <ion-item v-for="p in filtradas" :key="p.id">
          <ion-label>
            <h2>{{ p.data }}</h2>
            <p>{{ p.user_username }}</p>
          </ion-label>
        </ion-item>
      </ion-list>
      <ion-refresher slot="fixed" @ionRefresh="onRefresh">
        <ion-refresher-content />
      </ion-refresher>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonLabel, IonRefresher, IonRefresherContent } from '@ionic/vue'
import { listarPresencas } from '@/services/presencas'
import { useSession } from '@/services/session'
import type { Presenca } from '@/services/api'

const session = useSession()
const presencas = ref<Presenca[]>([])

const filtradas = computed(() => {
  if (!session.value.user_id) return presencas.value
  return presencas.value.filter(p => p.user === session.value.user_id)
})

async function carregar() {
  presencas.value = await listarPresencas()
}

function onRefresh(e: CustomEvent) {
  carregar().finally(() => (e.target as any).complete())
}

onMounted(() => {
  carregar()
})
</script>

<style scoped>
</style>

