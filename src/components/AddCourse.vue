<template>
  <div>
    <h1>Add Course</h1>
    <form @submit.prevent="addCourse">
      <div>
        <label for="name">Course Name:</label>
        <input type="text" v-model="name" />
      </div>
      <div>
        <label for="platform">Platform:</label>
        <input type="text" v-model="platform" />
      </div>
      <div>
        <label for="instructor">Instructor:</label>
        <input type="text" v-model="instructor" />
      </div>
      <div>
        <label for="category">Category:</label>
        <input type="text" v-model="category" />
      </div>
      <div>
        <label for="progress">Progress:</label>
        <input type="number" v-model="progress" />
      </div>
      <div>
        <label for="startDate">Start Date:</label>
        <input type="date" v-model="startDate" />
      </div>
      <div>
        <label for="completionDate">Completion Date:</label>
        <input type="date" v-model="completionDate" />
      </div>
      <div>
        <label for="courseUrl">Course URL:</label>
        <input type="url" v-model="courseUrl" />
      </div>
      <div>
        <label for="courseNotes">Course Notes:</label>
        <textarea v-model="courseNotes"></textarea>
      </div>
      <div>
        <label for="attachments">Attachments:</label>
        <input type="file" @change="handleFileUpload" multiple />
      </div>
      <div>
        <label for="courseDuration">Course Duration:</label>
        <input type="text" v-model="courseDuration" />
      </div>
      <div>
        <label for="courseDescription">Course Description:</label>
        <textarea v-model="courseDescription"></textarea>
      </div>
      <button type="submit">Add Course</button>
    </form>
  </div>
</template>

<script>
import { addCourse } from '../utils/db';

export default {
  name: 'AddCourse',
  data() {
    return {
      name: '',
      platform: '',
      instructor: '',
      category: '',
      progress: 0,
      startDate: '',
      completionDate: '',
      courseUrl: '',
      courseNotes: '',
      attachments: [],
      courseDuration: '',
      courseDescription: '',
    };
  },
  methods: {
    async addCourse() {
      await addCourse({
        name: this.name,
        platform: this.platform,
        instructor: this.instructor,
        category: this.category,
        progress: this.progress,
        startDate: this.startDate,
        completionDate: this.completionDate,
        courseUrl: this.courseUrl,
        courseNotes: this.courseNotes,
        attachments: this.attachments,
        courseDuration: this.courseDuration,
        courseDescription: this.courseDescription,
      });
      this.$router.push('/dashboard');
    },
    handleFileUpload(event) {
      this.attachments = Array.from(event.target.files);
    },
  },
};
</script>
