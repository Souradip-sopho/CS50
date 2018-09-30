<?php

    // configuration
    require("../includes/config.php");

    // if user reached page via GET (as by clicking a link or via redirect)
    if ($_SERVER["REQUEST_METHOD"] == "GET")
    {
        // else render form
        render("quote_form.php", ["title" => "Stock"]);
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
            $stock=lookup($_POST["symbol"]);
            if($stock== false)
            {
                apologize("Invalid symbol.");
            }
            else
            {
                $Price=$stock["price"];
                $price = number_format($Price,2);
                $message="Price:{$price}";
                render("quote_price.php",["message" => $message]);
            }
        }
    }

?>