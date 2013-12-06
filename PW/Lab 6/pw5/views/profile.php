<div id="profil">
    <h2>Pozele lui <?=$user->username?></h2>
	<?php if ($user->pictures() == null) { ?>
		Nu are nicio poza!
	<?php } else { ?>
		<ul id="pic_list">
		<?php foreach ($user->pictures() as $picture) { ?>
			<li><img src="<?=Dispatch::getPictureURL().$picture->file;?>"><span><?=$picture->name?>	
			<?php if ($user->id == User::getLoggedin()->id) { ?>
				<form method="POST" action="delete.php">
					<input type="hidden" name="picture_id" value="<?=$picture->id?>">
					<button type="submit" class="btn btn-warning">Delete</button>
				</form>
			<?php } ?>
			</li>
		<?php } ?>
		</ul>
	<?php } ?>
	
	<?php if ($user->id == User::getLoggedin()->id) { ?>
		<form method="POST" action="profile.php" enctype="multipart/form-data">
			<div class="control-group">
				<div class="controls">
					<input type="file" name="picture">
				</div>
			</div>
			<div class="control-group">
				<label class="control-label" for="title">Titlu</label>
				<div class="controls">
					<input type="text" name="title">
				</div>
			</div>
			<div class="control-group">
				<div class="controls">
					<button type="submit" class="btn btn-primary">Upload</button>
				</div>
			</div>
		</form>
	<?php } ?>
</div>