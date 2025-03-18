<template>
  <div>
    <h1>Dashboard</h1>
    <button @click="logout">Logout</button>
    <router-link to="/add-course">Add Course</router-link>
    <!-- Add your dashboard content here -->
  </div>
</template>

<script>
export default {
  name: 'UserDashboard',
  methods: {
    logout() {
      localStorage.removeItem('isAuthenticated');
      this.$router.push('/login');
    },
  },
  mounted() {
    if (localStorage.getItem('isAuthenticated') !== 'true') {
      this.$router.push('/login');
    }
  },
};
</script>
