import teambition
import func

if __name__ == "__main__":
    cookie_file = "/home/zpoint/Desktop/cookies.txt"
    func.fix_cookie_format(cookie_file, filter_domain=(".teambition.com", ))
    # t = teambition.teambition()
    t.refresh()
