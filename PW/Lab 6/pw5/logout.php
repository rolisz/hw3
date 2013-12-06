<?php
include_once './include/include.php';
session_start();
session_unset();
session_destroy();
setcookie("username", "", time()-3600,"/");
setcookie("credentials", "", time()-3600,"/");
?>