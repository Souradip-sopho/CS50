<?php

    // configuration
    require("../includes/config.php"); 

    // if user reached page via GET (as by clicking a link or via redirect)
    if ($_SERVER["REQUEST_METHOD"] == "GET")
    {
        // else render form
        render("buy_form.php", ["title" => "Buy"]);
    }

    // else if user reached page via POST (as by submitting a form via POST)
    else if ($_SERVER["REQUEST_METHOD"] == "POST")
    {
        // query database for user
        $rows = CS50::query("SELECT * FROM users WHERE id = ?", $_SESSION["id"]);
        $portf= CS50::query("SELECT * FROM portfolios");
        $count=count($portf);
        if(count($rows)==1)
            $prev_cash=$rows[0]["cash"];
        
        // validate submission
        if (empty($_POST["symbol"]))
        {
            apologize("You must provide a symbol.");
        }
        else if (empty($_POST["shares"]))
        {
            apologize("You must provide shares.");
        }
        
        $match=preg_match("/^\d+$/", $_POST["shares"]);
        if(!$match)
        {
            apologize("Invalid shares.");
        }
        
        $stock=lookup($_POST["symbol"]);
        $price=$stock["price"];
        $t_cost=$_POST["shares"]*$price;
        if($prev_cash<$t_cost)
        {
            apologize("Not enough cash.");
        }
        $symbol=strtoupper($_POST["symbol"]);
        $inserted=CS50::query("INSERT INTO portfolios (id,user_id, symbol, shares) VALUES( ?, ?, ?, ?) ON DUPLICATE KEY UPDATE shares = shares + VALUES(shares)",$count+1,$_SESSION["id"],$symbol,$_POST["shares"]);
        $update=CS50::query("UPDATE users SET cash = cash - ? WHERE id = ?",$t_cost,$_SESSION["id"]);
        //$type="buy";
        $update_history=CS50::query("INSERT IGNORE INTO history(userid,transaction,symbol,shares,price) VALUES(?,?,?,?,?)",$_SESSION["id"],"buy",$symbol,$_POST["shares"],$price);
        
        //display
        $rows=CS50::query("SELECT * FROM portfolios p JOIN users u ON p.user_id=u.id WHERE u.id = ?", $_SESSION["id"]);
                $positions=[];
                foreach($rows as $row)
                {
                    $stk=lookup($row["symbol"]);
                    if ($stk !== false)
                    {
                        $positions[] = [
                        "name" => $stk["name"],
                        "price" => $stk["price"],
                        "shares" => $row["shares"],
                        "symbol" => $row["symbol"]
                        ];
                    }
                }
                if($update!=0)
                {
                    if(count($rows)==1)
                        $cash=$rows[0]["cash"];
                    else
                        $cash=$prev_cash-$t_cost;
                    render("update.php",["title" => "update","cash"=>$cash,"positions"=>$positions]);
                }
    }

?>
