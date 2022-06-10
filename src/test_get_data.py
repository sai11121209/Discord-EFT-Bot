import main


def test():
    try:
        TEST = main.Initialize()
        return 0
    except:
        return 1

test()
