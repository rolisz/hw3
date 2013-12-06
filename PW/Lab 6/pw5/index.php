<?php
include_once('include/include.php');

if (User::getLoggedin() == null) {
	$content = Dispatch::getView('login.php');	
}
else {
	$content = Dispatch::getView('users.php', array('users'=> User::getAllFiltered()));
}

echo Dispatch::getView('frame.php',array('styles'=> array('bootstrap.min','bootstrap-responsive.min','base'),
                                        'title' => "Ninstagram",
                                        'content'=>$content,
                                        ));
?>
