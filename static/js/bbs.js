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
        $(".mask").toggleClass("open");
        $(".mask").toggleClass("mask2");
    });

    $(".delete_thread, .delete_cancel").on("click", function(){
        $(".delete_thread").toggleClass("active");
        $(".delete_display").toggleClass("open");
        $(".mask").toggleClass("open");
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
            if(messages_count<=27){
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
                            <a href="../static/send_images/'+ message +'" target="_blank"><img src="../static/send_images/'+ message +'" class ="img-msg"  width="400" alt="" border="0" ></a>\n\
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
        console.log('Received message: '+message["type"]+message["message"]);
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
document.getElementById('message-form').addEventListener('submit', function (event) {
    event.preventDefault();

});

$(function() {
    // $('.message-form button').on('click', function() {
    //     $(this).prop('disabled', true);
    //     const input = document.getElementById('form-image');
    //     const file = input.files[0];
    //     textarea = document.getElementById('text_area');
    //     if (file || textarea.value) {
    //         if (file) {
    //             console.log("send image");
    //             const reader = new FileReader();
    //             reader.onload = (e) => {
    //                 const imageData = e.target.result;
    //                 console.log(imageData)
    //                 socketio.emit('submit_message', { current_user:current_user,type:"image",message: imageData ,name: file.name,thread_id:thread_id});
    //             };
    //             reader.readAsDataURL(file);
    //             // socketio.emit('submit_message', { type:"image",message: file });
    //         }else{
    //             socketio.emit('submit_message', { current_user:current_user, type:"text",message: textarea.value ,thread_id:thread_id});
    //         }
    //     } else {
    //         console.log('Please select an image.');
    //     }
    //     textarea.value="";
    //  });
    $('.message-form button').on('click', function() {
        const formData = new FormData(document.getElementById('message-form'));
        const xhr = new XMLHttpRequest();
        const input = document.getElementById('form-image');
        const file = input.files[0];
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
    });
    $('.message-form button').on('click', function() {
    //    socketio.emit('my_chat', {data:"message",to:String(thread_id)});
    //    $('.message-form').submit();
       textarea.value="";
       $(this).prop('disabled', false);
    });
    
    var scrollable_box = document.getElementById('scrollable_box');
    textarea.rows=1;
    let clientHeight = textarea.clientHeight;
    let scroll_box_Height = scrollable_box.clientHeight;
    let init_scrollHeight = textarea.scrollHeight;
    textarea.focus();
    textarea.addEventListener('input', ()=>{
        let scrollHeight = textarea.scrollHeight;
        console.log(scrollHeight)
        
        if(scrollHeight < 160){
            textarea.style.height = clientHeight + 'px';
            let scrollHeight = textarea.scrollHeight;
            textarea.style.height = scrollHeight + 'px';
            scrollable_box.style.height = scroll_box_Height - scrollHeight + init_scrollHeight + 'px';
        }
    });
    textarea.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            if (event.ctrlKey || event.metaKey){
                console.log("submit")
                $('.message-form button').click();
                event.preventDefault(); // デフォルトのEnterキーのd挙動を防ぐ
            }
        }
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

// window.onload = function(){
//     var obj = document.getElementById("scroller__inner");
//     obj.scrollTop = obj.scrollHeight;
//     }