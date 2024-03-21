window.onload = function(){
    var checkbox = document.getElementById("switch");
    var disply_incom = document.getElementById("contents_income");
    var disply_spending = document.getElementById("contents_spending");
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            disply_incom.style.display = "none";
            disply_spending.style.display = "block";
        } else {
            disply_incom.style.display = "block";
            disply_spending.style.display = "none";
        }
    });
};
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/diary_app/diary/sw.js').then(registration => {
        console.log('ServiceWorker registration successful.');
    }).catch(err => {
        console.log('ServiceWorker registration failed.');
    });
}