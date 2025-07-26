<template>
  <div class="container py-5" style="font-family: 'Inter', sans-serif;">
    <!-- Header -->
    <div class="mb-4">
      <h2 class="fw-bold text-dark">Manage Users</h2>
      <p class="text-muted">List of all registered users</p>
    </div>

    <!-- Search -->
    <div class="mb-4">
      <div
        class="input-group bg-body-tertiary shadow-sm"
        style="background-color: #f1f3f5; border: 1px solid #ced4da; border-radius: 0.375rem;"
      >
    <span class="input-group-text bg-transparent border-0">
      <i class="bi bi-search text-muted"></i>
    </span>
    <input
      type="text"
      v-model="searchTerm"
      class="form-control bg-transparent border-0"
      placeholder="Search users"
      style="padding: 0.75rem 1rem; font-size: 1rem;"
    />
  </div>
</div>

    <!-- Loading/Error -->
    <div v-if="loading" class="text-center text-muted">Loading users...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="filteredUsers.length === 0" class="text-center text-muted">No users found.</div>
    <!-- Users List -->
    <div v-else >
      <div
        v-for="user in filteredUsers"
        :key="user.id"
        class="d-flex justify-content-between align-items-center mb-4 p-4 shadow-sm rounded-4 border"
      >
        <!-- User Info -->
        <div class="d-flex flex-column gap-2">
          <div class="d-flex align-items-center flex-wrap gap-2">
            <h5 class="mb-0 fw-bold">{{ user.name }}</h5>
            <span
              v-for="role in user.roles"
              :key="role"
              class="badge bg-secondary"
            >
              {{ role }}
            </span>
          </div>
          <small class="text-muted">
            <strong>User ID: {{ user.id }}</strong> <br />
            Email: {{ user.email }}<br />
            Semester: {{ user.semester || 'N/A' }}
          </small>
          <div class="form-check form-switch mt-2">
            <input
              class="form-check-input"
              type="checkbox"
              :checked="user.active"
              :disabled="user.roles.includes('admin')"
              @change="toggleStatus(user)"
            />
            <label class="form-check-label">
              {{ user.active ? 'Active' : 'Inactive' }}
            </label>
          </div>
        </div>

        <!-- Avatar + Delete -->
        <div class="d-flex flex-column align-items-end">
          <img
            :src="generateAvatar(user.name)"
            :alt="user.name"
            class="rounded"
            width="96"
            height="96"
          />
          <button
            @click="deleteUser(user)"
            :disabled="user.roles.includes('admin')"
            class="btn btn-sm btn-outline-danger mt-2"
            title="Delete user"
          >
            <i class="bi bi-trash"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { axiosPrivate } from '@/api/axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

const users = ref([])
const loading = ref(true)
const error = ref(null)
const searchTerm = ref('')

const fetchUsers = async () => {
  try {
    const res = await axiosPrivate.get('/admin/users')
    users.value = res.data
  } catch (err) {
    console.error('Fetch error:', err)
    error.value = 'Failed to load users.'
    toast.error('Failed to load users.')
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)

const filteredUsers = computed(() => {
  return users.value.filter(
    (u) =>
      u.name?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      u.email?.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const toggleStatus = async (user) => {
  if (user.roles.includes('admin')) {
    toast.warning('No alteration with Admin is allowed')
    return
  }
  try {
    const updatedStatus = !user.active
    await axiosPrivate.put(`/admin/users`, { active: updatedStatus, id: user.id })
    user.active = updatedStatus
    toast.success(`User ${user.name} marked as ${updatedStatus ? 'Active' : 'Inactive'}`)
  } catch (err) {
    console.error('Status update failed:', err)
    toast.error('Could not update user status.')
  }
}

const deleteUser = async (user) => {
  if (user.roles.includes('admin')) {
    toast.warning('No alteration with Admin is allowed')
    return
  }
  if (!confirm('Are you sure you want to delete this user?')) return
  try {
    await axiosPrivate.delete(`/admin/users`, { data: { id: user.id } })
    users.value = users.value.filter((u) => u.id !== user.id)
    toast.success('User deleted successfully.')
  } catch (err) {
    console.error('Delete error:', err)
    toast.error('Could not delete user.')
  }
}

const generateAvatar = (name) => {
  const encoded = encodeURIComponent(name)
  return `https://ui-avatars.com/api/?name=${encoded}&background=random&size=128`
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

input:focus {
  box-shadow: none;
}
</style>