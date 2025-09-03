// Import the functions you need from the SDKs you need
import { firebase } from "@react-native-firebase/app";
import auth from "@react-native-firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAefVkU1OukmkOLO2FuNL1BkQke_Jcj5Fg",
  authDomain: "test-40a43.firebaseapp.com",
  databaseURL: "https://test-40a43-default-rtdb.firebaseio.com",
  projectId: "test-40a43",
  storageBucket: "test-40a43.firebasestorage.app",
  messagingSenderId: "353391451443",
  appId: "1:353391451443:web:7fd26ddbe2042aacdb3246"
};

// Initialize Firebase
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

export { auth, firebase };