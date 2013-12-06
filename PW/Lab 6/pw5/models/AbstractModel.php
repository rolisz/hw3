<?php
include_once dirname(__FILE__) . '/../include/include.php';

class AbstractModel {
    protected static $columns;
    protected static $table;

    /**
     * This finds objects in database on the assumption that the given property
     * is unique - id, email, username, etc.
     * @param $property
     * @param $value
     * @return an instance or nullnull
     */
    public static function findBy($property, $value) {
        $db = Dispatch::getConnection();
        $table = static::$table;
        $query = $db->query("SELECT * FROM {$table} WHERE {$property}='".$db->escape_string($value)."'");
        if ($query) {
            if ($result = $query->fetch_object(get_called_class())) {
                return $result;
            }
        }
        return null;
    }

	public static function getRelated($col, $id) {
	    $db = Dispatch::getConnection();
        $table = static::$table;
        $query = $db->query("SELECT * FROM {$table} WHERE {$col}='".$db->escape_string($id)."'");
        if ($query) {
			$results = array();
            while ($result = $query->fetch_object(get_called_class())) {
                $results[] = $result;
            }
			return $results;
        }
        return null;
	}
	
	public static function getAllFiltered($filter = '') {
		$db = Dispatch::getConnection();
        $table = static::$table;
		if ($filter != '') {
			$filter = ' WHERE '.$filter;
		}
        $query = $db->query("SELECT * FROM {$table} {$filter}");
        if ($query) {
			$results = array();
            while ($result = $query->fetch_object(get_called_class())) {
                $results[] = $result;
            }
			return $results;
        }
        return null;
	}
	
    public static function findById($id) {
        return static::findBy('id', $id);
    }

    public function update() {
        $updates = '';
        $db = Dispatch::getConnection();
        foreach (static::$columns as $value) {
            $updates .= "`$value`='" . $db->escape_string($this->$value) . "',";
        }
        $updates = substr($updates, 0, strlen($updates) - 1); // get rid of last comma
        $table = static::$table;
        $id = $this->id;
        $sql = "UPDATE {$table} SET {$updates} WHERE `id`={$id}";
        if ($db->query($sql)) {
            return true;
        } else {
            throw new Exception($db->error."\n".$sql);
        }
    }

    public function save() {
        $colname = '(';
        $values = '(';
        $db = Dispatch::getConnection();
        foreach (static::$columns as $value) {
            $colname .= "`$value`" . ',';
            $values .= "'" . $db->escape_string($this->$value) . "'" . ',';
        }
        $colname = substr($colname, 0, strlen($colname) - 1); // getting rid of last comma
        $values = substr($values, 0, strlen($values) - 1);
        $colname .= ')';
        $values .= ')';
        $table = static::$table;
        $sql = "INSERT INTO {$table} {$colname} VALUES {$values}";

        if ($db->query($sql)) {
            $this->id = $db->insert_id;
            return $db->insert_id;
        } else {
            throw new Exception($db->error);
        }
    }

    public function delete() {
        $db = Dispatch::getConnection();
        $table = static::$table;
        $id = $this->id;
        $sql = "DELETE FROM {$table} WHERE id = {$id}";
        if ($db->query($sql)) {
            return;
        } else {
            throw new Exception($db->error);
        }
    }

    /**
     * Executes query and returns first column of first result blindly, without doing any
     * error checking. Use only when there is a guaranteed result (COUNT(*), etc)
     */
    protected static function getFirst($query) {
        $db = Dispatch::getConnection();
        $query = $db->query($query)->fetch_row();
        return $query[0];

    }
}
