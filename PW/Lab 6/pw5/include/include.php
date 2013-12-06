<?php
/*
 * The glorious autoloader.
 */

spl_autoload_register(function ($class) {
    $file = dirname(__FILE__).'/'.$class.'.php';
    if (is_readable($file)) {
        include $file;
    }
    $file = dirname(__FILE__).'/../models/'.$class.'.php';
    if (is_readable($file)) {
        include $file;
    }
});


//First thing always
session_start();
