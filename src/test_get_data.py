import main


def test():
    try:
        print("test start")
        TEST = main.Initialize()
        return 0
    except:
        return 1

test()
