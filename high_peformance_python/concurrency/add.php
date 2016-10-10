<?php
$name = $_GET['name'];
$delay = $_GET['delay'];
echo "name:".$name."<br />";
echo "delay:".$delay."<br />";
echo "I am going to sleep for ".$delay." millisceonds <br />";
usleep($delay * 1000);
echo "done<br />Hello!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! <br />";
?>
