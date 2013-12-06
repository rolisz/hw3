<?php
include_once './include/include.php';
/*
 * If the page is requested using GET, show the registration form, otherwise
 * try to authenticate the user
 */
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	$content = Dispatch::getView('register.php');	
	echo Dispatch::getView('frame.php',array('styles'=> array('bootstrap.min','bootstrap-responsive.min','base'),
                                        'title' => "Inregistrare",
                                        'content'=>$content,
                                        ));
} else {
    $errors = false;
    //todo return error messages as well
    if (filter_var($_POST['email'], FILTER_VALIDATE_EMAIL) == false|| User::findByEmail($_POST['email'])) {
		Dispatch::flash('Adresa de email introdusa nu este valida!');
		$errors = true;
    }
    if ($_POST['password'] != $_POST['password2']) {
        Dispatch::flash('Parolele nu coincid!');
		$errors = true;
    }
    if (strlen($_POST['password']) < 6) {
        Dispatch::flash('Parola este prea scurta!');
		$errors = true;
    }
    if (!preg_match('/^[a-zA-Z][a-zA-Z0-9_.-]{2,15}$/', $_POST['username'])) {
        Dispatch::flash('Numele de utilizator trebuie sa aiba intre 2 si 15 caractere si sa fie format din litere, cifre si _, . sau -');
		$errors = true;
    }
    if (User::findByUsername($_POST['username'])){
        Dispatch::flash('Exista deja utilizator cu acest nume!');
		$errors = true;
    }
    if (!$errors) {
        $user = new User($_POST['username'], $_POST['password'], '', $_POST['email']);
        try{
            $user->save();
            $user->login();
            Dispatch::redirectTo('index.php');
        }
        catch (Exception $e) {
			Dispatch::flash($e->getMessage());
            Dispatch::redirectTo('register.php');
        }
    } else {
		Dispatch::redirectTo('register.php');
    }
}
?>