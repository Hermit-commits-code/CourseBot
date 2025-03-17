# Course Tracking App Roadmap

## Overview

A Python desktop app for tracking 1500 courses from Udemy, Zenva, etc., designed for a solo user. Features include course management, progress tracking, and a modern GUI. The app uses an in-memory SQLite database with CSV export/import for persistence.

## Phase 1: Setup and Core Structure

- [x] Define modular project structure (UI, data, logic).
- [x] Install Python and libraries (`tkinter`, `sqlite3`).
- [x] Set up an in-memory SQLite database.
- [x] Build a basic GUI with a course list and "Add Course" button.

## Phase 2: Essential Features

- [x] Refine "Add Course" with a dialog for title and platform.
- [x] Add edit and delete functionality.
- [x] Implement progress tracking (manual percentage input).
- [x] Enable search/filter for the course list.

## Phase 3: Usability Enhancements

- [ ] Add notes field per course.
- [ ] Create a simple dashboard (total courses, completion rate).
- [ ] Implement CSV export/import for data persistence.

## Phase 4: Modern Design and Polish

- [ ] Upgrade UI with progress bars, grid layout, and theme toggle (dark/light).
- [ ] Optimize for 1500 courses (e.g., efficient list rendering).
- [ ] Add error handling and user feedback.

## Phase 5: Optional Future Features

- [ ] API integration (e.g., Udemy) for auto-importing courses.
- [ ] Time tracking for study sessions.

## Tech Stack

- **Language**: Python 3.x
- **GUI**: `tkinter` (simple, built-in; `PyQt5` optional later)
- **Database**: `sqlite3` (in-memory)
- **Libraries**: `csv` (for persistence)

## Milestones

1. **Week 1**: Phase 1 (setup).
2. **Week 2-3**: Phase 2 (core features).
3. **Week 4**: Phase 3 (enhancements).
4. **Week 5**: Phase 4 (polish).
