import re


def signUpValidator(email, password, nickname, phone, region):
    if not emailValidator(email):
        return [False, "email", "이메일 형식을 확인해주세요."]
    if not passwordValidator(password):
        return [False, "password", "비밀번호는 8자 이상 16자 이하로 입력해주세요."]
    if not nicknameValidator(nickname):
        return [False, "nickname", "닉네임은 2자 이상 8자 이하로 입력해주세요."]
    if not phoneValidator(phone):
        return [False, "phone", "휴대폰 번호를 확인해주세요."]
    if not regionValidator(region):
        return [False, "region", "지역을 확인해주세요."]

    return [True, None, None]


def nicknameValidator(nickname):
    if not nickname:
        return False
    if len(nickname) < 2 or len(nickname) > 8:
        return False
    return True


def emailValidator(email):
    if not email:
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True


def phoneValidator(phone):
    if not phone:
        return False
    if not re.match(r"01[016789][1-9]\d{7}", phone):
        return False
    return True


def passwordValidator(password):
    if not password:
        return False
    if len(password) < 8 or len(password) > 16:
        return False
    return True


def regionValidator(region):
    if not region:
        return False
    if len(region) < 2 or len(region) > 8:
        return False
    return True
