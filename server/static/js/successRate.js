
function SuccessRateGraph(data,minimum,maximum) { 
     console.log(data) 
    $('#container').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'CPU Usage',
            x: -20 //center
        },

        xAxis: {
            min: minimum,
            max: maximum
        },
        yAxis: {
            title: {
                text: 'CPU Percent'
            },

            min: 0,
            max: 100,

            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '°C'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: data
    })
}



