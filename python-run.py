from GraphEngine.tsl.type.factory import *
from GraphEngine.DotNet.setup import init_trinity_service, build_module, Env
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        init_trinity_service()
        print('json cons addr: ', Env.ffi._json_cons_fn_ptr_getter())
        self.tsl = TSL()

    def test_definitions(self):
        self.assertTrue(hasattr(Env, 'ffi'), 'Import `ffi` module failed.')

        tsl = self.tsl

        @tsl
        class S(Struct):
            i: int
            s: str

        @tsl
        class C(Cell):
            i: int
            s: S
            ls: List[S]

        @tsl
        class LS(List[S]):
            pass

        tsl.bind()
        print('json cons addr: ', Env.ffi._json_cons_fn_ptr_getter())
        self.assertIn('Jit_SwigGen', Env.ffi.__dict__,
                      'Build tsl module failed, no `Jit_SwigGen` found in `ffi` module.')

        c = C()
        c.i = 1

        self.assertEqual(c.i, 1)
        c.s.s = "123"
        self.assertEqual(c.s.s, "123")
        s = S()
        s.s = c.s.s
        s.i = 5
        c.s = s
        self.assertEqual(s.s, "123")
        self.assertEqual(s.i, 5)

        c.ls.append(s)
        fst = c.ls[0]
        self.assertEqual(1, len(c.ls))
        self.assertEqual(fst.s, s.s)
        self.assertEqual(fst.i, s.i)

        ls = c.ls
        s2 = S()
        s2.s = "5656"
        s2.i = 42

        ls.insert(0, s2)

        # here is something different from original python list
        self.assertEqual(fst.s, "5656")
        self.assertEqual(fst.i, 42)
        self.assertEqual(len(ls), 2)
        del ls[0]
        self.assertEqual(fst.s, s.s)
        self.assertEqual(fst.i, s.i)

        s3 = S(dict(i=1, s="555"))
        self.assertEqual(s3.i, 1)
        self.assertEqual(s3.s, "555")


if __name__ == '__main__':
    unittest.main()