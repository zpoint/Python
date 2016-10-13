<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>车票监控系统登陆窗口</title>
<h1 align="center">车票监控系统登陆窗口</h1>
<?php
	require($_SERVER['DOCUMENT_ROOT'].'/lib/db.php');
	session_start();
	$_SESSION['register_flag'] = True;
	
	function valid()
	{
		// check username and password
		$username = trim($_POST['username']);
		$password = trim($_POST['password']);
		if ($username === '')
		{
			$_SESSION['login_err_msg'] = '请输入用户名';
			return False;
		}
		else if ($password === '')
		{
			$_SESSION['login_err_msg'] = '请输入密码';
			return False;
		}
		if (! preg_match('/^[\da-zA-Z]+$/', $username))
		{
			$_SESSION['login_err_msg'] = '用户名不合法';
			return False;
		}
		else if (! preg_match('/^[\da-zA-Z]+$/', $password))
		{
			$_SESSION['login_err_msg'] = '密码不合法';
			return False;
		}
		else if (strlen($username) > 10)
		{
			$_SESSION['login_err_msg'] = '用户名长度过长';
			return False;
		}
		else if (strlen($username) < 3)
		{
			$_SESSION['login_err_msg'] = '用户名过短';
			return False;
		}
		else if (strlen($password) > 18)
		{
			$_SESSION['login_err_msg'] = '密码长度过长';
			return False;
		}
		else if (strlen($password) < 6)
		{
			$_SESSION['login_err_msg'] = '密码长度过短';
			return False;
		}
		
		$db = db_connect('site');
		$query = 'select * from train where username = "'.$username.'";';
		$result = $db->query($query);
		$row = $result->fetch_assoc();
		if ($row == NULL)
		{
			$_SESSION['login_err_msg'] = '无此用户';
			return False;
		}
		else if ($row['password'] != $password)
		{
			$_SESSION['login_err_msg'] = '密码错误';
			return False;
		}
		else // correct user, correct password, set login flag
		{
			$query = 'update train set login_time = NOW() where username = "'.$username.'"';
			$result = $db->query($query);
			$db->commit();
			$_SESSION['userrow'] = $row;
		}
		return True;
	}
	
	function echo_login()
	{
		if (isset($_SESSION['login_err_msg']) && $_SESSION['login_err_msg'] != False)
			echo '<p align="center">'.$_SESSION['login_err_msg'].', 请重新登录</p>';
		else
			echo '<p align="center">请登录</p>';
		echo '<form action="train_login.php" method="post">
		<table border=0 align="center">
		<tr>
		<td>用户名</td>
		<td><input type="text" name="username" pattern="^[\da-zA-Z]{3,10}$" title="请输入注册时的用户名" /></td>
		<td>密码</td>
		<td><input type="password" name="password" pattern="^[\da-zA-Z]{6,18}$" title="请输入注册时的密码,忘记密码email我, zp0int@qq.com " /></td>
		</tr></table>
	
		<table border=0 align="center">
		<tr><td><a href="train_register.php">新用户?点我注册</a></td>
		<td><input type="submit" align="center" value="登陆" /></td>
		</tr></table>
		</form>';
	}
	if (isset($_POST['logout']))
	{
		session_destroy();
		echo_login();
	}
	else if (!isset($_POST['username']) || !isset($_POST['password']))
		echo_login();
	else
	{
		if (!valid())
			echo_login();
		else
		{
			// success in login
			$_SESSION['login_err_msg'] = False;
			echo '<p align="center"><a href="train.php">登陆成功, <span id="time">3</span> 秒后跳转, 或者点我登陆</a></p>
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
					window.location.href = "train.php";
				}        
				} 
				</script>';
		}
		
	}
?>	
</body>
</html>
	