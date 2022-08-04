var chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/gpustat-data-tb1',
        success: function(point) {
            var series = chart.series[0]

            // add the point
            chart.series[0].addPoint(point[0], true);
            chart.series[1].addPoint(point[1], true);
            chart.series[2].addPoint(point[2], true);
            chart.series[3].addPoint(point[3], true);

            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Live Gpustat Data'
        },
        xAxis: {
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Gpustat',
                margin: 80
            }
        },
        series: [
            {
                name: 'Worker0',
                data: []
            },
            {
                name: 'Worker1',
                data: []
            },
            {
                name: 'Worker2',
                data: []
            },
            {
                name: 'Worker3',
                data: []
            }
        ]
    });
});
