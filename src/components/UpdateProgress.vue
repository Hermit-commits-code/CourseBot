<template>
  <div>
    <h1>Update Progress</h1>
    <form @submit.prevent="updateProgress">
      <div>
        <label for="courseId">Course ID:</label>
        <input type="number" v-model="courseId" />
      </div>
      <div>
        <label for="progress">Progress:</label>
        <input type="number" v-model="progress" />
      </div>
      <button type="submit">Update Progress</button>
    </form>
  </div>
</template>

<script>
import { updateCourseProgress } from '../utils/db';

export default {
  name: 'UpdateProgress',
  data() {
    return {
      courseId: '',
      progress: 0,
    };
  },
  methods: {
    async updateProgress() {
      await updateCourseProgress(this.courseId, this.progress);
      this.$router.push('/dashboard');
    },
  },
};
</script>
