<?php
$month = isset($_GET['month'])?$_GET['month']:"12";
$year = isset($_GET['year'])?$_GET['year']:"2013";

function month_link($year, $month) {
	if ($month == 0) {
		$month = 12;
		$year = $year - 1;
	}
	if ($month == 13) {
		$month = 1;
		$year = $year + 1;
	}
	return "calendar.php?month=$month&year=$year";
}
function generate_calendar($year, $month){
    $first_of_month = gmmktime(0,0,0,$month,1,$year);

	$first_day = 0;
    $day_names = array(); 
    for($n=0,$t=(3+$first_day)*86400; $n<7; $n++,$t+=86400)  {
        $day_names[$n] = ucfirst(gmstrftime('%A',$t)); 
	}

    list($month, $year, $month_name, $weekday) = explode(',',gmstrftime('%m,%Y,%B,%w',$first_of_month));
    $weekday = ($weekday + 7 - $first_day) % 7; 
    $title   = ucfirst($month_name).'&nbsp;'.$year;

    $p = '<span class="calendar-nav"><a href="'.month_link($year, $month-1).'">Prev</a></span>&nbsp;';
    $n = '&nbsp;<span class="calendar-nav"><a href="'.month_link($year, $month+1).'">Next</a></span>';
    $calendar = '<table class="calendar"><caption class="calendar-month">'.$p.$title.$n."</caption>\n<tr>";

	foreach($day_names as $d) {
		$calendar .= '<th abbr="'.$d.'">'.substr($d,0,3).'</th>';
	}
	$calendar .= "</tr>\n<tr>";
    
    if($weekday > 0) {
		$calendar .= '<td colspan="'.$weekday.'">&nbsp;</td>'; 
	}
    for($day=1,$days_in_month=gmdate('t',$first_of_month); $day<=$days_in_month; $day++,$weekday++){
        if($weekday == 7){
            $weekday   = 0; #start a new week
            $calendar .= "</tr>\n<tr>";
        }
		$calendar .= "<td>$day</td>";
    }
    if($weekday != 7) { 
		$calendar .= '<td colspan="'.(7-$weekday).'">&nbsp;</td>'; 
	}

    return $calendar."</tr>\n</table>\n";
}
echo generate_calendar($year, $month);
?>