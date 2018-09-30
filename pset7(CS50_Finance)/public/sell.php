<?php

    // configuration
    require("../includes/config.php");

    // if user reached page via GET (as by clicking a link or via redirect)
    if ($_SERVER["REQUEST_METHOD"] == "GET")
    {
        // else render form
        render("sell_form.php", ["title" => "Sell"]);
    }

    // else if user reached page via POST (as by submitting a form via POST)
    else if ($_SERVER["REQUEST_METHOD"] == "POST")
    {
        if(empty($_POST["symbol"]))
        {
            apologize("You must provide a symbol.");
        }
        else
        {   
            $flag=0;
            $row=NULL;
            $rows=CS50::query("SELECT * FROM portfolios p JOIN users u ON p.user_id=u.id WHERE u.id = ?", $_SESSION["id"]);
            foreach($rows as $row)
            {
                if($row["symbol"]==$_POST["symbol"])
                {
                    $flag=1;
                    break;
                }
            }
            if($flag==0)
            {
                apologize("No Such Shares.");    
            }
            else
            {
                $stock=lookup($_POST["symbol"]);
                $owed=$stock["price"]*$row["shares"];
                $prev_cash=$rows[0]["cash"];
                $deleted=CS50::query("DELETE FROM portfolios WHERE user_id = ? AND symbol = ?",$_SESSION["id"],$_POST["symbol"]);
                $update=CS50::query("UPDATE users SET cash = cash + ? WHERE id = ?",$owed,$_SESSION["id"]);
                $type="sell";
                $update_history=CS50::query("INSERT IGNORE INTO history(userid,transaction,symbol,shares,price) VALUES(?,?,?,?,?)",$_SESSION["id"],$type,$_POST["symbol"],$row["shares"],$stock["price"]);
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
                        $cash=$prev_cash+$owed;
                    render("update.php",["title" => "update","cash"=>$cash,"positions"=>$positions]);
                }
            }
        }
    }

?>