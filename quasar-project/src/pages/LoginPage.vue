<template>
  <q-page class="flex flex-center bg-grey-2">
    <q-card class="q-pa-md" style="width: 400px">
      <q-card-section>
        <div class="text-h5 text-center q-mb-md">Finance Dashboard</div>
        <div class="text-subtitle2 text-center text-grey-7">Login to your account</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="handleLogin">
          <q-input
            v-model="email"
            label="Email"
            type="email"
            outlined
            dense
            class="q-mb-md"
            :rules="[val => !!val || 'Email is required']"
          />

          <q-input
            v-model="password"
            label="Password"
            type="password"
            outlined
            dense
            class="q-mb-md"
            :rules="[val => !!val || 'Password is required']"
          />

          <q-btn
            type="submit"
            label="Login"
            color="primary"
            class="full-width"
            :loading="loading"
          />
        </q-form>
      </q-card-section>

      <q-card-section class="text-center text-caption text-grey-7">
        Default: admin@finance.com / admin123
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'stores/auth'

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const email = ref('admin@finance.com')
    const password = ref('admin123')
    const loading = ref(false)

    const handleLogin = async () => {
      loading.value = true
      const result = await authStore.login(email.value, password.value)
      loading.value = false

      if (result.success) {
        router.push('/dashboard')
      }
    }

    return {
      email,
      password,
      loading,
      handleLogin
    }
  }
}
</script>
