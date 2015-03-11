
function cpuRateGraph(input,minimum,maximum,timeStamps) { 

    $('#container').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'CPU Usage',
            x: -20 //center
        },

        xAxis: {
            categories: timeStamps,
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
            valueSuffix: '%'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: input 
    })
}



