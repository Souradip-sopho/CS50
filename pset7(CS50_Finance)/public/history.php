<?php

    // configuration
    require("../includes/config.php"); 
    
    // if user reached page via GET (as by clicking a link or via redirect)
    if($_SERVER["REQUEST_METHOD"] == "GET")
    {
        $rows=CS50::query("SELECT * FROM history WHERE userid = ?", $_SESSION["id"]);
        $positions=[];
        $count=1;
        foreach($rows as $row)
        {
            $stock = lookup($row["symbol"]);
            if ($stock !== false)
            {
                $positions[] = [
                    "id"=>$count++,
                    "type"=>$row["transaction"],
                    "price" => $stock["price"],
                    "shares" => $row["shares"],
                    "symbol" => $row["symbol"],
                    "time"=>$row["time"]
                ];
            }
        }
        // render portfolio
        render("history_show.php", ["positions" => $positions, "title" => "history"]);
    }
?>
