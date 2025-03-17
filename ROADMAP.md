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

- [x] Add notes field per course.
- [x] Create a simple dashboard (total courses, completion rate).
- [x] Implement CSV export/import for data persistence.

## Phase 4: Persistent Database

- [ ] Modify the database setup to use a file-based SQLite database instead of in-memory.
- [ ] Implement database connection management for persistence.
- [ ] Update existing features to work with the persistent database.

## Phase 5: Modern Design and Polish

- [x] Upgrade UI with progress bars, grid layout, and theme toggle (dark/light).
- [x] Optimize for 1500 courses (e.g., efficient list rendering).
- [x] Add error handling and user feedback.

## Phase 6: Advanced Features

- [ ] User Authentication and Profiles

  - Implement user authentication to allow multiple users to track their courses separately.
  - Add user profiles with customizable settings.

- [ ] Cloud Sync

  - Integrate cloud storage options (e.g., Google Drive, Dropbox) for backing up and syncing the database across devices.

- [ ] Advanced Reporting

  - Generate detailed reports on course progress, time spent, and completion rates.
  - Include graphical representations (charts and graphs) of progress and statistics.

- [ ] Reminders and Notifications
  - Add reminder functionality for upcoming courses or deadlines.
  - Implement notifications for new courses, milestones reached, etc.

## Phase 7: Enhanced API Integrations

- [ ] API Integration for Multiple Platforms

  - Extend API integration to other platforms like Coursera, edX, and LinkedIn Learning.
  - Implement automatic updates for course progress based on API data.

- [ ] Course Recommendations
  - Use machine learning algorithms to recommend new courses based on user interests and progress.

## Phase 8: Mobile App Version

- [ ] Mobile App Development
  - Develop a mobile version of the app using frameworks like Kivy or React Native.
  - Ensure seamless synchronization between the desktop and mobile versions.

## Phase 9: Community Features

- [ ] Social Features
  - Add social features like course sharing, discussions, and study groups.
  - Implement a community leaderboard for friendly competition.

## Phase 10: Performance Optimization and Scalability

- [ ] Database Optimization

  - Optimize the database for faster query performance and scalability.
  - Consider moving to a more robust database solution (e.g., PostgreSQL) for large-scale data.

- [ ] Codebase Refactoring
  - Continuously refactor the codebase for maintainability, readability, and efficiency.
  - Implement automated testing and CI/CD pipelines for streamlined development.

## Phase 11: Accessibility and Internationalization

- [ ] Accessibility Enhancements

  - Ensure the app meets accessibility standards (e.g., WCAG).
  - Add keyboard navigation, screen reader support, and other accessibility features.

- [ ] Internationalization (i18n)
  - Add support for multiple languages to reach a global audience.
  - Implement localization (l10n) for region-specific customizations.

## Tech Stack

- **Language**: Python 3.x
- **GUI**: `tkinter` (simple, built-in; `PyQt5` optional later)
- **Database**: `sqlite3` (persistent file-based)
- **Libraries**: `csv` (for persistence)

## Milestones

1. **Week 1**: Phase 1 (setup).
2. **Week 2-3**: Phase 2 (core features).
3. **Week 4**: Phase 3 (enhancements).
4. **Week 5**: Phase 4 (persistent database).
5. **Week 6**: Phase 5 (polish).
6. **Week 7-8**: Phase 6 (advanced features).
7. **Week 9-10**: Phase 7 (enhanced API integrations).
8. **Week 11-12**: Phase 8 (mobile app version).
9. **Week 13-14**: Phase 9 (community features).
10. **Week 15-16**: Phase 10 (performance optimization).
11. **Week 17**: Phase 11 (accessibility and internationalization).
