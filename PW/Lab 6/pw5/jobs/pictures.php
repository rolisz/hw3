<?php
include_once '/../include/include.php';
/**
 * User: Roland
 * Date: 7/24/13
 * Time: 3:53 PM
 */
$mysqli = Dispatch::getConnection();

$mysqli->query("DROP TABLE `pictures`");

$sql = "CREATE TABLE `pictures` (
        `id` INTEGER NOT NULL AUTO_INCREMENT DEFAULT NULL,
        `name` VARCHAR(50),
		`file` VARCHAR(50),
		`user_id` INTEGER,
  PRIMARY KEY (`id`)
)";


if ($mysqli->query($sql) === TRUE) {
    echo "Pictures created succesfully";
    echo $mysqli->error;
}
else {
    echo $mysqli->error;
}
