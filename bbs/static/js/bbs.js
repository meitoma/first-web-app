$(function() {
    $(".openbtn1").on("click", function(){
        $(".openbtn1").toggleClass("active");
        $(".mask").toggleClass("open");
        $(".nav").toggleClass("open");
    });
    $(".mask").on("click", function(){
        $(".new_thread").removeClass("active");
        $(".make_thread").removeClass("open");
        $(".delete_thread").removeClass("open");
        $(".delete_display").removeClass("open");
        $(".add_member").removeClass("open");
        $(".add_member_btn").removeClass("active");
        $(".nav").removeClass("open");
        $(".openbtn1").removeClass("active");
        $(".mask").removeClass("open");
    });
    $(".add_member_btn").on("click", function(){
        $(".add_member_btn").addClass("active");
        $(".add_member").addClass("open");
        $(".mask").addClass("open");
    });
    $(".add_cancel").on("click", function(){
        $(".add_member_btn").removeClass("active");
        $(".add_member").removeClass("open");
        if(!$(".openbtn1").hasClass("active")){
            $(".mask").removeClass("open");
        }
    });

    $(".new_thread").on("click", function(){
        $(".new_thread").addClass("active");
        $(".make_thread").addClass("open");
        if (!$(".mask").hasClass("open")) {
            $(".mask").addClass("open");
          }
    });
    $(".cancel").on("click", function(){
        $(".new_thread").removeClass("active");
        $(".make_thread").removeClass("open");
        if(!$(".openbtn1").hasClass("active")){
           $(".mask").removeClass("open");
        }
    });

    $(".delete_thread").on("click", function(){
        $(".delete_thread").addClass("active");
        $(".delete_display").addClass("open");
        if (!$(".mask").hasClass("open")) {
            $(".mask").addClass("open");
          }
    });

    $(".delete_cancel").on("click", function(){
        $(".delete_thread").removeClass("active");
        $(".delete_display").removeClass("open");
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
// var scrollable_box = document.getElementById('scrollable_box');
textarea.rows=1;
let clientHeight = textarea.clientHeight;
// let scroll_box_Height = scrollable_box.clientHeight;
let init_scrollHeight = textarea.scrollHeight;
function adjustTextareaHeight() {
    let scrollHeight = textarea.scrollHeight;
    console.log(scrollHeight);
    
        if(scrollHeight < 160){
            textarea.style.height = clientHeight + 'px';
            let scrollHeight = textarea.scrollHeight;
            textarea.style.height = scrollHeight + 'px';
            // scrollable_box.style.height = scroll_box_Height - scrollHeight + init_scrollHeight + 'px';
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
        // xhr.onload = function () {
        //     if (xhr.status >= 200 && xhr.status < 300) {
        //         console.log('Success:', xhr.responseText);
        //     } else {
        //         console.error('Error:', xhr.statusText);
        //     }
        // };
        // xhr.onerror = function () {
        //     console.error('Network Error');
        // };
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
            image_orientation = image.width < image.height ? "vertical" : "horizontal";
            console.log(image.width, image.height,image_orientation);
            formData.append('image_orientation', image_orientation);
            post_message();
        };
        reader.readAsDataURL(file);

    }else{
        formData.append('image_orientation', 'none');
        post_message();
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
            var content = document.getElementById("scroller__inner");
            var newContent=create_msg_html(message["send_user"],message["send_time"],message["send_user_name"],message["type"],message["message"],message["messages_count"])
            content.insertAdjacentHTML('beforeend', newContent);
            updateContent();
            setTimeout(function(){
                scrollbottonm();
            }, 700 );
    });
});