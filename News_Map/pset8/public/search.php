<?php

    require(__DIR__ . "/../includes/config.php");

    // numerically indexed array of places
    $places = [];

    // TODO: search database for places matching $_GET["geo"], store in $places
    if(is_numeric($_GET["geo"])) 
        $places = CS50::query("SELECT * FROM places WHERE postal_code LIKE ?", $_GET["geo"] . "%");
    else
    {
        $queries=explode(",",$_GET["geo"]);
        if(count($queries) == 1)
        {
            #$places = CS50::query("SELECT * FROM places WHERE MATCH(postal_code, place_name) AGAINST (? IN NATURAL LANGUAGE MODE)", $_GET["geo"]);
            $places = CS50::query("SELECT * FROM places WHERE place_name LIKE ?", $queries[0]."%");
        }
        else
        {
            $places = CS50::query("SELECT * FROM places WHERE place_name LIKE ? OR admin_name1 LIKE ?", $queries[0]."%",$queries[1]."%");
        }
    }

    // output places as JSON (pretty-printed for debugging convenience)
    header("Content-type: application/json");
    print(json_encode($places, JSON_PRETTY_PRINT));

?>