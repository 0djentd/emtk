#! python
import unittest
from lib.lists import ExtendedModifiersList, ModifiersList
from lib.dummy_modifiers import DummyBlenderModifier, DummyBlenderObj

print('ClustersList v1.0')


class ModifiersListTests(unittest.TestCase):
    def test_get_last(self):
        o = DummyBlenderObj()
        mods = []
        mods.append(o.modifier_add('Bevel', 'BEVEL'))
        mods.append(o.modifier_add('Bevel', 'BEVEL'))
        mods.append(o.modifier_add('Bevel', 'BEVEL'))

        m = ModifiersList()
        m._modifiers_list = mods

        self.assertEqual(m.get_last(), o.modifiers[-1])

    def test_get_first(self):
        o = DummyBlenderObj()
        mods = []
        mods.append(o.modifier_add('Bevel', 'BEVEL'))
        mods.append(o.modifier_add('Bevel', 'BEVEL'))
        mods.append(o.modifier_add('Bevel', 'BEVEL'))

        m = ModifiersList()
        m._modifiers_list = mods

        self.assertEqual(m.get_first(), o.modifiers[0])


class ExtendedModifiersListTests(unittest.TestCase):
    def test_create_modifiers_list(self):
        o = DummyBlenderObj()
        mods = []
        mods.append(o.modifier_add('Bevel', 'BEVEL'))
        mods.append(o.modifier_add('Bevel', 'BEVEL'))
        mods.append(o.modifier_add('Bevel', 'BEVEL'))

        m = ExtendedModifiersList()
        result = m.create_modifiers_list(o)

        self.assertNotEqual(result, False)

        # if not self.assertEqual(result, True):
        #     print(f'{m}')


if __name__ == '__main__':
    unittest.main()
