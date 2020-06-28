import re
import sys

def calculate_max_length(reg):
    parsed = re.sre_parse.parse(reg)
    return MaxLengthCalculator(reg).calculate()

class MaxLengthCalculator:
    def __init__(self, reg, max_repeat=10):
        self._cache = {}
        self._max_repeat = max_repeat
        self._parsed = re.sre_parse.parse(reg)

    def calculate(self):
        self._cache.clear()
        return self._calculate(self._parsed)

    def _calculate(self, parsed):
        ret = 0
        for opcode, value in parsed:
            #print(opcode, value)
            opstr = str(opcode)
            if opstr == 'LITERAL':
                ret += self._calculate_literal(value)
            elif opstr == 'NOT_LITERAL':
                ret += self._calculate_not_literal(value)
            elif opstr == 'AT':
                ret += self._calculate_at(value)
            elif opstr == 'IN':
                ret += self._calculate_in(value)
            elif opstr == 'ANY':
                ret += self._calculate_any(value)
            elif opstr == 'BRANCH':
                ret += self._calculate_branch(value)
            elif opstr == 'SUBPATTERN':
                ret += self._calculate_group(value)
            elif opstr == 'MAX_REPEAT':
                ret += self._calculate_repeat(value)
            elif opstr == 'MIN_REPEAT':
                ret += self._calculate_repeat(value)
            elif opstr == 'GROUPREF':
                ret += self._calculate_groupref(value)
            else:
                print(f'unimplemented: {opcode}')
        return ret

    def _calculate_literal(self, value):
        return 1

    def _calculate_not_literal(self, value):
        return 1

    def _calculate_repeat(self, value):
        min_repeat, max_repeat, parsed = value
        if str(max_repeat) == 'MAXREPEAT':
            max_repeat = self._max_repeat
        return self._calculate(parsed) * max_repeat

    def _calculate_in(self, value):
        return 1

    def _calculate_at(self, value):
        return 0

    def _calculate_any(self, value):
        return 1

    def _calculate_branch(self, value):
        return max(self._calculate(v) for v in value[1])

    def _calculate_group(self, value):
        pattern_idx = 1 if sys.version_info < (3,6) else 3
        ret = self._calculate(value[pattern_idx])
        if value[0]:
            self._cache[value[0]] = ret
        return ret

    def _calculate_groupref(self, group):
        return self._cache[group]

if __name__ == '__main__':
    print(calculate_max_length(r'a'))
    print(calculate_max_length(r'ab+'))
    print(calculate_max_length(r'a{1,2}'))
    print(calculate_max_length(r'a{,2}'))
    print(calculate_max_length(r'(ab)+'))
    print(calculate_max_length(r'(a|b)+'))
    print(calculate_max_length(r'(aa|b)+'))
    print(calculate_max_length(r'[^a]+'))
    print(calculate_max_length(r'^a$'))
    print(calculate_max_length(r'..+'))
    print(calculate_max_length(r'(\s+)+'))
    print(calculate_max_length(r'(ab)\1+'))
