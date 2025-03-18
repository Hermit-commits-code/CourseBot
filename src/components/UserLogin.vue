<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" />
      </div>
      <p v-if="errorMessage">{{ errorMessage }}</p>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    login() {
      const storedUsername = localStorage.getItem('username');
      const storedPassword = localStorage.getItem('password');

      if (
        this.username === storedUsername &&
        this.password === storedPassword
      ) {
        localStorage.setItem('isAuthenticated', true);
        this.$router.push('/dashboard');
      } else {
        this.errorMessage = 'Invalid username or password';
      }
    },
  },
  mounted() {
    if (localStorage.getItem('isAuthenticated') === 'true') {
      this.$router.push('/dashboard');
    }
  },
};
</script>
