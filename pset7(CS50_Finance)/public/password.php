<?php

    // configuration
    require("../includes/config.php");

    // if user reached page via GET (as by clicking a link or via redirect)
    if ($_SERVER["REQUEST_METHOD"] == "GET")
    {
        // else render form
        render("password_change.php", ["title" => "Password"]);
    }

    // else if user reached page via POST (as by submitting a form via POST)
    else if ($_SERVER["REQUEST_METHOD"] == "POST")
    {
        // validate submission
        if (empty($_POST["old_password"]))
        {
            apologize("You must provide your existing password.");
        }
        else if (empty($_POST["new_password"]))
        {
            apologize("You must provide a new password.");
        }
        else if ($_POST["confirm"] != $_POST["new_password"])
        {
            apologize("Passwords do not match.");
        }
        else if ($_POST["old_password"] == $_POST["new_password"])
        {
            apologize("Try a different password.");
        }
        
        //query
        $update_password=CS50::query("UPDATE users SET hash = ? WHERE id = ?",password_hash($_POST["new_password"],PASSWORD_DEFAULT),$_SESSION["id"]);
        if ($update_password == 0)
        {
            apologize("Error resetting password. ");
        }
        else
        {
            $rows = CS50::query("SELECT LAST_INSERT_ID() AS id");
            $id = $rows[0]["id"];
            // remember that user's now logged in by storing user's ID in session
            $_SESSION["id"] = $id;

            // redirect to index
            redirect("index.php");
        }
    }

?>