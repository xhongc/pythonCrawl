def grep(pattern):
    print("Searching for", pattern)
    while True:
        line = (yield)
        if pattern in line:
            print('line:', line)


search = grep('coroutine')
next(search)
# output: Searching for coroutine
search.send("I love you")
search.send("Don't you love me?")
search.send("I love coroutine instead!")
# search.send("coroutine")
# output: I love coroutine instead!
