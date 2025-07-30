# It's all about the 'frontend'  -- Setup and File Structure

Here I have explained how to set up and run the frontend of the projet

---
## To setup the Vite + vue3 enviourment 

```bash
mkdir frontend
cd frontend
npm create vite@latest . -- --template vue
```

## Terminal 1 : To run the node server
```bash
npm install
#or
npm i

# Compile and Hot Reload
npm run dev
```

### File Structure:

```
frontend/
├── .gitignore                              # Git ignored files and folders
├── vite.config.js                          # Vite configuration file ; here the port, poxy and alias are defined
├── README.md                               # Frontend readme (this file)
├── package.json                            # Project metadata and dependencies 
├── package-lock.json                       # Dependency tree lock (auto-generated)
├── index.html                              # Main HTML entry point
├── public/                                 # Static public assets
│   └── vite.svg                            # Vite logo; used in <title> tag of index.html
├── src/                                    # Main source code
│   ├── App.vue                             # Root Vue component
│   ├── main.js                             # JS entry point
│   ├── style.css                           # Global styles
│   ├── api/                   
│   │   └── axios.js                        # Axios instance setup; axiosPublic and axiosPrivate is defined here
│   ├── assets/                             # Static resources (images/icons)
│   │   ├── logo.png
│   │   └── vue.svg
│   ├── constants/             
│   │   └── appInfo.js                      # Application metadata and constants; APPNAME is defined here 
│   ├── globalComponents/                   # Reusable components
│   │   ├── Admin/                          # Nothing is here
│   │   ├── User/                           # Nothing is in here
│   │   ├── Footers.vue                     # Footer component
│   │   ├── Header.vue                      # Header component
│   │   └── UseAuth.js                      # Contains logout function
│   ├── routes/                
│   │   ├── admin.js                        # Routes only accesable to Admin
│   │   ├── user.js                         # Routes only accesable to User
│   │   └── index.js                        # Routes useable for everyone; No authentication needed
│   ├── store/                 
│   │   └── authStore.js                    # Pinia store; Auth-related state management
│   ├── views/                              # Page views 
|   |   ├── HomeView/
│   |   |   └── HomeView.vue                # This is the page we'll see when running app at the begining
|   │   ├── AuthView/
|   |   │   ├── AuthFormView.vue            # This is the PAge being used fo both Login and Register
|   |   │   └── Components/
|   |   |      └── DynamicForm.vue          # Renders the form dynamically
│   |   ├── admin/
|   |   |   ├── DashboardView.vue           # This is the page used for Admin Dashboard
│   |   |   ├── UserView.vue                # This is the page used to view User Card under the Dashboard
│   |   |   ├── SubjectView.vue             # This is the page used to view Subject Card under the Dashboard
│   |   |   ├── ChapterView.vue             # This is the page used to view Chapter paga under each Subjects
│   |   |   ├── QuizView.vue                # This is the page used to view Quiz Card under the Dashboard
│   |   |   ├── QuestionView.vue            # This is the page used to view Questions under each quizzes
│   |   |   ├── AnalyticsView.vue           # This is the page used to view Analystics Card under the Dashboard
│   |   |   └── Components/
│   |   |       ├── AddQuestionView.vue     # This is to handel the modal required for Adding/Edditing Questions
│   |   |       ├── AddSubjectView.vue      # This is to handel the modal required for Adding/Edditing Subjects
│   |   |       ├── ChapterModalView.vue    # This is to handel the modal required for Adding/Edditing Chapters
│   |   |       └── QuizModalView.vue       # This is to handel the modal required for Adding/Edditing Quizzes
│   |   └─ user/
│   |   |  ├── ProfileView.vue              # This is the page used to view User's profile
│   |   |  ├── DashboardView/               # This page is used as User Dashboard; Shows available quizzes & allows subject-wise filters
│   |   |  │    └── DashboardView.vue
│   |   |  └── QuizView/
│   |   |       ├── QuizLandingView.vue     # Shows quizzes info before starting
│   |   |       ├── QuizQuestionView.vue    # Shows the questions; Timer is working in this page
│   |   |       ├── QuizResultView.vue      # After submission this page shows the Result
|   |   |       └── UseStartQuiz.js         # Pevent duplicate submission and unauthorized access

