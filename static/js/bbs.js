$(function() {
    $(".openbtn1").on("click", function(){
        $(".openbtn1").toggleClass("active");
        $(".mask").toggleClass("open");
        $(".nav").toggleClass("open");
    });
    $(".mask").on("click", function(){
        $(".openbtn1").toggleClass("active");
        $(".mask").toggleClass("open");
        $(".nav").toggleClass("open");
    });
});

$(function() {
    $('button').on('click', function() {
       $(this).prop('disabled', true);
       $('form').submit();
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
            // submitTextarea();
            console.log("submit")
            $('button').click();
            // $.post( '/bbs/1', $('form').serialize() )
            // .done(function( data ) {
            //     console.log( data.form );
            // })
            event.preventDefault(); // デフォルトのEnterキーのd挙動を防ぐ
        }
    }
});