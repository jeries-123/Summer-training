<?php
include 'myDB.php';  // Adjust this path if necessary

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);  // Hash the password

    // Insert into users table
    $sql_users = "INSERT INTO register (username, password) VALUES ('$username', '$password')";

    // Insert into login table
    $sql_login = "INSERT INTO login (username, password) VALUES ('$username', '$password')";

    if ($conn->query($sql_users) === TRUE && $conn->query($sql_login) === TRUE) {
        header("Location: login.php");
        exit();
    } else {
        $error = "Error: " . $conn->error;
    }
    
    $conn->close();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link rel="stylesheet" href="style.css">  <!-- Adjust this path if necessary -->
</head>
<body>
    <header>
        <h1>Smart Beekeeping - Register</h1>
    </header>
    <main>
        <?php
        if (isset($error)) {
            echo "<p style='color:red;'>$error</p>";
        }
        ?>
        <form action="register.php" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            
            <button type="submit">Register</button>
        </form>
        <p>Already have an account? <a href="login.php">Login here</a>.</p>
    </main>
</body>
</html>
