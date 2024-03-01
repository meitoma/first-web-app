if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/bbs/firebase-messaging-sw.js').then(registration => {
        console.log('ServiceWorker registration successful.');
    })
        .catch(err => {
        console.log('ServiceWorker registration failed.');
    });
    }
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getMessaging,onMessage,getToken} from "/bbs/static/js/firebase-messaging.js";

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
    // Notification.requestPermission().then((permission) => {
    //     if (permission === 'granted') {
    //         // 通知を許可した場合
    //         console.log('Notification permission granted.');
    //         getToken(messaging, { vapidKey: 'BLHLS0TscLaIH35iBgdaXUugwesIzIEGfud6jjxYYXFNomWQROLwiQBwrwYcgoC5KGcXiUZJbEHALiGmg0dDeOU' }).then((currentToken) => {
    //             if (currentToken) {
    //                 console.log("currentToken:");
    //                 console.log(currentToken);
    //                 socketio.emit("set_notification", {token:currentToken,user_id:current_user})
    //             }
    //             });
    //     } else {
    //         // 通知を拒否した場合
    //         console.log('Unable to get permission to notify.');
    //     }
    //     });
        // setTimeout(function(){
        //     location.reload();
        // }, 500 );
    });

$(function() {
    $(".openbtn1").on("click", function(){
        $(".openbtn1").toggleClass("active");
        $(".mask").toggleClass("open");
        $(".nav").toggleClass("open");
    });
    $(".mask").on("click", function(){
        $(".mask").toggleClass("open");
        if ($(".mask").hasClass("mask2")) {
            $(".make_thread").toggleClass("open");
            $(".mask").toggleClass("mask2");
          }
        else if ($(".mask").hasClass("mask3")) {
            $(".delete_display").toggleClass("open");
            $(".mask").toggleClass("mask3");
          }
        else if ($(".mask").hasClass("mask4")) {
            $(".add_member").toggleClass("open");
            $(".mask").toggleClass("mask4");
          }
        else{
            $(".openbtn1").toggleClass("active");
            $(".nav").toggleClass("open");
        }   
    });
    $(".add_member_btn, .add_cancel").on("click", function(){
        $(".add_member_btn").toggleClass("active");
        $(".add_member").toggleClass("open");
        $(".mask").toggleClass("mask4");
    });
    $(".new_thread, .cancel").on("click", function(){
        $(".new_thread").toggleClass("active");
        $(".make_thread").toggleClass("open");
        if (!$(".mask").hasClass("open")) {
            $(".mask").toggleClass("open");
          }
        $(".mask").toggleClass("mask2");
    });

    $(".delete_thread, .delete_cancel").on("click", function(){
        $(".delete_thread").toggleClass("active");
        $(".delete_display").toggleClass("open");
        if (!$(".mask").hasClass("open")) {
            $(".mask").toggleClass("open");
          }
        $(".mask").toggleClass("mask3");
    });
    $(".select_thread").on("click", function(){
        // socketio.emit('server_echo', {data: 'client leave from' + String(thread_id)});
        socketio.emit("leave", {room:String(thread_id)})
    });
    $(".create-thread").on("click", function(){
        // socketio.emit('server_echo', {data: 'client leave from' + String(thread_id)});
        socketio.emit("create_thread")
    });
    $(".delete-thread").on("click", function(){
        // socketio.emit('server_echo', {data: 'client leave from' + String(thread_id)});
        socketio.emit("delete_thread")
    });
    $('input').on('change', function () {
        var file = $(this).prop('files')[0];
        //text()で要素内のテキストを変更する
        if(file){
            textarea.value = file.name;
        }
        else{
            textarea.value = "";
        }
        
    });
});

function create_msg_html(send_user,send_time,send_user_name,type,message,messages_count) {
    var jc = "justify-content-start"
    var msbox = "othre-message-box"
    if(send_user==current_user){
        jc="justify-content-end"
        msbox="my-message-box"
    }
    var content_html='<div class="row '+ jc +' layer1">\n\
        <div class="col-9 '+ jc +' fix-btn">\n\
            <p class="'+ msbox +' inf-message"><span class="p-msg-name">'+ send_user_name +' </span> :\n\
            '+ send_time;
    if(send_user==current_user){
         content_html += '<span><a href="#">編集</a>&ensp;<a href="#">削除</a></span>\n'
        }
    if(type=="text"){
            content_html += '<div class="small-screen-content close"><!-- スマホ用の画面 -->\n'
            if(messages_count<=33){
                content_html += '<p class='+ msbox +' style="overflow-wrap: break-word; word-wrap: break-word;"><span class="message-box back-color">'+ message +'</span></p>\n</div>\n'
            }
            else{
                content_html += '<p class="'+ msbox +'  multi-rows " style="overflow-wrap: break-word; word-wrap: break-word;">'+ message +'</p>\n</div>\n'
            }
            content_html += '<div class="large-screen-content open"><!-- PC用の画面 -->\n'
            if(messages_count<=56){
                content_html += '<p class="'+ msbox +'" style="overflow-wrap: break-word; word-wrap: break-word;"><span class="message-box back-color">'+ message +'</span></p>\n</div>\n'
            }
            else{
                content_html += '<p class="'+ msbox +' multi-rows " style="overflow-wrap: break-word; word-wrap: break-word;">'+ message +'</p>\n</div>\n'
            }
        }
    else{
        content_html +='<div class="box '+ msbox +'">\n\
                        <div class="img-wrap">\n\
                            <a href="../static/send_images/'+ message +'" target="_blank"><img src="../static/send_images/'+ message +'" class ="img-msg"  width="400" alt="画像が見つかりませんでした" border="0" ></a>\n\
                        </div>\n\
                    </div>\n\
                </div>\n\
            </div>';
    }
    // console.log(content_html)
    return content_html;
}

