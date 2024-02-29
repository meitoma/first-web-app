var post_currentToken;
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/bbs/firebase-messaging-sw.js').then(registration => {
        console.log('ServiceWorker registration successful.');
    })
        .catch(err => {
        console.log('ServiceWorker registration failed.');
    });
    }
    const firebaseConfig = {
    apiKey: "AIzaSyD0X-VUevT6W94SZXJm6Dz3a3PlSG4u8Ow",
    authDomain: "bbs-app-da21d.firebaseapp.com",
    projectId: "bbs-app-da21d",
    storageBucket: "bbs-app-da21d.appspot.com",
    messagingSenderId: "78893226549",
    appId: "1:78893226549:web:063932b1409e9800a7af7c",
    measurementId: "G-8W68P9L4DF"
    };
    firebase.initializeApp(firebaseConfig);
    
    const messaging = firebase.messaging();
    Notification.requestPermission().then((permission) => {
    if (permission === 'granted') {
        // 通知を許可した場合
        console.log('Notification permission granted.');

        messaging.getToken().then((currentToken) => {
        if (currentToken) {
            post_currentToken = currentToken;
            console.log("currentToken:");
            console.log(currentToken);
        } else {
            // トークン取得失敗
        }
        });
    } else {
        // 通知を拒否した場合
        console.log('Unable to get permission to notify.');
    }
    });

document.getElementById('loginButton').addEventListener('click', function() {
    document.getElementById('loaderContainer').style.display = 'flex';
    document.getElementById('mask').style.display = 'block';
    setTimeout(function() {
        document.getElementById('loaderContainer').style.display = 'none';
    }, 15000); // 2秒後に非表示にする例
});
document.getElementById('signup1').addEventListener('click', function() {
    document.getElementById("h1_title").innerText = 'サインアップ';
    signup();
});
document.getElementById('signup2').addEventListener('click', function() {
    signup();
    document.getElementById("h1_title").innerText = 'サインアップ';
});
document.getElementById('signup_cancel').addEventListener('click', function() {
    login();
    document.getElementById("h1_title").innerText = 'ログイン';
});

function login() {
    // ログインフォーム表示
    document.getElementById("login-form").style.display = "block";
    // 新規登録フォーム非表示
    document.getElementById("signup-form").style.display = "none";
  }
  
function signup() {
    // 新規登録フォーム表示
    document.getElementById("signup-form").style.display = "block";
    // ログインフォーム非表示
    document.getElementById("login-form").style.display = "none";
}

$(function() {
    $('#loginButton').on('click', function() {
       $(this).prop('disabled', true);
       var formData = new FormData(document.getElementById('login-form'));
       console.log(post_currentToken);
       formData.append('FCMToken', post_currentToken);
       const xhr = new XMLHttpRequest();
       xhr.open('POST', '/login', true);
       xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                console.log(xhr.responseText);
                var response = JSON.parse(xhr.responseText);
                window.location.href = response.redirect_url;
            }
        };
       xhr.send(formData);
    });
});

$(function() {
    $('.one-clk-btn').on('click', function() {
       $(this).prop('disabled', true);
       $('#signup-form').submit();
    });
});




  