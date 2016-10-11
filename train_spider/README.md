##A web-based system to help people buy train tickets automatically
####Idea：
1. make the **login**, **register** and **mainpulate page**, users can save their  wish list to **MySQL** database in the **mainpulate page**.
2. python scripts **train_spider.py** runs in server's background will keep refreshing users's wish list, get the tickets' imformation via the selling page.
3. Whenever the scripts detects that the remaining seats of the train in user's wish list meet the user's requirment, the script **recognizing verification code** and **buy your tickets** automatically.

####recognizing verification code:
1. run **`python3 asyncio_getjpg.py`**  to get an amount of verification code in jpg format.
2. run **`python3 cut_and_recognize.py`** to **cut the picture**, It will change the image to string format with  [image_to_string(TESSERACT-OCR)](https://github.com/zpoint/Python/blob/master/image_to_string.py).
3. Use **Imagehash** module to generate fingerprint for each cut image, classify all fingerprints into types generated in **step2**, store them in database.
4. Whenever the script need to recognize verification code, it cut the code image, generate fingerprint for each small image. For each fingerprint, calculate the [Hamming_distance](http://https://en.wikipedia.org/wiki/Hamming_distance) of it and every type in database. The shortest distance is the type you want.

####However:
The Tesseract-OCR has low precision in Chinese character.
I tried the trainning tool with hundreds of samples, the precison remains the same. So, I remove the **buy your tickets automatically** part.

####Finally:
The **train_spider.py** can do **step1, step2** in **Idea** part

change step 3 to: Email user whenever meet user's requirement

You need to:
1. Replace the **pwd** arguments' default value with your password.
2. **In terminal**

		nohub python3 train_spider.py > tspider.log &

It will keep working until system shutdown, reboot or you send a signal to stop the process.


- - -

#####Screenshots
**contents it will email user**

![image](https://github.com/zpoint/Python/blob/master/train_spider/screenshots/4.png)

**First register in "train_register.php" with invited code “郭大帅”**
 ![image](https://github.com/zpoint/Python/blob/master/train_spider/screenshots/1.png)

**Second log in in "train_login.php"**
![image](https://github.com/zpoint/Python/blob/master/train_spider/screenshots/2.png)

**Third, Add your train in your wish list in the webpage "train.php"**
![image](https://github.com/zpoint/Python/blob/master/train_spider/screenshots/3.png)


