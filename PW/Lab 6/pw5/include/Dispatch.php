<?php
/**
 * Helper class for several random stuff, that are needed on pretty much every page:
 * db connection, getting user language, getting online user count
 */
class Dispatch {
    private static $connection;
    private static $online;
	private static $flash_messages = '';
	
    public static function getConnection() {
        if (Dispatch::$connection == null) {
            // Enviroment is switched between dev and production using the ENV environment variable
            // For Apache, using mod_env, use "SetEnv ENV development" in .htaccess file
            if ($_SERVER['ENV'] == 'development') {
                $mysqli = new mysqli("localhost", "root", "", "pw");
            }
            
            if ($mysqli->connect_errno) {
                echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
            }
            $mysqli->query('SET NAMES utf8');
            $mysqli->query('SET CHARACTER SET utf8');
            $mysqli->query('SET COLLATION_CONNECTION="utf8_general_ci"');
            Dispatch::$connection = $mysqli;
        }
        return Dispatch::$connection;
    }

    /*
     * Get the contents of a view from the folder views, where the variables are
     * given in the $params argument
     */
    public static function getView($file, $params = array(), $folder = '') {
        $file = dirname(__FILE__)."/..$folder/views/".$file;
        if (is_file($file)) {
            extract($params);
			if (array_key_exists('flash', $_SESSION) && count($_SESSION['flash']) > 0) {
				Dispatch::$flash_messages = $_SESSION['flash'];
				$_SESSION['flash'] = array();
			}
			$flash_messages = Dispatch::$flash_messages;
            ob_start();
            include $file;
            return ob_get_clean();
        }
        throw new Exception("File not found: ".$file);
    }


    public static function randomString($length = 20) {
        $characters = '0123456789abcdefghijklmnopqrstuvwxyz';
        $randstring = '';
        for ($i = 0; $i < $length; $i++)
        {
            $randstring .= $characters[rand(0, strlen($characters) - 1)];
        }
        return $randstring;
    }

    /**
     * Generate a link to a message list, to a certain page, to a certain speaker
     * or a certain year
     * Param should be m for testimony, vb for speaker, an for year
     */
    public static function generateLink($pos, $param = '', $value = '') {
        $pos = 'index.php?'.(($pos > 0)?'poz='.$pos:'');
        $link = $pos;
        if ($param != '') {
            return $link."&$param=".htmlentities($value);
        }
        if (count($_GET) > 1) {
            foreach ($_GET as $key => $value) {
                if (array_search($key,array('vb','an','m'))) {
                    return $link."&$key=".htmlentities($value);
                }
            }

        }
        return $pos;
    }

    public static function redirectTo($url) {
        header("Location: $url");
        exit();
    }

    /**
     * Return $_GET[$key] or default if the key is not set.
     * @param $key
     * @param $default
     * @return string
     */
    public static function GET($key, $default = '') {
        if (isset($_GET[$key])) {
            return $_GET[$key];
        }
        return $default;
    }

    /**
     * @param string $env - environment URL to return
     * @return string
     */
    public static function getPictureUrl($env = '') {
        if ($env == '') {
            $env = $_SERVER['ENV'];
        }
        if ($env == 'development') {
            $str = './upload/images/';
        }
        return $str;
    }

	public static function flash($message, $type = 'error') {
		if (!array_key_exists('flash', $_SESSION)) {
			$_SESSION['flash'] = array();
		}
		
		if(!array_key_exists($type, $_SESSION['flash'])) {
			$_SESSION['flash'][$type] = array();
		}
		$_SESSION['flash'][$type][] = $message;
	}
	
}
