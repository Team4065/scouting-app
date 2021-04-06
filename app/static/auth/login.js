var firebaseConfig = {
  apiKey: "AIzaSyCIUUm-niMkgeFBCC6cPlIwOPDJm3aHZH4",
  authDomain: "nerdsofpreyscoutingapp.firebaseapp.com",
  projectId: "nerdsofpreyscoutingapp",
  storageBucket: "nerdsofpreyscoutingapp.appspot.com",
  messagingSenderId: "6231571727",
  appId: "1:6231571727:web:adb905152bbf57687c927a",
  measurementId: "G-F5FRC1DY91",
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();

var ui = new firebaseui.auth.AuthUI(firebase.auth());

var uiconfig = {
  callbacks: {
    signInSuccessWithAuthResult: function (authResult, redirectUrl) {
      authResult.user.getIdToken()
        .then(token => {
          console.log('Sending auth_token to the server!');
          console.log(token);
          fetch('/auth/login', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({auth_token: token})
          })
          .then(resp => resp.json())
          .then(json => console.log(json))
          .catch(err => console.error("Failed to send authentication token to server."));
        });
      return false;
    },
    uiShown: function () {
      // The widget is rendered.
      // Hide the loader.
      document.getElementById("loader").style.display = "none";
    },
  },
  // Will use popup for IDP Providers sign-in flow instead of the default, redirect.
  signInFlow: "redirect",
  signInSuccessUrl: "/",
  signInOptions: [
    {
      provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      customParameters: {
        // Forces account selection even when one account
        // is available.
        prompt: "select_account",
      },
    },
    firebase.auth.EmailAuthProvider.PROVIDER_ID, // Other providers don't need to be given as object.
  ],
};

ui.start("#firebaseui-auth-container", uiconfig);
