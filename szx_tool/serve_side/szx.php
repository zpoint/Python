<?php
if (!isset($_POST['userid']) or !isset($_POST['version']) or $_SERVER['HTTP_REFERER'] != 'grade_tool')
{
	header('HTTP/1.0 403 Forbidden');
	die('Permission Denied. Only Hamdsome body can access this page'); 
}
$dir = $_SERVER['DOCUMENT_ROOT'].'/szx/'.$_POST['userid'].'/';
if (!is_dir($dir))
	mkdir($dir);
$file_name = $_POST['userid'].'.txt';
$file = fopen($dir.''.$file_name, 'w');

for ($i = 0; $i <= 8;$i++)
{
	fwrite($file, $_POST[strval($i)]."\n");
}
fclose($file);
$url = 'http://localhost/wsgi/szx/'.$_POST['userid'];
$html = file_get_contents($url);
echo $html;
?>
