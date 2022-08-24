var chart_time_w0;
var chart_time_w1;
var chart_time_w2;
var chart_time_w3;
var chart_images;

function requestData_time_w0() {
    $.ajax({
        url: '/log-data-tb1',
        success: function(point) {
            var series = chart_time_w0.series[0]
            chart_time_w0.series[0].addPoint(point[0], true);
            
            setTimeout(requestData_time_w0, 1000);
        },
        cache: false
    });
}

function requestData_time_w1() {
    $.ajax({
        url: '/log-data-tb1',
        success: function(point) {
            var series = chart_time_w1.series[0]
            chart_time_w1.series[0].addPoint(point[1], true);

            setTimeout(requestData_time_w1, 1000);
        },
        cache: false
    });
}

function requestData_time_w2() {
    $.ajax({
        url: '/log-data-tb1',
        success: function(point) {
            var series = chart_time_w2.series[0]
            chart_time_w2.series[0].addPoint(point[2], true);

            setTimeout(requestData_time_w2, 1000);
        },
        cache: false
    });
}

function requestData_time_w3() {
    $.ajax({
        url: '/log-data-tb1',
        success: function(point) {
            var series = chart_time_w3.series[0]
            chart_time_w3.series[0].addPoint(point[3], true);

            setTimeout(requestData_time_w3, 1000);
        },
        cache: false
    });
}

function requestData_images() {
    $.ajax({
        url: '/log-data-tb1',
        success: function(point) {
            var series = chart_images.series[0]

            chart_images.series[0].addPoint(point[4], true);
            
            setTimeout(requestData_images, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart_images = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container-images',
            defaultSeriesType: 'spline',
            events: {
                load: requestData_images
            }
        },
        title: {
            text: 'Log Data (Images per Second)'
        },
        xAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'iteration',
                margin: 40
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'image.per.sec',
                margin: 80
            }
        },
        series: [
            {
                name: 'node(testbed1)',
                data: []
            }
        ]
    });

    chart_time_w0 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container-time-w0',
            defaultSeriesType: 'spline',
            events: {
                load: requestData_time_w0
            }
        },
        title: {
            text: 'Worker 0 Log Data (Elapsed Time)'
        },
        xAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'iteration',
                margin: 40
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'elapsed.time(sec)',
                margin: 80
            }
        },
        series: [
            {
                name: 'Worker0',
                data: []
            }
        ]
    });

    chart_time_w1 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container-time-w1',
            defaultSeriesType: 'spline',
            events: {
                load: requestData_time_w1
            }
        },
        title: {
            text: 'Worker 1 Log Data (Elapsed Time)'
        },
        xAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'iteration',
                margin: 40
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'elapsed.time(sec)',
                margin: 80
            }
        },
        series: [
            {
                name: 'Worker1',
                data: []
            }
        ]
    });

    chart_time_w2 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container-time-w2',
            defaultSeriesType: 'spline',
            events: {
                load: requestData_time_w2
            }
        },
        title: {
            text: 'Worker 2 Log Data (Elapsed Time)'
        },
        xAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'iteration',
                margin: 40
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'elapsed.time(sec)',
                margin: 80
            }
        },
        series: [
            {
                name: 'Worker2',
                data: []
            }
        ]
    });

    chart_time_w3 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container-time-w3',
            defaultSeriesType: 'spline',
            events: {
                load: requestData_time_w3
            }
        },
        title: {
            text: 'Worker 3 Log Data (Elapsed Time)'
        },
        xAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'iteration',
                margin: 40
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'elapsed.time(sec)',
                margin: 80
            }
        },
        series: [
            {
                name: 'Worker3',
                data: []
            }
        ]
    });
});
