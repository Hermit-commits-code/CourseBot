import { openDB } from 'idb';

const dbPromise = openDB('course-tracker', 1, {
  upgrade(db) {
    db.createObjectStore('courses', {
      keyPath: 'id',
      autoIncrement: true,
    });
  },
});

export const addCourse = async (course) => {
  const db = await dbPromise;
  await db.add('courses', course);
};

export const getCourses = async () => {
  const db = await dbPromise;
  return await db.getAll('courses');
};

// Add more functions for editing, deleting, and querying courses
