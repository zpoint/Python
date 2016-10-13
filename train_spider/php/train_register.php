<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<?php
	session_start();
	require($_SERVER['DOCUMENT_ROOT'].'/lib/db.php');
	
?>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>车票监控系统注册窗口</title>
<h1 align="center">车票监控系统注册窗口</h1>
<?php
	function register_echo()
	{
			
			if (isset($_SESSION['err_msg']) && $_SESSION['err_msg'] != False)
			{
				echo "<p align='center'>".$_SESSION['err_msg']."</p>";
				echo '<p align="center">请重新输入</p>';
			}
			else
				echo '<p align="center">请注册</p>';
			echo'  <form action="train_register.php" method="post">
			  <table border=0 align="center">
			  <tr>
			  <td>用户名</td>
			  <td><input type="text" name="username" pattern="^[\da-zA-Z]{3,10}$" title="请输入3-10位英文或数字" /></td>
			  </tr>
			  <tr>
			  <td>密码</td>
			  <td><input type="password" name="password" pattern="^[\da-zA-Z]{6,18}$" title="请输入6-18位英文或数字" /></td>
			  </tr>
			  <tr>
			  <td>确认密码</td>
			  <td><input type="password" name="password2" pattern="^[\da-zA-Z]{6,18}$" title="请输入与第一次密码相同的密码" /></td>
			  </tr>
			  <tr>
			  <td>邮箱</td>
			  <td><input type="text" name="email" pattern="^[\da-zA-Z]+@[\da-zA-Z]+\.[a-zA-Z]+$" title="请输入用来接收消息的邮箱, 当系统检测到票数变化时， 会第一时间发邮件给您 " /></td>
			  </tr>			  
			  <tr>
			  <td>邀请码</td>
			  <td><input type="text" name="invite_code" title="请给管理员 zp0int@qq.com 发红包获得邀请码" /></td>
			  <tr>
			  </tr></table>
			  <table border=0 align="center"><tr><td><input type="submit" align="center" value="注册" /></td></tr></table>';
	}
	
	function echo_jump()
	{
		echo '<p align="center"><a href="train_login.php">注册成功,<span id="time">4</span> 秒后跳转, 或者点我登陆</a></p>
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
	
	function valid()
	{
		// check username and password
		$username = trim($_POST['username']);
		$password = trim($_POST['password']);
		$password2 = trim($_POST['password2']);
		$invite_code = trim($_POST['invite_code']);
		$email = trim($_POST['email']);
		if ($username === '')
		{
			$_SESSION['err_msg'] = '请输入用户名';
			return False;
		}
		else if ($password === '')
		{
			$_SESSION['err_msg'] = '请输入密码';
			return False;
		}
		else if ($password != $password2)
		{
			$_SESSION['err_msg'] = '两次输入的密码不相同';
			return False;
		}
		else if ($invite_code != "郭大帅" && $invite_code != "美丽的方")
		{
			$_SESSION['err_msg'] = '邀请码不合法, 请给管理员 zp0int@qq.com 发红包获得邀请码';
			return False;
		}
		else if (! preg_match('/^[\da-zA-Z]+@[\da-zA-Z]+\.[a-zA-Z]+$/', $email))
		{
			$_SESSION['err_msg'] = 'email 格式不合法 ';
			return False;
		}
		else if (! preg_match('/^[\da-zA-Z]+$/', $username))
		{
			$_SESSION['err_msg'] = '用户名不合法';
			return False;
		}
		else if (! preg_match('/^[\da-zA-Z]+$/', $password))
		{
			$_SESSION['err_msg'] = '密码不合法';
			return False;
		}
		else if (strlen($username) > 10)
		{
			$_SESSION['err_msg'] = '用户名长度过长';
			return False;
		}
		else if (strlen($username) < 3)
		{
			$_SESSION['err_msg'] = '用户名过短';
			return False;
		}
		else if (strlen($password) > 18)
		{
			$_SESSION['err_msg'] = '密码长度过长';
			return False;
		}
		else if (strlen($password) < 6)
		{
			$_SESSION['err_msg'] = '密码长度过短';
			return False;
		}
		
		return True;
	}
	if (isset($_POST['verify_code']) and isset($_SESSION['err_msg']))
	{
		$_SESSION['err_msg'] = False; // make sure not be modified
		if (trim($_POST['verify_code']) != $_SESSION['verify_code'])
			$_SESSION['err_msg'] = '验证码不符,请重新注册';
		else
		{
			$db = db_connect('site');
			$query = "insert into train (username, password, email, invite_code, modify_time, login_time, max_url) values ('".$_SESSION['username']."','".$_SESSION['password']."', '".$_SESSION['email']."', '".$_SESSION['invite_code']."', NOW(), NOW(), 3);";
			$result = $db->query($query);
			if (! $result)
				$_SESSION['err_msg'] = "注册失败, 服务器错误"; // bad query
		}
		if ($_SESSION['err_msg'] == False)
			echo_jump();
		else
			register_echo();
	}
	else if (!isset($_SESSION['err_msg']) || !isset($_POST['username']) || !isset($_POST['password']) || !isset($_POST['password2']) || !isset($_POST['email']))
	{
		register_echo();
		$_SESSION['err_msg'] = False;
	}
	else
	{
		$username = trim($_POST['username']);
		$password = trim($_POST['password']);
		$invite_code = trim($_POST['invite_code']);
		$db = db_connect('site');
		$query = 'select count(*) from train where invite_code = "'.$invite_code.'";';
		$result = $db->query($query);
		$row = $result->fetch_assoc();
		if (valid())
		{
				$query = 'select username from train where username = "'.$username.'";';
				$result = $db->query($query);
				$row = $result->fetch_assoc();
				
				$query = 'select email from train where email = "'.$_POST['email'].'";';
				$result = $db->query($query);
				$row2 = $result->fetch_assoc();
				if ($row != NULL)
				{
					$_SESSION['err_msg'] = "该用户已被注册";
				}
				else if ($row2 != NULL)
				{
					$_SESSION['err_msg'] = "该邮箱已被注册";
				}
				else
				{
					// verify email tomail!!!!subject
					$url = 'http://localhost/wsgi/email/'.trim($_POST['email']).'!!!!车次系统验证邮箱';
					$result = file_get_contents($url);
					if (strlen($result) != 4)
						$_SESSION['err_msg'] = $result;
					else
					{
						$_SESSION['err_msg'] = False;
						$_SESSION['username'] = $username;
						$_SESSION['password'] = $password;
						$_SESSION['invite_code'] = $invite_code;
						$_SESSION['email'] = trim($_POST['email']);
						$_SESSION['verify_code'] = $result;
						echo '<p align="center">系统已向您的邮箱 '.$_SESSION['email'].' 发了一封验证邮件, 请输入验证邮件的验证码完整注册</p>
							<p align="center">验证过程请勿关闭此页面, 否则需重新注册</p>
							<form action="train_register.php" method="post"><table border=0 align="center"><tr><td><input type="text" align="center" name="verify_code" pattern="[0-9]{4}" title="请输入邮件中收到的数字验证码" /><input type="submit" align="center" value="提交" /></td></tr></table></form>';
					}
				}
		}
		if ($_SESSION['err_msg'] != False)
			register_echo();
	}
?>
</body>
</html>