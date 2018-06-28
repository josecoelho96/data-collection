<?php

    if (empty($_REQUEST['day'])) {
        print("ERROR: A day must be given!");
    }

    $day = $_REQUEST['day'];
?>



<!doctype html>
<html>

<head>
    <title>Data collection results - <?php print($day) ?> - Plot</title>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <style>
        canvas{
            -moz-user-select: none;
            -webkit-user-select: none;
            -ms-user-select: none;
        }
    </style>
</head>

<body>
    <div style="width:90%;">
        <canvas id="canvas"></canvas>
    </div>
    <br>
    <br>
	<script>
		window.onload = function() {
            $.get('http://web.tecnico.ulisboa.pt/~ist181013/data-collection/list_day_json.php', {day: <?php echo("\"".$day."\"")?> }, function(data){

                var config = {
			        type: 'line',
			        data: {
			        	labels: data.datetime,
			        	datasets: [
                            {
                                label: 'Temperature',
                                yAxisID: 'Temperature',
                                backgroundColor: 'rgb(252, 42, 0)',
                                borderColor: 'rgb(252, 42, 0)',
                                borderWidth: 1.5,
                                radius: 0,
                                data: data.temperature,
			        		    fill: false,
			        	    },
                            {
                                label: 'Humidity',
                                yAxisID: 'Humidity',
                                backgroundColor: 'rgb(17, 187, 249)',
                                borderColor: 'rgb(17, 187, 249)',
                                borderWidth: 1.5,
                                radius: 0,
                                data: data.humidity,
                                fill: false,
			        	    },
                            {
                                label: 'Light intensity',
                                yAxisID: 'Light',
                                backgroundColor: 'rgb(244, 127, 2)',
                                borderColor: 'rgb(244, 127, 2)',
                                borderWidth: 1.5,
                                radius: 0,
                                data: data.light,
                                fill: false,
			        	    }
                        ]
		            },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Measurements evolution over time'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        elements: {
                            line: {
                                tension: 0
                            }
                        },
                        scales: {
                            xAxes: [
                                {
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Date/Time'
                                    }
                                }
                            ],
                            yAxes: [
                                {
                                    id: 'Temperature',
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Temperature [ºC]'
                                    },
                                    ticks: {
                                        suggestedMin: 10,
                                        suggestedMax: 45
                                    }
                                },
                                {
                                    id: 'Humidity',
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Humidity [%]'
                                    },
                                    ticks: {
                                        min: 0,
                                        max: 100
                                    }
                                },
                                {
                                    id: 'Light',
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Light intensity [0 - 1023]'
                                    },
                                    ticks: {
                                        min: 0,
                                        max: 1023
                                    }
                                }
                            ]
                        }
                    }
		        };

			    var ctx = document.getElementById('canvas').getContext('2d');
			    window.myLine = new Chart(ctx, config);
            });

		};

	</script>
</body>

</html>