var socketio = io();
$(function() {
    socketio.on('connect', function() {
        socketio.emit("join", {room:String(thread_id)})
    });

    socketio.on('reload', function () {
        console.log('Received message: reload');
        setTimeout(function(){
            location.reload()
        }, 500 );
    });
    socketio.on('add_meddage', function (message) {
        console.log('Received message: '+message["type"]+':'+message["message"]);
            var content = document.getElementById("scroller__inner");
            var contentHTML = content.innerHTML;
            var newContent=create_msg_html(message["send_user"],message["send_time"],message["send_user_name"],message["type"],message["message"],message["messages_count"])
            content.innerHTML = contentHTML + newContent;
            updateContent();
            setTimeout(function(){
                scrollbottonm();
            }, 700 );
    });
});


// 文字入力数に応じてテキストエリアの大きさ変更
var scrollable_box = document.getElementById('scrollable_box');
textarea.rows=1;
let clientHeight = textarea.clientHeight;
let scroll_box_Height = scrollable_box.clientHeight;
let init_scrollHeight = textarea.scrollHeight;
function adjustTextareaHeight() {
    let scrollHeight = textarea.scrollHeight;
    console.log(scrollHeight);
    
        if(scrollHeight < 160){
            textarea.style.height = clientHeight + 'px';
            let scrollHeight = textarea.scrollHeight;
            textarea.style.height = scrollHeight + 'px';
            scrollable_box.style.height = scroll_box_Height - scrollHeight + init_scrollHeight + 'px';
        }
}

$('.message-form button').on('click', function() {
    $(this).prop('disabled', true);
    var formData = new FormData(document.getElementById('message-form'));
    const xhr = new XMLHttpRequest();
    const input = document.getElementById('form-image');
    const file = input.files[0];
    function post_message() {
        xhr.open('POST', '/bbs/'+thread_id, true);

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                console.log('Success:', xhr.responseText);
            } else {
                console.error('Error:', xhr.statusText);
            }
        };
        xhr.onerror = function () {
            console.error('Network Error');
        };
        xhr.send(formData);
    }

    if (file) {
        var image_orientation;
        const reader = new FileReader();
        const loadImage = (src) => {
            return new Promise((resolve) => {
                const image = new Image();
                image.onload = () => resolve(image);
                image.src = src;
            });
        };
        reader.onload = async function (e) {
            const image = await loadImage(e.target.result);
            console.log(image.width, image.height);
            image_orientation = image.width < image.height ? "vertical" : "horizontal";
            formData.append('image_orientation', image_orientation);
            post_message()
        };
    
        reader.readAsDataURL(file);

    }else{
        formData.append('image_orientation', 'none');
        post_message()
    }
    textarea.value="";
    document.getElementById('form-image').value = '';
    $(this).prop('disabled', false);
    adjustTextareaHeight();
});

$(function () {    
    textarea.focus();
    textarea.addEventListener('input', adjustTextareaHeight);
    textarea.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            if (event.ctrlKey || event.metaKey){
                console.log("submit")
                $('.message-form button').click();
                event.preventDefault(); // デフォルトのEnterキーの挙動を防ぐ
        }}
    });
  });

var pre_window=0
function updateContent() {
    const smallScreenContent = document.querySelectorAll('.small-screen-content');
    const largeScreenContent = document.querySelectorAll('.large-screen-content');
    const image_message = document.querySelectorAll('.img-msg');
    var thresholdWidth = 600;

    if (window.innerWidth <= thresholdWidth) {
            smallScreenContent.forEach((element) => 
                element.classList.replace("close","open")
            );
            largeScreenContent.forEach((element) => 
                element.classList.replace("open","close")
            );
            image_message.forEach((element) => 
                element.setAttribute('width', 200)
            );
    } else {
            smallScreenContent.forEach((element) => 
                element.classList.replace("open","close")
            );
            largeScreenContent.forEach((element) => 
                element.classList.replace("close","open")
            );
            image_message.forEach((element) => 
                element.setAttribute('width', 400)
            );
    }
}
window.addEventListener('load', updateContent);
window.addEventListener('resize', updateContent);
