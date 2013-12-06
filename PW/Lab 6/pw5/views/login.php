<form class="form-horizontal"  method="POST" action="login.php">
	<div class="control-group">
		<label class="control-label" for="inputUser">Nume utilizator</label>

		<div class="controls">
			<input type="text" id="inputUser" name="username"
				   placeholder="Username">
		</div>
	</div>
	<div class="control-group">
		<label class="control-label" for="inputPassword">Parola</label>

		<div class="controls">
			<input type="password" id="inputPassword" name="password"
				   placeholder="Password">
		</div>
	</div>
	<div class="control-group">
		<div class="controls">
			<label class="checkbox">
				<input type="checkbox" id="rememberMe" name="remember"/>Ține-mă minte
			</label>
			<a class="btn btn-info" href="register.php">Inregistrare</a>
			<button type="submit" class="btn btn-primary">Login</button>
		</div>
	</div>
</form>
<div>

</div>