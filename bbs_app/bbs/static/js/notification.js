if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/bbs_app/bbs/firebase-messaging-sw.js').then(registration => {
        console.log('ServiceWorker registration successful.');
    })
        .catch(err => {
        console.log('ServiceWorker registration failed.');
    });
    }
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getMessaging,onMessage,getToken} from "/bbs_app/bbs/static/js/firebase-messaging.js";

const firebaseConfig = {
apiKey: "AIzaSyD0X-VUevT6W94SZXJm6Dz3a3PlSG4u8Ow",
authDomain: "bbs-app-da21d.firebaseapp.com",
projectId: "bbs-app-da21d",
storageBucket: "bbs-app-da21d.appspot.com",
messagingSenderId: "78893226549",
appId: "1:78893226549:web:063932b1409e9800a7af7c",
measurementId: "G-8W68P9L4DF"
};
const firebaseApp = initializeApp(firebaseConfig);
const messaging = getMessaging(firebaseApp);
function asyncFunction1() {
    return new Promise((resolve, reject) => {
        Notification.requestPermission().then((permission) => {
            if (permission === 'granted') {
                // 通知を許可した場合
                console.log('Notification permission granted.');
                getToken(messaging, { vapidKey: 'BLHLS0TscLaIH35iBgdaXUugwesIzIEGfud6jjxYYXFNomWQROLwiQBwrwYcgoC5KGcXiUZJbEHALiGmg0dDeOU' }).then((currentToken) => {
                    if (currentToken) {
                        console.log("currentToken:");
                        console.log(currentToken);
                        socketio.emit("set_notification", {token:currentToken,user_id:current_user});
                        resolve();
                    }
                    });
            } else {
                // 通知を拒否した場合
                console.log('Unable to get permission to notify.');
                resolve();
            }
            });
        setTimeout(function(){
            reject();
            }, 5000 );
    });
}
function asyncFunction2() {
return new Promise((resolve, reject) => {
    location.reload();
    resolve();
});
}

$('#notification').on('click', async function() {
    console.log('Notification');
    try {
        await asyncFunction1();
        console.log("Both functions completed");
    } catch (error) {
        console.error("An error occurred:", error);
        await asyncFunction2();
    }
    });