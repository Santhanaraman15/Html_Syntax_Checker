MAX_TAG_CHARS = 10
MIN_TAG_CHARS = 1

def convert_and_strip(tag):
    tag_array = list(tag)
    del(tag_array[0])
    del(tag_array[-1])
    return tag_array

def is_ending_tag(tag_array):
    if len(tag_array) > 0 and tag_array[0] == '/':
        return True
    else:
        return False

def check_tag(tag):
    tag_array = convert_and_strip(tag)
    if (is_ending_tag(tag_array)):
        del(tag_array[0])
    if len(tag_array) > MAX_TAG_CHARS or len(tag_array) < MIN_TAG_CHARS:
        return 'INVALID_NO_OF_CHARS'
    for char in tag_array:
        if char >= 'A' and char <= 'Z':
            continue
        else:
            return 'BAD_CHAR'
    return 'SUCCESS'


class HTMLChecker(object):
    def __init__(self):
        self.__return_val = ''
        self.stack = []
        self.errors = {'BAD_CHAR' : 'bad character in tag name',
                        'INVALID_NO_OF_CHARS' : 'too many/few characters in tag name',
                        'EXPECTED_END_OF_TAG' : 'expected </xxxx>',
                        'UNEXPECTED_TAG' : 'no matching begin tag.',
                        'SUCCESS' : 'OK'}
    def handle_tag(self,tag):
        tag_array = convert_and_strip(tag)
        result = 'SUCCESS'
        if not is_ending_tag(tag_array):
            self.push_tag(tag)
        else:
            result = self.validate_ending_tag(tag)
        return result
    def push_tag(self, tag):
        self.stack.append(tag)
    def validate_ending_tag(self,tag):
        if len(self.stack) == 0:
            return 'UNEXPECTED_TAG'
        top_of_stack = self.stack.pop()
        if top_of_stack != tag[0]+tag[2::]:
            self.__return_val = top_of_stack[0]+'/'+top_of_stack[1::]
            self.errors['EXPECTED_END_OF_TAG'] = 'expected '+self.__return_val
            return 'EXPECTED_END_OF_TAG'
        else:
            return 'SUCCESS'



if __name__ == '__main__':
    test_case_no = 1
    NL = raw_input()
    NL = int(NL)
    results = []
    results.append("Test Case "+str(test_case_no))
    checker = HTMLChecker()
    err_flag = False
    for line_no in xrange(1,NL+1):
        line = raw_input()
        tag_flag = False
        tag_array = []
        for char in line:
            if char == '<' or tag_flag:
                tag_array.append(char)
                tag_flag = True
                if char == '>':
                    tag_flag = False
                    tag = ''.join(tag_array)
                    tag_array = []
                    result = check_tag(tag)
                    if result == 'SUCCESS':
                        result = checker.handle_tag(tag)
                        if result != 'SUCCESS':
                            results.append("line "+str(line_no)+": "+checker.errors[result])
                            err_flag = True
                            break
                    else:
                        results.append("line "+str(line_no)+": "+checker.errors[result])
                        err_flag = True
                        break
            else:
                continue
        # If a tag is not cloed by end of line
        if tag_flag:
            results.append("line "+str(line_no)+": "+checker.errors['BAD_CHAR'])
            err_flag = True
    if len(checker.stack) != 0 and not err_flag:
        err_flag = True
        top_of_stack = checker.stack.pop()
        checker.__return_val = top_of_stack[0]+'/'+top_of_stack[1::]
        checker.errors['EXPECTED_END_OF_TAG'] = 'expected '+checker.__return_val
        results.append("line "+str(line_no-1)+": "+ checker.errors['EXPECTED_END_OF_TAG'])
    if not err_flag:
        results.append("OK")
    results.append("")
    for result in results:
        print result
