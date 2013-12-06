<form class="form-horizontal" id="regForm" name="regForm" method="POST">
	<div class="control-group">
		<label class="control-label" for="username">Nume de utilizator</label>
		<div class="controls">
			<input type="text" id="username" name="username"
				   placeholder="Nume utilizator" pattern="[a-zA-Z][a-zA-Z0-9_.-]{2,15}" required>
		</div>
	</div>
	<div class="control-group">
		<label class="control-label" for="password">Parola</label>
		<div class="controls">
			<input type="password" id="password" name="password"
				   placeholder="Parola" required>
		</div>
	</div>
	<div class="control-group">
		<label class="control-label" for="password2">Confirmare parola</label>
		<div class="controls">
			<input type="password" id="password2" name="password2"
				   placeholder="Parola încă o dată" required>
		</div>
	</div>

	<div class="control-group">
		<label class="control-label" for="email">Email</label>
		<div class="controls">
			<input type="email" id="email" name="email"
				   placeholder="Email" required>
		</div>
	</div>
	<div class="control-group">
		<div class="controls">
			<button type="submit" class="btn btn-primary">Inregistrare</button>
		</div>
	</div>
</form>