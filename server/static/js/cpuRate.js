
function cpuRateGraph(container,input,minimumX,maximumX,timeStamps) { 

    $(container).highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'CPU Usage',
            x: -20 //center
        },

        xAxis: {
            categories: timeStamps,
            min: minimumX,
            max: maximumX
        },
        yAxis: {
            title: {
                text: 'CPU Percent'
            },

            min: 0,
            max: 200,

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



