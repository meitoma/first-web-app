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