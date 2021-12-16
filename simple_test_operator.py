#! python
from lib.lists import ExtendedModifiersList
from lib.dummy_modifiers import DummyBlenderModifier
from lib.dummy_modifiers import DummyBlenderObj
import unittest

print('ClustersList v1.0')


class ModifiersListTests(unittest.TestCase):
    def test_get_first(self):
        mods = []
        for x in range(5):
            mods.append(DummyBlenderModifier)

        o = DummyBlenderObj(mods)
        a = ExtendedModifiersList()

        a.create_modifiers_list(o)

        self.assertEqual(a.get_first(), o.modifiers[0])


if __name__ == '__main__':
    unittest.main()
