<?php

    if (empty($_REQUEST['day'])) {
        print("ERROR: A day must be given!");
        exit(-1);
    }

    $day = $_REQUEST['day'];
    $conn = require_once('db.php');
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $stmt = $conn->prepare("SELECT id, date_created, origin, temperature, humidity, light_intensity
                            FROM measurements
                            WHERE CAST(date_created AS DATE) = :date
                            ORDER BY date_created DESC");

    $stmt->bindParam(':date', $day);
    $measurements = array();
    if($stmt->execute()) {
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $measurements[] = $row;
        }
    }
?>

<!DOCTYPE html>
<html>
    <head>
        <title>Data collection</title>
        <meta charset="UTF-8">
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                text-align:center;
            }
            th, td {
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <?php
            print("Data collection results - ".$day);
        ?>
        <?php
            if (count($measurements) == 0) {
                print("<p>No measurements found!</p>");
            } else {

                print("<table>");
                print("<tr><th>ID</th><th>Date</th><th>Origin</th><th>Temperature</th><th>Humidity</th><th>Light Intensity</th></tr>");
                foreach ($measurements as $m) {
                    $date = date_create($m['date_created']);
                    print("<tr><td>".$m['id']."</td>");
                    print("<td>".date_format($date, 'Y-m-d H:i:s')."</td>");
                    print("<td>".$m['origin']."</td>");
                    print("<td>".$m['temperature']."</td>");
                    print("<td>".$m['humidity']."</td>");
                    print("<td>".$m['light_intensity']."</td></tr>");
                }
                print("</table>");

            }
        ?>
    </body>
</html>