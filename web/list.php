<!DOCTYPE html>
<html>
    <head>
        <title>Data collection</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Data collection results - All</h1>

<?php
    $conn = require_once('db.php');

    echo("<table border=1 cellpadding='5'>");
    echo("<thead><tr><th>Date created</th><th>Origin</th><th>Temperature</th><th>Humidity</th><th>Light intensity</th></tr></thead>");
    foreach ($conn->query("SELECT date_created, origin, temperature, humidity, light_intensity FROM measurements ORDER BY date_created DESC") as $row) {
        echo("<tr><td>".$row['date_created']."</td><td>".$row['origin']."</td><td>".$row['temperature']."</td><td>".$row['humidity']."</td><td>".$row['light_intensity']."</td></tr>");
        #echo($row['date_created']);
    }
    echo("</table>");
?>
    </body>
</html>