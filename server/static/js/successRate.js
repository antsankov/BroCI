function SuccessRateGraph(data) { 
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
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
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



