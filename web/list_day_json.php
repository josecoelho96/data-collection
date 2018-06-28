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
                            ORDER BY date_created ASC");

    $stmt->bindParam(':date', $day);

    $date_created_arr = array();
    $temperature_arr = array();
    $humidity_arr = array();
    $light_intensity_arr = array();

    if($stmt->execute()) {
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $date = date_create($row['date_created']);
            $date_created_arr[] = date_format($date, 'Y-m-d H:i');;
            $temperature_arr[] = $row['temperature'];
            $humidity_arr[] = $row['humidity'];
            $light_intensity_arr[] = $row['light_intensity'];
        }
    }

    $arr = array('datetime'=>$date_created_arr, 'temperature'=>$temperature_arr, 'humidity'=>$humidity_arr, 'light'=>$light_intensity_arr);
    header('Content-type: application/json');
    echo json_encode($arr);
?>