
function SuccessRateGraph(data,minimum,maximum) { 
 
    console.log(min)
    $('#container').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'CPU Usage',
            x: -20 //center
        },
        //hardcoded for now, possibly a param in the future? 
        xAxis: {
            min: minimum,
            max: maximum
        },
        yAxis: {
            title: {
                text: 'CPU Percent'
            },
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



