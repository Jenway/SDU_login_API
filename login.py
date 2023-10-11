# 导入requests库
import httpx
import xml.dom.minidom
import getpass

# 定义baseURL变量
# baseURL = "https://pass.sdu.edu.cn/"

# 定义username和password变量
# username = ""
# password = ""
def login(username, password, baseURL="https://pass.sdu.edu.cn/") -> str:
# 发送第一个请求，获取ticket
    ticket = httpx.post(
        f"{baseURL}cas/restlet/tickets",
        data={"username": username, "password": password, "lt": "LT-1-1-1"},
    ).text
    # print("ticket: " + ticket)
    # 检查ticket是否以TGT开头
    if not ticket.startswith("TGT"):
        raise Exception("ticket should start with TGT. Check your username and password.")

    # 发送第二个请求，获取sTicket
    sTicket = httpx.post(f"{baseURL}cas/restlet/tickets/{ticket}",content="service=https://service.sdu.edu.cn/tp_up/view?m=up", headers={"Content-Type": "text/plain"}).text
    # print("sTicket: " + sTicket)
    # 检查sTicket是否以ST开头
    if not sTicket.startswith("ST"):
        raise Exception("sTicket should start with ST")

    return sTicket
def get_user_name_and_id(sTicket, baseURL="https://pass.sdu.edu.cn/"):
    user_data = xml.dom.minidom.parseString(httpx.get(
        f"{baseURL}cas/serviceValidate",
        params={
            "ticket": sTicket,
            "service": "https://service.sdu.edu.cn/tp_up/view?m=up",
        },
    ).text)
    name = user_data.getElementsByTagName("cas:USER_NAME")[0].childNodes[0].data
    student_id = user_data.getElementsByTagName("sso:user")[0].childNodes[0].data
    return name, student_id


if __name__ == "__main__":
    username = input("请输入学号：")
    password = getpass.getpass("请输入密码：")
    try:
        name, student_id = get_user_name_and_id(login(username, password))
    except Exception as e:
        print("登录失败，可能是密码错误")
        print(e)
        exit(1)
    print(f"姓名：{name}")
    print(f"学号：{student_id}")

