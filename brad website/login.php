
<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Hardcoded credentials
    $hardcoded_username = 'neuuni';
    $hardcoded_password_hash = password_hash('123456', PASSWORD_DEFAULT);

    // Check if the provided username matches the hardcoded username
    if ($username === $hardcoded_username && password_verify($password, $hardcoded_password_hash)) {
        $_SESSION['username'] = $username;
        header("Location: dashboard.php"); // Make sure the path is correct
        exit();
    } else {
        $error = "Invalid username or password";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="style.css">  <!-- Adjust this path if necessary -->
</head>
<body>
    <header>
        <h1>Smart Beekeeping - Login</h1>
    </header>
    <main>
        <?php
        if (isset($error)) {
            echo "<p style='color:red;'>$error</p>";
        }
        ?>
        <form action="login.php" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="register.php">Register here</a>.</p>
    </main>
</body>
</html>
