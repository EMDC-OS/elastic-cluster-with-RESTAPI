var chart_util;
var chart_power;
var chart_mem;

function requestData_util() {
    $.ajax({
        url: '/gpustat-data-tb2',
        success: function(point) {
            var series = chart_util.series[0]

            chart_util.series[0].addPoint(point[0][0], true);
            chart_util.series[1].addPoint(point[1][0], true);
            chart_util.series[2].addPoint(point[2][0], true);
            chart_util.series[3].addPoint(point[3][0], true);

            setTimeout(requestData_util, 1000);
        },
        cache: false
    });
}

function requestData_power() {
    $.ajax({
        url: '/gpustat-data-tb2',
        success: function(point) {
            var series = chart_power.series[0]

            chart_power.series[0].addPoint(point[0][1], true);
            chart_power.series[1].addPoint(point[1][1], true);
            chart_power.series[2].addPoint(point[2][1], true);
            chart_power.series[3].addPoint(point[3][1], true);

            setTimeout(requestData_power, 1000);
        },
        cache: false
    });
}

function requestData_mem() {
    $.ajax({
        url: '/gpustat-data-tb2',
        success: function(point) {
            var series = chart_mem.series[0]

            chart_mem.series[0].addPoint(point[0][2], true);
            chart_mem.series[1].addPoint(point[1][2], true);
            chart_mem.series[2].addPoint(point[2][2], true);
            chart_mem.series[3].addPoint(point[3][2], true);

            setTimeout(requestData_mem, 1000);
        },
        cache: false
    });
}


$(document).ready(function() {
    chart_util = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container-util',
            defaultSeriesType: 'spline',
            events: {
                load: requestData_util
            }
        },
        title: {
            text: 'Live Gpustat Data (utilization.gpu)',
            style : {
                fontSize: '22px'                                                                          
            }
        },
        xAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'time(sec)',
                margin: 40,
                style : {
                    fontSize: '20px'
                }
            },
            labels: {
                style: {
                    fontSize: '20px'
                }
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'utilization.gpu(%)',
                margin: 80,
                style : {
                    fontSize: '20px'
                }
            },
            labels: {
        	    style: {
            	    fontSize: '20px'
                }
            }
        },
        legend: {
    	    itemStyle: {
        	    fontSize: '15px'
            }
        },
        series: [
            {
                name: 'Worker0',
                data: [],
                dataLabels: {
                    style: {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker1',
                data: [],
                dataLabels: {
                    style: {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker2',
                data: [],
                dataLabels: {
                    style: {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker3',
                data: [],
                dataLabels: {
                    style: {
                        fontSize: '15px'
                    }
                }
            }
        ]
    });

    chart_power = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container-power',
            defaultSeriesType: 'spline',
            events: {
                load: requestData_power
            }
        },
        title: {
            text: 'Live Gpustat Data (power.draw)',
            style : {
                fontSize: '22px'                                                                          
            }
        },
        xAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'time(sec)',
                margin: 40,
                style : {
                    fontSize: '20px'
                }
            },
            labels: {
                style: {
                    fontSize: '20px'
                }
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'power.draw(W)',
                margin: 80,
                style : {
                    fontSize: '20px'
                }
            },
            labels: {
                style: {
                    fontSize: '20px'
                }
            }
        },
        legend: {
            itemStyle: {
                fontSize: '15px'                                                                          
            }
        },
        series: [
            {
                name: 'Worker0',
                data: [],
                dataLabels: {
                    style : {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker1',
                data: [],
                dataLabels: {
                    style : {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker2',
                data: [],
                dataLabels: {
                    style : {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker3',
                data: [],
                dataLabels: {
                    style : {
                        fontSize: '15px'
                    }
                }
            }
        ]
    });

    chart_mem = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container-mem',
            defaultSeriesType: 'spline',
            events: {
                load: requestData_mem
            }
        },
        title: {
            text: 'Live Gpustat Data (memory.used)',
            style : {
                fontSize: '22px'
            }
        },
        xAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'time(sec)',
                margin: 40,
                style : {
                    fontSize: '20px'
                }
            },
            labels: {
                style: {
                    fontSize: '20px'
                }
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'memory.used(MB)',
                margin: 80,
                style : {
                    fontSize: '20px'
                }
            },
            labels: {
                style: {
                    fontSize: '20px'
                }
            }
        },
        legend: {
            itemStyle: {
                fontSize: '15px'                                                                          
            }
        },
        series: [
            {
                name: 'Worker0',
                data: [],
                dataLabels: {
                    style : {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker1',
                data: [],
                dataLabels: {
                    style : {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker2',
                data: [],
                dataLabels: {
                    style : {
                        fontSize: '15px'
                    }
                }
            },
            {
                name: 'Worker3',
                data: [],
                dataLabels: {
                    style : {
                        fontSize: '15px'
                    }
                }
            }
        ]
    });
});
