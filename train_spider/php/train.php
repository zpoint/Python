<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>
<?php
require($_SERVER['DOCUMENT_ROOT'].'/lib/db.php');
require($_SERVER['DOCUMENT_ROOT'].'/train/train_data.php'); # for $train_array
/*
* post to wsgi format   url + username + "@@@" + data + "@@@" + tsn + "@@@" + fsn
* store in mysql format url + "@@@" + each_dict['车次']
*/
session_start();
$_SESSION['train_array'] = $train_array;

	function echo_myurl($msg = False)
	{
			if ($msg != False)
					echo '<p align="center">'.$msg.'</p>';
			echo "<h2 align=\"center\">目前正在监控的车次</h2>";
			if ($_SESSION['userrow']['url0'] == '') // No result
			{
				echo "<p align=\"center\">您目前无在监控车次，请搜索并添加</p>";
				$_SESSION['row_index'] = -1;
			}
			else // result
			{
					echo '<table id="mytable" align="center" border=1>';
					echo '<tr><td align="center">车次</td><td align="center">日期</td><td align="center">出发站</td><td align="center">到站</td><td align="center">修改</ td>';
					$maxrow = intval($_SESSION['userrow']['max_url']);
					for ($i = 0; $i < $maxrow; $i++)
					{
						if ($_SESSION['userrow']['url'.$i] == '')
						{
							// NULL or '' are the same in php
							$_SESSION['row_index'] = $i - 1;
							break;
						}
						$result = explode('@@@', $_SESSION['userrow']['url'.$i]);
						parse_str($result[0], $output);
						echo "<tr><form action=\"train.php\" method=\"post\"><input type=\"hidden\" name=\"delete_index\" value=".$i."\" />
							<td align='center'>".$result[1]."</td>
							<td align='center'>".$output['https://kyfw_12306_cn/otn/leftTicket/queryT?leftTicketDTO_train_date']."</td>
							<td align='center'>".$_SESSION['train_array'][$output['leftTicketDTO_from_station']]."</td>
							<td align='center'>".$_SESSION['train_array'][$output['leftTicketDTO_to_station']]."</td>
							<td align='center'><input type=\"submit\" align=\"center\" value=\"删除\" /></td></tr></form>";
					}
			}
					  
	}
	function echo_basic()
	{
		echo '<head>
			 <meta http-equiv="content-type" content="text/html; charset=utf-8" />
			 <title>12306车票监控系统(BETA)</title>
			 </head>
			<body>
			<h1 align="center">12306车票监控系统(BETA)</h1>
	
			<p align="center">尊敬的 <b align="center" id="username">'.$_SESSION['userrow']['username'].'</b>, 本程序会在后台每隔数秒左右刷新一次剩余票数!!!<br />当系统检测到车票数目变化时会自动发邮件提醒您!!!<br /></p>
			<form action="train.php" method="post">
			<table border=0 align="center">
			<tr>
			<td>出发站</td>
			<td><input type="text" name="from_station_name" title="请输入不为空的中文站名" pattern="^[\u4e00-\u9fa5]{1,15}$" /></td>
			<td>目的站</td>
			<td><input type="text" name="to_station_name" title="请输入不为空的中文站名" pattern="^[\u4e00-\u9fa5]{1,15}$" /></td>
			<td>发车日期</td>
			<td><input type="text" name="start_train_date" pattern="^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$" title="格式:2016-12-31 , 请输入大于当前日期的值" /></td>
			<input type="hidden" name="search_flag" value="True">
			<td><input type="submit" align="center" value="搜索" /><td>
			</tr></table></form>';
	}
	
	function echo_search()
	{
		$_SESSION['last_search'] = file_get_contents('http://localhost/wsgi/train/'.$_SESSION['userrow']['username'].'@@@'.$_POST['start_train_date'].'@@@'.$_POST['to_station_name'].'@@@'.$_POST['from_station_name']);
		echo $_SESSION['last_search'];
	}
	
	if (!isset($_SESSION['userrow']))
	{
			echo '<p align="center"><a href="train_login.php">请先登录再进入本系统, <span id="time">4</span> 秒后跳转, 或者点我登陆</a></p>
				<script type="text/javascript">  
				delayURL();    
				function delayURL() { 
					var delay = document.getElementById("time").innerHTML;
					var t = setTimeout("delayURL()", 1000);
				if (delay > 0) {
					delay--;
					document.getElementById("time").innerHTML = delay;
				} else {
					clearTimeout(t); 
					window.location.href = "train_login.php";
				}        
				} 
				</script>';
	}
	else
	{
		$msg = False;
		echo_basic();
		//echo "before:_SESSION['row_index']".var_dump($_SESSION['row_index'])."<br />";
		//echo "before:intval(_SESSION['userrow']['max_url'])".var_dump(intval($_SESSION['userrow']['max_url']))."<br />";
	
		if (isset($_POST['search_flag']))
		{
				//search
				echo_search();
		}
		
		else if(isset($_POST['delete_index'])) //delete
		{
			// update 
			$username = $_SESSION['userrow']['username'];
			$i = intval($_POST['delete_index']);
			$db = db_connect('site');
			for ($j = $_SESSION['row_index'] - 1; $j >= $i; $j--)
			{
				$query = 'update train set url'.$j.' = "'.$_SESSION['userrow']['url'.($j + 1)].'" where username = "'.$username.'"';
				$result = $db->query($query);
			}
			$query = 'update train set url'.$_SESSION['row_index'].' = "" where username = "'.$username.'"';
			$result = $db->query($query);
			$query = 'update train set login_time = NOW() where username = "'.$username.'"';
			$result = $db->query($query);
			$db->commit();
			// fetch newest data
			$query = 'select * from train where username = "'.$username.'";';
			$result = $db->query($query);
			$row = $result->fetch_assoc();	
			$_SESSION['userrow'] = $row;
			$_SESSION['row_index'] -= 1;
			if (isset($_SESSION['last_search']))
				echo $_SESSION['last_search'];
			$msg = "删除成功, 由于服务器资源限制, 您的删除请求将在 <b>3</b> 分钟内生效";
		}
		else if (isset($_POST['add_url'])) // combined url ,with @@@ inside
		{
			$username = $_SESSION['userrow']['username'];
			if ($_SESSION['row_index'] >= intval($_SESSION['userrow']['max_url']) - 1)
				$msg = "添加失败, 您同时只能监控 <b>".$_SESSION['userrow']['max_url']."</b> 个班次, 要加大限制， 请给管理员<b> zp0int@qq.com </b>发红包";
			else
			{
				for ($i = 0; $i <= $_SESSION['row_index']; $i++)
					if ($_SESSION['userrow']['url'.$i] == $_POST['add_url'])
						$msg = "添加失败, 您的监控列表中已含有该车次";
				if ($msg == False) // success in adding
				{
					$_SESSION['row_index'] += 1;
					$db = db_connect('site');
					$query = 'update train set url'.($_SESSION['row_index']).' = "'.$_POST['add_url'].'" where username = "'.$username.'"';
					$result = $db->query($query);
					$query = 'update train set login_time = NOW() where username = "'.$username.'"';
					$result = $db->query($query);
					$commit = $db->commit(); // commit change
			
					$_SESSION['userrow']['url'.$_SESSION['row_index']] = $_POST['add_url'];
					$msg = "添加成功, 由于服务器资源限制, 您的添加请求将会在 <b>3</b> 分钟内生效";
				}
			}
			
			if (isset($_SESSION['last_search']))
				echo $_SESSION['last_search'];
		}
		else  // first time
		{
		}
		echo_myurl($msg);
		//echo "Aftrer:_SESSION['row_index']".var_dump($_SESSION['row_index'])."<br />";
		//echo "After:intval(_SESSION['userrow']['max_url'])".var_dump(intval($_SESSION['userrow']['max_url']))."<br />";
		echo '<table align="center" ><form action="train_login.php" method="post" ><input type="hidden" value="True" name="logout" /><tr><td align="center"><input type="submit" value="注销" /></form></table>';
	}
	
	
?>
</body>
</html>
