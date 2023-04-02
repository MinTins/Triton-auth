import requests
from bs4 import BeautifulSoup


def triton_auth(login, password) -> ("info", "session-cookies"):

    with requests.Session() as session:
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        response = session.post("http://student.triton.knu.ua/", data={"ReturnUrl": "/"})

        soup = BeautifulSoup(response.content, 'html.parser')
        token_input = soup.find('input', {'name': '__RequestVerificationToken'})
        token_value = token_input['value']

        response = session.post("https://student.triton.knu.ua/", data={"Login": login, "Password": password, "__RequestVerificationToken": token_value, "RememberMe": "true"})

        if response.history and response.history[0].status_code == 302:
            response = session.get("https://student.triton.knu.ua/Settings")
            soup = BeautifulSoup(response.content, "html.parser")
            element = soup.select_one("body > div > div > div:nth-child(1) > div.col-sm-9")

            username = element.select_one("p:nth-of-type(1)").get_text().split(":")[1].strip()
            fullname = element.select_one("p:nth-of-type(2)").get_text().split(":")[1].strip()
            email = element.select_one("p:nth-of-type(3)").get_text().split(":")[1].strip()
            faculty = element.select_one("p:nth-of-type(4)").get_text().split(":")[1].strip()
            course = element.select_one("p:nth-of-type(5)").get_text().split(":")[1].strip()
            group = element.select_one("p:nth-of-type(6)").get_text().split(":")[1].strip()
            role = element.select_one("p:nth-of-type(7)").get_text().split(":")[1].strip()

            data = {
                "username": username,
                "fullname": fullname,
                "email": email,
                "faculty": faculty,
                "course": course,
                "group": group,
                "role": role
            }

            cookies = session.cookies.get_dict()

            return data, cookies