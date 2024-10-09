import unittest


def inverseDict(d: dict) -> dict:
    result = {}
    for key, value in d.items():
        result[value] = (*result.get(value, ()), key)

    # now we have to unwrap all the singletons (tuples of length 1)
    for key in filter(lambda key: len(result[key]) == 1, result.keys()):
        result[key] = result[key][0]

    return result


class Tests(unittest.TestCase):
    def testBasic(self):
        d = {
            "abc": 1,
            'b': 2,
            (3): 1,
            4: 3,
            ('a', 'b'): 1,
        }
        self.assertEqual(
            {
                1: ("abc", (3), ('a', 'b')),
                2: 'b',
                3: 4,
            },
            inverseDict(d)
        )

    def testUnhashableValues(self):
        d = {
            "abc": 1,
            'b': [0, 2],
            (3): 1,
            4: {3},
            ('a', 'b'): 1,
        }

        got_exception = False
        try:
            inverseDict(d)
        except TypeError:
            got_exception = True

        self.assertTrue(
            got_exception, "Should get `TypeError` for non-hashable values")


if __name__ == "__main__":
    unittest.main()
