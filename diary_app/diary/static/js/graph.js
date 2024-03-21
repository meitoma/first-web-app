$(function() {
    $("#switch1").on("click", function(){
        $("#switch1").addClass("open");
        $("#switch2").removeClass("open");
        $("#switch3").removeClass("open");
    });
    $("#switch2").on("click", function(){
        $("#switch1").removeClass("open");
        $("#switch2").addClass("open");
        $("#switch3").removeClass("open");
    });
    $("#switch3").on("click", function(){
        $("#switch1").removeClass("open");
        $("#switch2").removeClass("open");
        $("#switch3").addClass("open");
    });
});

$('#myChart').on('inview', function(event, isInView) {//画面上に入ったらグラフを描画
    if (isInView) {
    var ctx=document.getElementById("myChart");//グラフを描画したい場所のid
    var chart=new Chart(ctx,{
        type: 'pie',
        data: {
            labels: ["食費", "日用品", "衣服", "美容", "交際費", "医療費", "教育費", "光熱費", "交通費", "通信費", "住居費"],
            datasets: [{
                backgroundColor: [
                    "#002b55",
                    "#004080",
                    "#0055aa",
                    "#006ad5",
                    "#0080ff",
                    "#2b95ff",
                    "#55aaff",
                    "#80bfff",
                    "#aad5ff",
                    "#d5eaff",
                    "#eaf4ff",
                ],
                data: [10, 11, 9, 8, 7, 6, 11, 10, 8, 9,11]
            }]
        },
        plugins: [ChartDataLabels], // datalabelsプラグインを追加
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend:{
                    display:true,//グラフの説明を表示
                    position: 'bottom',
                    align: 'start'
                },
                datalabels: {
                    formatter: function(value, context) {
                        return context.chart.data.labels[context.dataIndex];
                    },
                    align:"end",
                    display: 'auto',
                    color:"#888", 
                    }
                },},
        });
    }
});