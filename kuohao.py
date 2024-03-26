class valid:
    def __init__(self, input_string):
        self.result = []
        # use stack to store the extra id of '('
        self.stack = []
        self.input_string = input_string

    def isvalid(self):
        for i in range(len(self.input_string)):
            if self.input_string[i] == '(':
                self.stack.append(i)
                self.result.append(" ")
            elif self.input_string[i] == ')':
                if self.stack:
                    self.stack.pop()
                    self.result.append(" ")
                else:
                    self.result.append('?')
            else:
                self.result.append(" ")
        for num in self.stack:
            self.result[num] = 'x'
        print(''.join(self.result))
        return ''.join(self.result)


def test_result():
    user_input = input("请输入一个字符串: ")
    if not user_input:
        raise ValueError("输入字符串不能为空")
    test_input = valid(user_input)
    test_input.isvalid()
    goon = input("是否继续猜测? 请输入y or n > ")
    if goon == 'y':
        test_result()
    else:
        pass


if __name__ == '__main__':
    test_result()
