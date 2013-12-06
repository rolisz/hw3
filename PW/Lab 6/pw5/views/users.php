<div id="luzeri">
    <ul>
		<?php foreach ($users as $user) { ?>
			<li><a href="profile.php?user_id=<?=$user->id;?>"><?=$user->username;?></a></li>
		<?php } ?>
	</ul>
</div>