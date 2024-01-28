$(function() {
    $('.one-clk-btn').on('click', function() {
       $(this).prop('disabled', true);
       $('form').submit();
    });
  });