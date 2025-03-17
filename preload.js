const { contextBridge } = require('electron');
const db = require('./db/operations');

contextBridge.exposeInMainWorld('api', {
  addCourse: (name, description, callback) =>
    db.addCourse(name, description, callback),
  getAllCourses: (callback) => db.getAllCourses(callback),
  updateProgress: (courseId, progress, callback) =>
    db.updateProgress(courseId, progress, callback),
});
