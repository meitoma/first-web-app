$(function() {
    $(".openbtn1").on("click", function(){
        $(".openbtn1").toggleClass("active");
        $(".mask").toggleClass("open");
        $(".nav").toggleClass("open");
    });
    $(".mask").on("click", function(){
        $(".new_thread").removeClass("active");
        $(".make_thread").removeClass("open");
        $("#nav1").removeClass("mk_thread_open");
        $(".delete_thread").removeClass("open");
        $(".delete_display").removeClass("open");
        $(".add_member").removeClass("open");
        $(".add_member_btn").removeClass("active");
        $(".nav").removeClass("open");
        $(".openbtn1").removeClass("active");
        $(".mask").removeClass("open");
        $(".mask").removeClass("open_up");
        $(".ws-invite").removeClass("open");
    });
    $(".add_member_btn").on("click", function(){
        $(".add_member_btn").addClass("active");
        $(".add_member").addClass("open");
        $(".mask").addClass("open");
        $(".mask").addClass("open_up");
    });
    $(".add_cancel").on("click", function(){
        $(".add_member_btn").removeClass("active");
        $(".add_member").removeClass("open");
        $(".mask").removeClass("open_up");
        if(!$(".openbtn1").hasClass("active")){
            $(".mask").removeClass("open");
        }
    });
    $("#show_invite_screen").on("click", function(){
        $(".ws-invite").addClass("open");
        $(".mask").addClass("open");
        $(".mask").addClass("open_up");
    });
    $("#cancel_invite_screen").on("click", function(){
        $(".ws-invite").removeClass("open");
        $(".mask").removeClass("open_up");
    });

    $(".new_thread").on("click", function(){
        $(".new_thread").addClass("active");
        $(".make_thread").addClass("open");
        $(".mask").addClass("open_up");
        $("#nav1").addClass("mk_thread_open");
        if (!$(".mask").hasClass("open")) {
            $(".mask").addClass("open");
    }
    });
    $(".cancel").on("click", function(){
        $(".new_thread").removeClass("active");
        $(".make_thread").removeClass("open");
        $("#nav1").removeClass("mk_thread_open");
        $(".mask").removeClass("open_up");
        if(!$(".openbtn1").hasClass("active")){
            $(".mask").removeClass("open");
        }
    });

    $(".delete_thread").on("click", function(){
        $(".delete_thread").addClass("active");
        $(".delete_display").addClass("open");
        $(".mask").addClass("open_up");
        if (!$(".mask").hasClass("open")) {
            $(".mask").addClass("open");
    }
    });
    $(".delete_cancel").on("click", function(){
        $(".delete_thread").removeClass("active");
        $(".delete_display").removeClass("open");
        $(".mask").removeClass("open_up");
        if(!$(".openbtn1").hasClass("active")){
            $(".mask").removeClass("open");
        }
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
    $('#form-image').on('change', function () {
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
document.getElementById('linkcpBtn').addEventListener('click', function() {
    // ボタンがクリックされたときの処理
    var linkText = document.getElementById('invite_link').innerText; // URLを取得
    navigator.clipboard.writeText(linkText) // URLをクリップボードに書き込む
    .then(function() {
        console.log('Link copied to clipboard!'); // コピーが完了したことをユーザーに通知
    })
    .catch(function(err) {
        console.error('Failed to copy: ', err); // コピーが失敗した場合のエラー処理
    });
});
function create_error_html(send_user){
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
    content_html += '<div class="small-screen-content close"><!-- スマホ用の画面 -->\n'
    if(messages_count<=33){
        content_html += '<p class='+ msbox +' style="overflow-wrap: break-word; word-wrap: break-word;"><span class="message-box back-color">'+ message +'</span></p>\n</div>\n'
    }
    else{
        content_html += '<p class="'+ msbox +'  multi-rows " style="overflow-wrap: break-word; word-wrap: break-word;">通信に失敗しました。リロードしてください。</p>\n</div>\n'
    }
    content_html += '<div class="large-screen-content open"><!-- PC用の画面 -->\n'
    if(messages_count<=56){
        content_html += '<p class="'+ msbox +'" style="overflow-wrap: break-word; word-wrap: break-word;"><span class="message-box back-color">通信に失敗しました。リロードしてください。</span></p>\n</div>\n'
    }
    else{
        content_html += '<p class="'+ msbox +' multi-rows " style="overflow-wrap: break-word; word-wrap: break-word;">通信に失敗しました。リロードしてください。</p>\n</div>\n'
    }
    console.log(content_html)
    return content_html;
}
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
                            <a href="/bbs/static/send_images/'+ message +'" target="_blank"><img src="/bbs/static/send_images/'+ message +'" class ="img-msg"  width="400" alt="画像が見つかりませんでした" border="0" ></a>\n\
                        </div>\n\
                    </div>\n\
                </div>\n\
            </div>';
    }
    // console.log(content_html)
    return content_html;
}

// 文字入力数に応じてテキストエリアの大きさ変更
textarea.rows=1;
let clientHeight = textarea.clientHeight;
let init_scrollHeight = textarea.scrollHeight;
function adjustTextareaHeight() {
    let scrollHeight = textarea.scrollHeight;
    console.log(scrollHeight);
    
        if(scrollHeight < 160){
            textarea.style.height = clientHeight + 'px';
            let scrollHeight = textarea.scrollHeight;
            textarea.style.height = scrollHeight + 'px';
        }
}

$('.message-form button').on('click', function() {
    $(this).prop('disabled', true);
    var formData = new FormData(document.getElementById('message-form'));
    const xhr = new XMLHttpRequest();
    const input = document.getElementById('form-image');
    const file = input.files[0];
    // 位置情報の取得に成功した場合のコールバック関数
    function get_current_position(){
        function successCallback(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            console.log('位置情報の送信に成功しました:', latitude, longitude);
            socketio.emit('get_reverse_geo', {latitude:latitude,longitude:longitude});
        }
        function errorCallback(error) {
            console.error("Error getting location:", error);
        }
        var options = {
            enableHighAccuracy: true, // より高精度な位置情報を取得する場合はtrue
            timeout: 5000, // タイムアウトまでの時間（ミリ秒）
            maximumAge: 0 // キャッシュされた位置情報を使用しない場合は0
        };
        navigator.geolocation.getCurrentPosition(successCallback,errorCallback,options);
    }

    function post_message() {
        xhr.open('POST', thread_id, true);
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                console.log('Success:', xhr.responseText);
            } else {
                var newContent = '<p class="msg-error">通信に失敗しました。リロードします。</p>'
                content.insertAdjacentHTML('beforeend', newContent);
                console.error('Error:', xhr.statusText);
                setTimeout(function(){
                    location.reload()
                }, 3000 );
            }
        };
        xhr.onerror = function () {
            console.error('Network Error');
        };
        xhr.send(formData);
    }
    get_current_position();
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
            image_orientation = image.width < image.height ? "vertical" : "horizontal";
            console.log(image.width, image.height,image_orientation);
            formData.append('image_orientation', image_orientation);
            post_message();
        };
        reader.readAsDataURL(file);

    }else{
        formData.append('image_orientation', 'none');
        post_message();
        socketio.emit('submit_message', { current_user:current_user, type:"text",message: textarea.value ,thread_id:thread_id});
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

// var socketio =  io.connect('http://127.0.0.1:3000');
var socketio =  io();
socketio.emit("join", {room:String(thread_id)})
$(function() {
    socketio.on('connect', function() {
    console.log('connect');
        // socketio.emit("join", {room:String(thread_id)})
    });

    socketio.on('reload', function () {
        console.log('Received message: reload');
        setTimeout(function(){
            location.reload()
        }, 500 );
    });
    socketio.on('add_meddage', function (message) {
        console.log('Received message: '+message["type"]+':'+message["message"]);
            var newContent=create_msg_html(message["send_user"],message["send_time"],message["send_user_name"],message["type"],message["message"],message["messages_count"])
            content.insertAdjacentHTML('beforeend', newContent);
            updateContent();
            setTimeout(function(){
                scrollbottonm();
            }, 700 );
    });
});