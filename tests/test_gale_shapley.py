import unittest

class TestGaleShapley(unittest.TestCase):

    def test_gale_shapley_example1(self):
        '''
        Example 1 from Gale & Shapley's "College Admissions and the Stability
        of Marriage" article.
        '''
        
        from matchfuncs import DA
        import numpy as np
        
        men   = ['alpha', 'beta', 'gamma']
        women = ['a', 'b', 'c']
        
        men_prefs = np.array([
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1],
        ])

        women_prefs = np.array([
            [1, 2, 0],
            [2, 0, 1],
            [0, 1, 2],
        ])

        prop_prefs = { 'alpha': ['a', 'b', 'c'],
                       'beta': ['b', 'c', 'a'], 
                       'gamma': ['c', 'a', 'b'],
                     }
        
        resp_prefs = { 'a': ['beta', 'gamma', 'alpha'],
                       'b': ['gamma', 'alpha', 'beta'],
                       'c': ['alpha', 'beta', 'gamma'],
                     }

        # Compute the men-optimal assignment        
        men_optimal_assignment = np.array([0, 1, 2])

        res = DA(men_prefs, women_prefs)
        assert np.array_equal(res[0], men_optimal_assignment)
        
        # Compute the women-optimal assignment        
        women_optimal_assignment = np.array([1, 2, 0])

        res = DA(women_prefs, men_prefs)
        assert np.array_equal(res[0], women_optimal_assignment)
    
    def test_gale_shapley_example2(self):
        '''
        Example 2 from Gale & Shapley's "College Admissions and the Stability
        of Marriage" article.
        '''
        
        from matchfuncs import DA
        import numpy as np
        
        men_prefs = np.array([
            [0, 1, 2, 3],
            [0, 3, 2, 1],
            [1, 0, 2, 3],
            [3, 1, 2, 0],
        ])

        women_prefs = np.array([
            [3, 2, 0, 1],
            [1, 3, 0, 2],
            [3, 0, 1, 2],
            [2, 1, 0, 3],
        ])

        expected_assignment = np.array([2, 3, 0, 1])

        # Compute the assignments
        men_matches = DA(men_prefs, women_prefs)[0]
        assert np.array_equal(men_matches, expected_assignment)
        
        # Verify that the women-optimal solution is the same as the
        # men-optimal one
        men_matches2 = DA(women_prefs, men_prefs)[1]
        assert np.array_equal(men_matches2, men_matches)
        
    def test_nrmp_matching_algorithm(self):
        '''
        This test is based on the example presented in the National Resident
        Matching Program (NRMP) explainer video available at
            http://www.nrmp.org/matching-algorithm/
        '''
        pass
