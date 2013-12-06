<?php
include_once dirname(__FILE__) . '/../include/include.php';

define('SALT',"5zND5chnJNwaZVAJ5UJC");

/**
 *
 * mcrypt_create_iv didn't work on server.
 * If it gets installed, should be remove
 * @param $size
 * @param string $useless - for compatibility with mcrypt
 * @return string
 */
function alt_mcrypt_create_iv ($size, $useless = '') {
    $iv = '';
    for($i = 0; $i < $size; $i++) {
        $iv .= chr(rand(0,255));
    }
    return $iv;
}
class User extends AbstractModel{
    public $id;
    public $username;
    public $name;
    public $email;
    public $password;
    public $salt;
    
    protected static $columns = array('id',
        'username',
        'name',
        'email',
        'password',
        'salt',
        );

    private static $currentUser = null;
    protected static $table = 'users';

    public function __construct($username = '', $password = '', $name = '',
                                $email = '') {
        if (!$this->salt && !$this->password) { // fetch_object sets attributes before calling
                                 // constructor
            $this->username = $username;
            $salt = alt_mcrypt_create_iv(16);
            $this->password = sha1($salt.$password);
            $this->salt = $salt;
            $this->name = $name;
            $this->email = $email;
        }
		$this->pictures = null;
    }

    public static function findByEmail($email) {
        return static::findBy('email', $email);
    }

    public static function findByUsername($username) {
        return static::findBy('username', $username);
    }

    public static function findByUsernameAndPass($username, $password) {
        if ($user = User::findByUsername($username)) {
            if (sha1(($user->salt).$password) == $user->password) {
                return $user;
            }
        }
        return null;
    }

    /*
     * Logs in this user, with option to make him persistent (cookies or
     * session only)
     */
    public function login($remember = false) {
        $db = Dispatch::getConnection();

        $this->update();
        $_SESSION['user'] = $this->username;
        $_SESSION['pw'] = $this->password;
        if ($remember) {
            $crypted_credentials = openssl_encrypt($this->password,'aes-256-cbc',SALT,false,$this->salt);
            setcookie('username',$this->username,time()+60*60*24*300,'/');
            setcookie('credentials',$crypted_credentials,time()+60*60*24*300,'/');
        }
    }

    /*
     * Checks the credentials in session, if they are not valid, checks the one in cookies.
     * If they are valid, update session credentials.
     * Return either currently logged in user or null
     */
    public static function getLoggedin() {
        if (User::$currentUser !== null) {
            return User::$currentUser;
        }
        if (array_key_exists('user',$_SESSION) && array_key_exists('pw',$_SESSION)) {
            $username = $_SESSION['user'];
            $password = $_SESSION['pw'];
            $user = User::findByUsername($username);
            if ($user !== null and $user->password == $password) {
                User::$currentUser = $user;
                return $user;
            }
        }
        if (isset($_COOKIE['username']) && isset($_COOKIE['credentials'])) {
            $username = $_COOKIE['username'];
            $credentials = $_COOKIE['credentials'];
            $user = User::findByUsername($username);
            if ($user !== null) {
                $salt = $user->salt;
                $decrypted_credentials = openssl_decrypt($credentials,'aes-256-cbc',SALT,false,$salt);
                if ($user->password == $decrypted_credentials) {
                    $_SESSION['user'] = $user->username;
                    $_SESSION['pw'] = $user->password;
                    User::$currentUser = $user;
                    return $user;
                }
            }
        }
        return null;
    }

	public function pictures() {
		if ($this->pictures != null) {
			return $this->pictures;
		}
		$this->pictures = Picture::getRelated('user_id', $this->id);
		return $this->pictures;
	}
}
