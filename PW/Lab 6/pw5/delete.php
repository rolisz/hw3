<?php
include_once('include/include.php');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	$user = User::getLoggedin();
	$picture = Picture::findById($_POST['picture_id']);
	if ($picture && $picture->user_id == $user->id) {
		$picture->delete();
	
	}
	else {
		Dispatch::flash("Nu aveti voie sa stergeti poza asta!");
	}
	Dispatch::redirectTo('profile.php');
} 
else {
	Dispatch::redirectTo('index.php');
}
?>
