<?php
// Database connection settings
$host = "ipropostgres.smisc.net";
$port = "5433";
$dbname = "iotsecurity";
$user = "postgres";
$password = "&w9*TCE,8D5t";

$conn_string = "host={$host} port={$port} dbname={$dbname} user={$user} password={$password} sslmode=allow connect_timeout=5";
$dbconn = pg_connect($conn_string);

if (!$dbconn) {
    echo "Error: Unable to connect to the database.\n";
    exit;
}
try {
    // Prepare the SQL query
    $sql = "SELECT login_links.company, logins.username, logins.password 
            FROM login_links 
            JOIN companies ON login_links.company = companies.company 
            JOIN logins ON login_links.loginid = logins.id";
    
    // Execute the query
    $result = pg_query($dbconn, $sql);
    
    // Fetch the results
    $results = pg_fetch_all($result);
    
    // Save results to JSON file
    $jsonFile = 'login_data.json';
    file_put_contents($jsonFile, json_encode($results, JSON_PRETTY_PRINT));
    
    echo "Results saved to $jsonFile";

} catch (Exception $e) {
    // Handle errors
    echo "Error: " . $e->getMessage();
}
?>
