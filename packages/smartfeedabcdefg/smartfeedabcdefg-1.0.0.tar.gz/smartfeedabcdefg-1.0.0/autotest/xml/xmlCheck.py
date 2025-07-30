def checkTotle(xmlUrl,expertCouont):
    flag = True
    return (False, {"与期望结果存在差异": expertCouont}) if flag else (True, "校验期望结果包含校验通过")


def main():
    code,message = checkTotle("http://XXXX",20)
    print(code)
    print(message)

if __name__ == '__main__':
    main()
