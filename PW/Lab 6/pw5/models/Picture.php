<?php
include_once dirname(__FILE__) . '/../include/include.php';

class Picture extends AbstractModel {
	public $id;
	public $file = '';
	public $name = '';
	public $user_id = '';
	
    protected static $columns = array('id',
        'file',
        'name',
		'user_id'
        );

    protected static $table = 'pictures';

    public function delete() {
        if (file_exists(Dispatch::getPictureUrl().$this->file)) {
            unlink(Dispatch::getPictureUrl().$this->file);
        }
        parent::delete();
    }

    public function update() {
        if (isset($this->prev_file) && file_exists(Dispatch::getPictureUrl().$this->prev_file)) {
            rename(Dispatch::getPictureUrl().$this->prev_file,
                Dispatch::getPictureUrl().$this->file);
        }
        parent::update();
    }

}
