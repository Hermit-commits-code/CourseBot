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

export const updateCourseProgress = async (id, progress) => {
  const db = await dbPromise;
  const tx = db.transaction('courses', 'readwrite');
  const store = tx.objectStore('courses');
  const course = await store.get(id);
  course.progress = progress;
  await store.put(course);
  await tx.done;
};
