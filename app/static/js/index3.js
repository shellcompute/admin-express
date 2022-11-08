// pyecharts based js
(function () {
    let containers = document.getElementsByClassName("chart-container");
    if (containers.length > 0) {
        containers[0].style.display = "block";
    }
})()

function showChart(evt, chartID) {
    let containers = document.getElementsByClassName("chart-container");
    for (let i = 0; i < containers.length; i++) {
        containers[i].style.display = "none";
    }

    let tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = "tablinks";
    }

    document.getElementById(chartID).style.display = "block";
    evt.currentTarget.className += " active";
}

$(
    function () {
        let chart1 = echarts.init(document.getElementById('general_pies'), 'white', {renderer: 'canvas'});
        let windowWidth = $(window).width();
        $.ajax({
            type: "GET",
            url: "/api/v1/general_pies?w="+windowWidth,
            dataType: 'json',
            success: function (result) {
                chart1.setOption(result);
            }
        });
    }
)