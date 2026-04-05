<template>
  <q-page class="q-pa-md">
    <div class="row items-center justify-between q-mb-md">
      <div class="text-h4">Transactions</div>
      <q-btn v-if="authStore.canWrite" color="primary" label="Add Transaction" icon="add" @click="showCreateDialog" />
    </div>

    <!-- Filters -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-3">
            <q-input v-model="search" placeholder="Search category..." outlined dense @keyup.enter="fetchTransactions">
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
          <div class="col-12 col-md-2">
            <q-select v-model="filters.type" :options="typeOptions" label="Type" outlined dense clearable />
          </div>
          <div class="col-12 col-md-2">
            <q-input v-model="filters.start_date" label="Start Date" type="date" outlined dense clearable />
          </div>
          <div class="col-12 col-md-2">
            <q-input v-model="filters.end_date" label="End Date" type="date" outlined dense clearable />
          </div>
          <div class="col-12 col-md-3">
            <q-btn color="primary" label="Apply" @click="fetchTransactions" class="full-width" />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Table -->
    <q-table
      :rows="transactions"
      :columns="columns"
      row-key="id"
      :loading="loading"
      :pagination="pagination"
      @request="onRequest"
    >
      <template v-slot:body-cell-amount="props">
        <q-td :props="props">
          <span :class="props.row.type === 'income' ? 'text-green-6' : 'text-red-6'">
            {{ props.row.type === 'income' ? '+' : '-' }}{{ formatCurrency(props.row.amount) }}
          </span>
        </q-td>
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn v-if="authStore.canWrite" flat dense icon="edit" color="primary" @click="editTransaction(props.row)" />
          <q-btn v-if="authStore.canWrite" flat dense icon="delete" color="negative" @click="deleteTransaction(props.row)" />
        </q-td>
      </template>
    </q-table>

    <!-- Create/Edit Dialog -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ editMode ? 'Edit Transaction' : 'Add Transaction' }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveTransaction">
            <q-input v-model.number="form.amount" label="Amount" type="number" step="0.01" outlined dense class="q-mb-md" :rules="[val => val > 0 || 'Amount must be positive']" />
            <q-select v-model="form.type" :options="['income', 'expense']" label="Type" outlined dense class="q-mb-md" :rules="[val => !!val || 'Type is required']" />
            <q-input v-model="form.category" label="Category" outlined dense class="q-mb-md" :rules="[val => !!val || 'Category is required']" />
            <q-input v-model="form.date" label="Date" type="date" outlined dense class="q-mb-md" :rules="[val => !!val || 'Date is required']" />
            <q-input v-model="form.notes" label="Notes" type="textarea" outlined dense class="q-mb-md" />

            <div class="row q-gutter-sm">
              <q-btn type="submit" label="Save" color="primary" :loading="saving" />
              <q-btn label="Cancel" color="grey" flat @click="showDialog = false" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useAuthStore } from 'stores/auth'
import { useQuasar } from 'quasar'

export default {
  name: 'TransactionsPage',
  setup() {
    const $q = useQuasar()
    const authStore = useAuthStore()
    const transactions = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const showDialog = ref(false)
    const editMode = ref(false)
    const search = ref('')
    const pagination = ref({
      page: 1,
      rowsPerPage: 10,
      rowsNumber: 0
    })

    const filters = ref({
      type: null,
      start_date: '',
      end_date: ''
    })

    const form = ref({
      id: null,
      amount: null,
      type: '',
      category: '',
      date: new Date().toISOString().split('T')[0],
      notes: ''
    })

    const typeOptions = ['income', 'expense']

    const columns = [
      { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
      { 
        name: 'date', 
        label: 'Date', 
        field: 'date', 
        align: 'left', 
        sortable: true,
        format: val => new Date(val).toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short', 
          day: 'numeric'
        })
      },
      { name: 'category', label: 'Category', field: 'category', align: 'left' },
      { name: 'amount', label: 'Amount', field: 'amount', align: 'right' },
      { name: 'type', label: 'Type', field: 'type', align: 'left' },
      { name: 'notes', label: 'Notes', field: 'notes', align: 'left' },
      { name: 'actions', label: 'Actions', align: 'center' }
    ]

    const formatCurrency = (amount) => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }

    const fetchTransactions = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.value.page,
          limit: pagination.value.rowsPerPage
        }

        if (search.value) params.category = search.value
        if (filters.value.type) params.type = filters.value.type
        if (filters.value.start_date) params.start_date = filters.value.start_date
        if (filters.value.end_date) params.end_date = filters.value.end_date

        const response = await api.get('/transactions/list/', { params })
        if (response.data.ok) {
          transactions.value = response.data.records
          pagination.value.rowsNumber = response.data.total_count
        }
      } catch (error) {
        $q.notify({ type: 'negative', message: 'Failed to fetch transactions' })
      }
      loading.value = false
    }

    const onRequest = (props) => {
      pagination.value = props.pagination
      fetchTransactions()
    }

    const showCreateDialog = () => {
      editMode.value = false
      form.value = {
        id: null,
        amount: null,
        type: '',
        category: '',
        date: new Date().toISOString().split('T')[0],
        notes: ''
      }
      showDialog.value = true
    }

    const editTransaction = (transaction) => {
      editMode.value = true
      form.value = { ...transaction }
      showDialog.value = true
    }

    const saveTransaction = async () => {
      saving.value = true
      try {
        const endpoint = editMode.value
          ? `/transactions/update/${form.value.id}/`
          : '/transactions/create/'

        const response = await api.post(endpoint, form.value)
        if (response.data.ok) {
          $q.notify({ type: 'positive', message: response.data.msg })
          showDialog.value = false
          fetchTransactions()
        }
      } catch (error) {
        $q.notify({ type: 'negative', message: error.response?.data?.msg || 'Failed to save transaction' })
      }
      saving.value = false
    }

    const deleteTransaction = (transaction) => {
      $q.dialog({
        title: 'Confirm',
        message: 'Are you sure you want to delete this transaction?',
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          const response = await api.post(`/transactions/delete/${transaction.id}/`)
          if (response.data.ok) {
            $q.notify({ type: 'positive', message: 'Transaction deleted' })
            fetchTransactions()
          }
        } catch (error) {
          $q.notify({ type: 'negative', message: 'Failed to delete transaction' })
        }
      })
    }

    onMounted(() => {
      fetchTransactions()
    })

    return {
      authStore,
      transactions,
      loading,
      saving,
      showDialog,
      editMode,
      search,
      pagination,
      filters,
      form,
      typeOptions,
      columns,
      formatCurrency,
      fetchTransactions,
      onRequest,
      showCreateDialog,
      editTransaction,
      saveTransaction,
      deleteTransaction
    }
  }
}
</script>
