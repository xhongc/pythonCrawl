product_list = [
    ('iphone', 5800),
    ('mac pro', 9800),
    ('bike', 800),
    ('coffee', 31),
    ('yang python', 120)

]
shopping_list = []
salary = input("input you salary:")
if salary.isdigit():
    salary = int(salary)
    while True:
        for index, item in enumerate(product_list):
            # print(product_list.index(item),item) #下标的第一种写法
            print(index, item)
        user_choice = input("选择要买嘛？(输入q 退出购买)>>>:\n").strip()

        if user_choice.isdigit():
            user_choice = int(user_choice)
            if 0 <= user_choice < len(product_list):
                p_item = product_list[user_choice]
                if p_item[1] <= salary:  # 买得起
                    shopping_list.append(p_item)
                    salary -= p_item[1]

                    print("added %s into shopping cart,your current balance is %s" % (p_item, salary))
                else:
                    print('买不起')
                    break
        elif user_choice == 'q':
            break
        else:
            break
