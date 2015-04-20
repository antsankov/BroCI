/* This file contains all of the graphs we need to display brofiler */

function ramRateGraph(container,input,maximumX,maximumY,timeStamps) { 
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
            min: 0, 
            max: maximumX
        },
        yAxis: {
            title: {
                text: 'RAM'
            },

            min: 0,
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

function speedRateGraph(container,input,maximumX,maximumY,timeStamps) {  
    $(container).highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'Speed (mbps)',
            x: -20 //center
        },

        xAxis: {
            categories: timeStamps,
            min: 0,
            max: maximumX
        },
        yAxis: {
            title: {
                text: 'speed'
            },

            min: 0,
            max: maximumY,

            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: 'mbps'
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

function cpuRateGraph(container,input,maximumX,timeStamps) { 

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
            min: 0, 
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


function successRateGraph(container,input,maximumX,timeStamps) {  
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
            min: 0, 
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
