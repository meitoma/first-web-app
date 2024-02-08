document.getElementById('loginButton').addEventListener('click', function() {
    document.getElementById('loaderContainer').style.display = 'flex';
    setTimeout(function() {
        document.getElementById('loaderContainer').style.display = 'none';
    }, 15000); // 2秒後に非表示にする例
});
