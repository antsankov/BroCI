
function successRateGraph(container,input,minimumX,maximumX,timeStamps) { 

    $(container).highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'Analyzed Packets',
            x: -20 //center
        },

        xAxis: {
            categories: timeStamps,
            min: minimumX,
            max: maximumX
        },
        yAxis: {
            title: {
                text: 'Percent Successful Packets'
            },

            min: 0,
            max: 1,

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



