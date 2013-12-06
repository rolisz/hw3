<?php
include_once('include/include.php');

if (($user = User::getLoggedin()) == null) {
    Dispatch::redirectTo('index.php');
}

$user  = isset($_GET['user_id']) ? User::findById($_GET['user_id']) : User::getLoggedin();

if ($_SERVER['REQUEST_METHOD'] == 'POST' && $user == User::getLoggedin()) {
	if (move_uploaded_file($_FILES['picture']['tmp_name'],Dispatch::getPictureUrl().$_FILES['picture']['name'])) {
		$picture = new Picture();
		$picture->name = $_POST['title'];
		$picture->file = $_FILES['picture']['name'];
		$picture->user_id = $user->id;
		$picture->save();
	}
	else {
		Dispatch::flash("S-a intamplat o eroare!");
	}
}

echo Dispatch::getView('frame.php',array('title' => "Profil user",
            'content' => Dispatch::getView('profile.php', array('user'=> $user)),
            'footer' => ''));

?>