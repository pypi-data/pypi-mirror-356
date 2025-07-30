# import unittest
# import numpy as np
# import pandas as pd
# import missensemble_class_dev
# import sys
# sys.path.append('..')#
#
# class TestMissensemble(unittest.TestCase):
#    def test_no_nas_end(self):
#        data_pre = pd.DataFrame({'X1': [1, np.nan, 3, 10, 12, 15],
#                                 'X2': [-1, 5, 2, 9, np.nan, 15]})
#        missensemble = missensemble_class_dev.MissEnsemble(n_iter = 100, numerical_vars = ['X1', 'X2'])
#        data_post = missensemble.fit_transform(data_pre)
#        if data_post.convergence_:
#            self.assertTrue(not data_post.isna().values.any())#
#
# if __name__ == '__main__':
#    unittest.main()
