
function ramRateGraph(container,input,minimumX,maximumX,minimumY,maximumY,timeStamps) { 

    $(container).highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'RAM Usage (RSS)',
            x: -20 //center
        },

        xAxis: {
            categories: timeStamps,
            min: minimumX,
            max: maximumX
        },
        yAxis: {
            title: {
                text: 'RAM'
            },

            min: minimumY,
            max: maximumY,

            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: 'Bytes'
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



