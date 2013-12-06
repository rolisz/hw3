<?php
$db = Dispatch::getConnection();
?>
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="assets/css/bootstrap.min.css"/>
        <link rel="stylesheet" type="text/css" href="assets/css/bootstrap-responsive.min.css"/>
        <link rel="stylesheet" type="text/css" href="assets/css/base.css"/>
        <link rel="stylesheet" type="text/css" href="assets/css/fontello.css"/>
        <title>
            <?php echo $title; ?>
        </title>
	</head>
	<body>
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
                    <div class="row-fluid">
                    <button class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="brand homepage-link" href="./">Ninstagram</a>
                    <div class="nav-collapse collapse fright">
                        <ul class="nav">
                            <?php if (User::getLoggedin() != null) { ?> <li><a href="profile.php" id="admin" class="meniu">Profil</a></li> <?php }?>
                            <?php if (User::getLoggedin() == null) { ?>
                                <li><a href="../login.php" id="loginBtn">Login</a></li>
                            <?php } else {  ?>
                                <li><a href="logout.php"  id="logoutBtn">Logout</a></li>
                            <?php } ?>
                        </ul>
                    </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container-fluid main-content">
			<?php if ($flash_messages != '') {
				foreach ($flash_messages as $type => $messages) {
					foreach ($messages as $message) { ?>
						<div class="<?=$type?>"><?=$message?></div>
					<?php }
				}
			} ?>
            <div class="row-fluid">

                <?php echo $content; ?>

            </div>
        </div>
        <div id="footer">
            <div class="row-fluid">
               Copyright - rolisz
            </div>
        </div>
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/bootstrap.js"></script>
        <script src="assets/js/main.js"></script>
	</body>
</html>