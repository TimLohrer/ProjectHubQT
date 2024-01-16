# ProjectHubQT
A lightweight project manager in PyQt5.
In the following, you will find the documentation of the project ProjectHub. The documentation includes the Database Structure, instructions for usage, and changes deviating from the original plan.

## Table of Contents
- Database Structure
- Instructions on Usage
    - Title Bar
    - Side Bar
    - Workspace
- Changes
    - Components
    - Qt-Designer

- Ressources

## Database Structure
The Database of the Project has the following structure and can be split into three tables:

1. **Project:** Defines the Projects via an ID, Name, and Description. It is mandatory for the Name to be unique. Still, the primary identification is served by the ID column.
2. **User:** Defines the Users via an ID, surname, first name, username, and e-mail. Again, the ID column serves as the main method of identification, although the columns username and e-mail are required to be unique for reasons manifested by the UI.
3. **Task:** Defines the Tasks via an ID, its ProjectID, UserId, creation date, title, description, type, status, priority, UserId of the assigned User, and due date.

## Instructions on Usage
In the following, the instructions on how to use this application will be discussed. The Window can be segregated into three groups: Title Bar, Side Bar, and Workspace.

1. **Title Bar:** On the top of the Window across the entire width.
2. **Side Bar:** On the left of the Window across the entire height.
3. **Workspace:** The rest of the available Window-space.

The groups will be used for orientation in the Window and as references.

You are also provided by default with a Tutorial Project.

### Title Bar
The Title Bar can be dragged when the window is normalizing, by dragging the dark-grey rectangle with one mouse. The buttons on its right control minimizing, normalizing, maximizing, and closing of the window.

### Side Bar
The Side Bar can be further divided into three groups. One at the top, one at the bottom, and one in the middle.

The bottom group shows the current user who is logged in and a button called "Switch Account" which opens a new window in which one can switch users and create a new one. When creating a user it is important that the username and email are not already being used.

In the group in the middle, all projects are listed and a user can navigate to them by left-clicking on them. The currently loaded project is highlighted. When right-clicking a project, the user can change the project or delete it if at least one more projects exist.

The most upper group contains two buttons: "Create Project" which allows the user to create a new project. Make sure that the name is unique. "Create Task" allows the user to create a new task. Here make sure to specify a title and Project. When assigning an assignee to the task make sure you write the exact username.

### Workspace
The Workspace is project-specific and always split into four columns "Backlog," "ToDo," "In Progress," and "Done." These columns help to organize your workflow and make sure that tasks are processed and managed on time. The tasks are displayed in these columns and can be right-clicked to edit the task. Make sure you obey the rules discussed in the Side Bar "Create Task."

## Changes
### Components
The Component System which was proposed in the beginning was developed because it always was vague and the benefit to the user wasn't apparent to us.

### Qt-Designer
Because of the limitations of the Qt-Designer and general problems associated with installing the software, we came to the conclusion that we were better off designing the UI in the code.

## Ressources
Followin ressources were used:
- [Stackoverflow](https://stackoverflow.com/)
- [PythonGUIs](https://www.pythonguis.com/tutorials/custom-title-bar-pyqt6/)
- [PyQT6](https://doc.qt.io/qtforpython-6/)
- [GitHub](https://github.com)
- [Sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [W3Schools](https://www.w3schools.com/MySQL/default.asp)
