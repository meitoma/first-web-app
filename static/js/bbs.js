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
        else{
            $(".openbtn1").toggleClass("active");
            $(".nav").toggleClass("open");
        }
          
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
});

$(function() {
    $('.message-form button').on('click', function() {
       $(this).prop('disabled', true);
       $('.message-form').submit();
    });
  });

var textarea = document.getElementById('text_area');
var scrollable_box = document.getElementById('scrollable_box');
textarea.rows=1;
let clientHeight = textarea.clientHeight;
let scroll_box_Height = scrollable_box.clientHeight;
let init_scrollHeight = textarea.scrollHeight;

textarea.addEventListener('input', ()=>{
    let scrollHeight = textarea.scrollHeight;
    console.log(scrollHeight)
    
    if(scrollHeight < 160){
        //textareaの要素の高さを設定（rows属性で行を指定するなら「px」ではなく「auto」で良いかも！）
        textarea.style.height = clientHeight + 'px';
        //textareaの入力内容の高さを取得
        let scrollHeight = textarea.scrollHeight;
        //textareaの高さに入力内容の高さを設定
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