import unittest
from lib.lists.extended_modifiers_list import ExtendedModifiersList
from lib.lists.modifiers_list import ModifiersList
from lib.dummy_modifiers import DummyBlenderModifier, DummyBlenderObj

print('ClustersList v1.0')


class ModifiersListTests(unittest.TestCase):
    def setUp(self):
        self.o = DummyBlenderObj()
        mods = []
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))

        self.m_list = ModifiersList()
        self.m_list._modifiers_list = mods

    def teatDown(self):
        del(self.o)
        del(self.m_list)

    def test_get_last(self):
        self.assertEqual(self.m_list.get_last(), self.o.modifiers[-1])

    def test_get_first(self):
        self.assertEqual(self.m_list.get_first(), self.o.modifiers[0])

    def test_modifier_get_name(self):
        self.assertEqual(self.m_list.modifier_get_name(
            self.m_list.get_first()), self.o.modifiers[0].name)

    def test_modifier_get_type(self):
        self.assertEqual(self.m_list.modifier_get_type(
            self.m_list.get_first()), self.o.modifiers[0].type)

    def test_get_list_in_range_inclusive(self):
        mod1 = self.m_list.get_first()
        mod2 = self.m_list.get_last()
        self.assertEqual(self.m_list.get_list_in_range_inclusive(
            mod1, mod2), self.m_list._modifiers_list)

    def test_get_list_in_range_not_inclusive(self):
        mod1 = self.m_list.get_first()
        mod2 = self.m_list.get_last()
        self.assertEqual(self.m_list.get_list_in_range_not_inclusive(
            mod1, mod2), self.m_list._modifiers_list[1:2])


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
