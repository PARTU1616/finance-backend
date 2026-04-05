<template>
  <q-page class="q-pa-md">
    <div class="row items-center justify-between q-mb-md">
      <div class="text-h4">Users</div>
      <div class="row q-gutter-sm">
        <q-input v-model="search" placeholder="Search email..." outlined dense @keyup.enter="fetchUsers">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-btn color="primary" label="Add User" icon="add" @click="showCreateDialog" />
      </div>
    </div>

    <!-- Table -->
    <q-table
      :rows="users"
      :columns="columns"
      row-key="id"
      :loading="loading"
      :pagination="pagination"
      @request="onRequest"
    >
      <template v-slot:body-cell-status="props">
        <q-td :props="props">
          <q-badge :color="props.row.status === 'active' ? 'green' : 'grey'">
            {{ props.row.status }}
          </q-badge>
        </q-td>
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn flat dense icon="edit" color="primary" @click="editUser(props.row)" />
          <q-btn 
            v-if="props.row.status === 'active'" 
            flat 
            dense 
            icon="block" 
            color="negative" 
            @click="deactivateUser(props.row)" 
          />
        </q-td>
      </template>
    </q-table>

    <!-- Create/Edit Dialog -->
    <q-dialog v-model="showDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ editMode ? 'Edit User' : 'Add User' }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveUser">
            <q-input 
              v-model="form.email" 
              label="Email" 
              type="email" 
              outlined 
              dense 
              class="q-mb-md" 
              :rules="[val => !!val || 'Email is required']" 
            />
            
            <q-input 
              v-if="!editMode"
              v-model="form.password" 
              label="Password" 
              type="password" 
              outlined 
              dense 
              class="q-mb-md" 
              :rules="[val => !!val || 'Password is required']" 
            />
            
            <q-select 
              v-model="form.role" 
              :options="roleOptions" 
              label="Role" 
              outlined 
              dense 
              class="q-mb-md" 
              :rules="[val => !!val || 'Role is required']" 
            />

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
import { useQuasar } from 'quasar'

export default {
  name: 'UsersPage',
  setup() {
    const $q = useQuasar()
    const users = ref([])
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

    const form = ref({
      id: null,
      email: '',
      password: '',
      role: ''
    })

    const roleOptions = ['Admin', 'Analyst', 'Viewer']

    const columns = [
      { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
      { name: 'email', label: 'Email', field: 'email', align: 'left' },
      { name: 'role', label: 'Role', field: 'role', align: 'left' },
      { name: 'status', label: 'Status', field: 'status', align: 'left' },
      { 
        name: 'created_at', 
        label: 'Created', 
        field: 'created_at', 
        align: 'left',
        format: val => new Date(val).toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short', 
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      },
      { name: 'actions', label: 'Actions', align: 'center' }
    ]

    const fetchUsers = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.value.page,
          limit: pagination.value.rowsPerPage
        }

        if (search.value) params.search = search.value

        const response = await api.get('/users/list/', { params })
        if (response.data.ok) {
          users.value = response.data.users
          pagination.value.rowsNumber = response.data.total_count
        }
      } catch (error) {
        $q.notify({ type: 'negative', message: 'Failed to fetch users' })
      }
      loading.value = false
    }

    const onRequest = (props) => {
      pagination.value = props.pagination
      fetchUsers()
    }

    const showCreateDialog = () => {
      editMode.value = false
      form.value = {
        id: null,
        email: '',
        password: '',
        role: ''
      }
      showDialog.value = true
    }

    const editUser = (user) => {
      editMode.value = true
      form.value = {
        id: user.id,
        email: user.email,
        password: '',
        role: user.role
      }
      showDialog.value = true
    }

    const saveUser = async () => {
      saving.value = true
      try {
        const endpoint = editMode.value
          ? `/users/update/${form.value.id}/`
          : '/users/create/'

        const payload = editMode.value
          ? { email: form.value.email, role: form.value.role }
          : form.value

        const response = await api.post(endpoint, payload)
        if (response.data.ok) {
          $q.notify({ type: 'positive', message: response.data.msg })
          showDialog.value = false
          fetchUsers()
        }
      } catch (error) {
        $q.notify({ type: 'negative', message: error.response?.data?.msg || 'Failed to save user' })
      }
      saving.value = false
    }

    const deactivateUser = (user) => {
      $q.dialog({
        title: 'Confirm',
        message: `Are you sure you want to deactivate ${user.email}?`,
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          const response = await api.post(`/users/deactivate/${user.id}/`)
          if (response.data.ok) {
            $q.notify({ type: 'positive', message: 'User deactivated' })
            fetchUsers()
          }
        } catch (error) {
          $q.notify({ type: 'negative', message: 'Failed to deactivate user' })
        }
      })
    }

    onMounted(() => {
      fetchUsers()
    })

    return {
      users,
      loading,
      saving,
      showDialog,
      editMode,
      search,
      pagination,
      form,
      roleOptions,
      columns,
      fetchUsers,
      onRequest,
      showCreateDialog,
      editUser,
      saveUser,
      deactivateUser
    }
  }
}
</script>
