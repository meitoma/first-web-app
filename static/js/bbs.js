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
});

// var socketio = io.connect('http://' + '127.0.0.1:5000');
var socketio = io();
$(function() {
    socketio.on('connect', function() {
        socketio.emit("join", {room:String(thread_id)})
    });

    socketio.on('message', function () {
        console.log('Received message: reload');
        setTimeout(function(){
            location.reload()
        }, 500 );
    });
});

$(function() {
    $('.message-form button').on('click', function() {
       $(this).prop('disabled', true);
       socketio.emit('my_chat', {data:"message",to:String(thread_id)});
       $('.message-form').submit();
    });
    var textarea = document.getElementById('text_area');
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
    // const smallScreenContent = document.querySelector('.a');
    // const largeScreenContent = document.querySelector('.b');
    var thresholdWidth = 600;
    if (window.innerWidth <= thresholdWidth) {
        // if (!$(".small-screen-content").contains("open")) {
            // smallScreenContent.classList.remove("close");
            smallScreenContent.forEach((element) => 
                element.classList.replace("close","open")
            );
            largeScreenContent.forEach((element) => 
                element.classList.replace("open","close")
            );
            // smallScreenContent.classList.add("open");
            // smallScreenContent.style.display="block";
            // largeScreenContent.style.display="none";
            // largeScreenContent.classList.replace("open","close");
            // console.log(smallScreenContent)
            // console.log(largeScreenContent)
        // }
    } else {
        // if (!$(".large-screen-content").contains("open")) {
            // smallScreenContent.classList.replace("open","close");
            // smallScreenContent.style.display="none";
            // largeScreenContent.style.display="block";
            // largeScreenContent.classList.replace("close","open");
            smallScreenContent.forEach((element) => 
                element.classList.replace("open","close")
            );
            largeScreenContent.forEach((element) => 
                element.classList.replace("close","open")
            );
            // console.log(smallScreenContent)
            // console.log(largeScreenContent)
        // }
    }
}
window.addEventListener('load', updateContent);
window.addEventListener('resize', updateContent);