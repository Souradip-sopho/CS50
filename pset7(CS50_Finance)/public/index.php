<?php

    // configuration
    require("../includes/config.php"); 
    
    // if user reached page via GET (as by clicking a link or via redirect)
    if($_SERVER["REQUEST_METHOD"] == "GET")
    {
        $rows=CS50::query("SELECT * FROM portfolios p JOIN users u ON p.user_id=u.id WHERE u.id = ?", $_SESSION["id"]);
        $positions=[];
        $postion=NULL;
        $cash=$rows[0]["cash"];
        foreach($rows as $row)
        {
            $stock = lookup($row["symbol"]);
            if ($stock !== false)
            {
                $positions[] = [
                    "name" => $stock["name"],
                    "price" => $stock["price"],
                    "shares" => $row["shares"],
                    "symbol" => $row["symbol"]
                ];
            }
        }
        // render portfolio
        render("portfolio.php", ["positions" => $positions, "title" => "Portfolio", "cash"=>$cash]);
    }
?>
