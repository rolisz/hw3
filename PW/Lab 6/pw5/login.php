<?php
include_once './include/include.php';

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	$content = Dispatch::getView('login.php');	
	echo Dispatch::getView('frame.php',array('styles'=> array('bootstrap.min','bootstrap-responsive.min','base'),
                                        'title' => "Login to Ninstagram",
                                        'content'=>$content,
                                        ));

}
else {
	if ($user = User::findByUsernameAndPass($_POST['username'], $_POST['password'])) {
		$user->login($_POST['remember']);
		Dispatch::redirectTo('index.php');
	} else {
		Dispatch::redirectTo('login.php');
	}

}
?>
