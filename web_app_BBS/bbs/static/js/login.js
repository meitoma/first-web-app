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
    $('.one-clk-btn').on('click', function() {
       $(this).prop('disabled', true);
       $('#signup-form').submit();
    });
});
