import pyrebase

firebase_config = {
  "apiKey": "APIKEY",
  "authDomain": "smart-25f64.firebaseapp.com",
  "projectId": "smart-25f64",
  "storageBucket": "smart-25f64.firebasestorage.app",
  "messagingSenderId": "1037714016693",
  "appId": "1:1037714016693:web:fe5566e3073d0ff5cd31fc",
  "measurementId": "G-SH5E3714N7",
  "databaseURL": "https://console.firebase.google.com/u/0/project/smart-25f64/authentication/users"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
