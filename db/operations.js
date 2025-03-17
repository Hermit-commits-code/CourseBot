const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./db/database.sqlite');

function addCourse(name, description, callback) {
  const stmt = db.prepare(
    'INSERT INTO courses (name, description) VALUES (?, ?)'
  );
  stmt.run(name, description, function (err) {
    if (err) {
      return callback(err);
    }
    callback(null, this.lastID);
  });
  stmt.finalize();
}

function getAllCourses(callback) {
  db.all('SELECT * FROM courses', [], (err, rows) => {
    if (err) {
      return callback(err);
    }
    callback(null, rows);
  });
}

function updateProgress(courseId, progress, callback) {
  const stmt = db.prepare('UPDATE courses SET progress = ? WHERE id = ?');
  stmt.run(progress, courseId, function (err) {
    if (err) {
      return callback(err);
    }
    callback(null, this.changes);
  });
  stmt.finalize();
}

module.exports = {
  addCourse,
  getAllCourses,
  updateProgress,
};
