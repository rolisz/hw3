<?php
/**
 * Drops the users table and recreates it!
 */
include_once '../include/include.php';
$mysqli = Dispatch::getConnection();

$mysqli->query("DROP TABLE `users`");

$sql = "CREATE TABLE `users` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `username` VARCHAR(30),
  `name` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(60) NULL DEFAULT NULL,
  `password` TEXT(120) NULL DEFAULT NULL,
  `salt` BINARY(16) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
)";


if ($mysqli->query($sql) === TRUE) {
    echo "Users created succesfully";
}
else {
    echo $mysqli->error;
}
