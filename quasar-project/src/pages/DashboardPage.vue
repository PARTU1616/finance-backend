<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md">Dashboard</div>

    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-md-4">
        <q-card>
          <q-card-section>
            <div class="text-subtitle2 text-grey-7">Total Income</div>
            <div class="text-h5 text-green-6">{{ formatCurrency(summary.total_income) }}</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card>
          <q-card-section>
            <div class="text-subtitle2 text-grey-7">Total Expenses</div>
            <div class="text-h5 text-red-6">{{ formatCurrency(summary.total_expenses) }}</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card>
          <q-card-section>
            <div class="text-subtitle2 text-grey-7">Net Balance</div>
            <div class="text-h5" :class="summary.net_balance >= 0 ? 'text-green-6' : 'text-red-6'">
              {{ formatCurrency(summary.net_balance) }}
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Recent Transactions</div>
            <q-list separator>
              <q-item v-for="txn in summary.recent_transactions" :key="txn.id">
                <q-item-section>
                  <q-item-label>{{ txn.category }}</q-item-label>
                  <q-item-label caption>{{ formatDate(txn.date) }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label :class="txn.type === 'income' ? 'text-green-6' : 'text-red-6'">
                    {{ txn.type === 'income' ? '+' : '-' }}{{ formatCurrency(txn.amount) }}
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-6">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Category Breakdown</div>
            <q-list separator>
              <q-item v-for="cat in categories" :key="cat.category + cat.type">
                <q-item-section>
                  <q-item-label>{{ cat.category }}</q-item-label>
                  <q-item-label caption>{{ cat.type }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label :class="cat.type === 'income' ? 'text-green-6' : 'text-red-6'">
                    {{ formatCurrency(cat.total) }}
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

export default {
  name: 'DashboardPage',
  setup() {
    const summary = ref({
      total_income: 0,
      total_expenses: 0,
      net_balance: 0,
      recent_transactions: []
    })
    const categories = ref([])

    const formatCurrency = (amount) => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const fetchSummary = async () => {
      try {
        const response = await api.get('/dashboard/summary/')
        if (response.data.ok) {
          summary.value = response.data.data
        }
      } catch (error) {
        console.error('Failed to fetch summary:', error)
      }
    }

    const fetchCategories = async () => {
      try {
        const response = await api.get('/dashboard/category-breakdown/')
        if (response.data.ok) {
          categories.value = response.data.data.categories
        }
      } catch (error) {
        console.error('Failed to fetch categories:', error)
      }
    }

    onMounted(() => {
      fetchSummary()
      fetchCategories()
    })

    return {
      summary,
      categories,
      formatCurrency
    }
  }
}
</script>
