import unittest
import numpy as np

class TestGaleShapley(unittest.TestCase):

    def _buildIncidenceMatrix(self, row_keys, col_keys, matches):
        
        row_keys = sorted(row_keys)
        col_keys = sorted(col_keys)
        matrix = np.zeros((len(row_keys), len(col_keys)))
        for i, k in enumerate(row_keys):
            for col_key in matches[k]:
                j = col_keys.index(col_key)
                matrix[i][j] = 1
        
        return matrix
            
    def test_gale_shapley_example1(self):
        '''
        Example 1 from Gale & Shapley's "College Admissions and the Stability
        of Marriage" article.
        '''
        
        men_prefs = { 'alpha': ['a', 'b', 'c'],
                      'beta':  ['b', 'c', 'a'], 
                      'gamma': ['c', 'a', 'b'],
                    }
        
        women_prefs = { 'a': ['beta', 'gamma', 'alpha'],
                        'b': ['gamma', 'alpha', 'beta'],
                        'c': ['alpha', 'beta', 'gamma'],
                      }

        expected_men_optimal_assignment = {
            'alpha': ['a'],
            'beta' : ['b'], 
            'gamma': ['c'],
        }
        
        expected_women_optimal_assignment = {
            'a': ['beta'],
            'b': ['gamma'], 
            'c': ['alpha'],
        }
        
        from emt.gale_shapley import deferred_acceptance

        # Compute the men-optimal assignment        
        actual_assignment = deferred_acceptance(men_prefs, women_prefs)
    
        m1 = self._buildIncidenceMatrix(men_prefs.keys(),
                                        women_prefs.keys(),
                                        expected_men_optimal_assignment)
        m2 = self._buildIncidenceMatrix(women_prefs.keys(),
                                        men_prefs.keys(),
                                        actual_assignment)
        assert np.array_equal(m1, np.transpose(m2))
    
        # Compute the women-optimal assignment
        actual_assignment = deferred_acceptance(women_prefs, men_prefs)
    
        m1 = self._buildIncidenceMatrix(women_prefs.keys(),
                                        men_prefs.keys(),
                                        expected_women_optimal_assignment)
        m2 = self._buildIncidenceMatrix(men_prefs.keys(),
                                        women_prefs.keys(),
                                        actual_assignment)
        assert np.array_equal(m1, np.transpose(m2))
    
    def test_gale_shapley_example2(self):
        '''
        Example 2 from Gale & Shapley's "College Admissions and the Stability
        of Marriage" article.
        '''
        
        men_prefs = {
            'alpha': ['a', 'b', 'c', 'd'], 
            'beta' : ['a', 'd', 'c', 'b'], 
            'gamma': ['b', 'a', 'c', 'd'], 
            'delta': ['d', 'b', 'c', 'a'], 
        }
        
        women_prefs = {
            'a': ['delta', 'gamma', 'alpha', 'beta'],
            'b': ['beta',  'delta', 'alpha', 'gamma'],
            'c': ['delta', 'alpha', 'beta',  'gamma'],
            'd': ['gamma', 'beta',  'alpha', 'delta'],
        }

        expected_assignment = {
            'alpha': ['c'],
            'beta' : ['d'], 
            'gamma': ['a'],
            'delta': ['b'],
        }

        from emt.gale_shapley import deferred_acceptance
        
        # Compute the assignments
        actual_assignment = deferred_acceptance(men_prefs, women_prefs)
    
        m1 = self._buildIncidenceMatrix(men_prefs.keys(),
                                        women_prefs.keys(),
                                        expected_assignment)
        m2 = self._buildIncidenceMatrix(women_prefs.keys(),
                                        men_prefs.keys(),
                                        actual_assignment)
        assert np.array_equal(m1, np.transpose(m2))
        
        # Verify that the women-optimal solution is the same as the
        # men-optimal one
        actual_assignment = deferred_acceptance(women_prefs, men_prefs)
        m2 = self._buildIncidenceMatrix(men_prefs.keys(),
                                        women_prefs.keys(),
                                        actual_assignment)
        assert np.array_equal(m1, m2)
        
    def test_nrmp_matching_algorithm(self):
        '''
        This test is based on the example presented in the National Resident
        Matching Program (NRMP) explainer video available at:
            http://www.nrmp.org/matching-algorithm/
        '''
        
        applicant_prefs = {
            'arthur' : ['city'],
            'sunny'  : ['city', 'mercy'],
            'joseph' : ['city', 'general', 'mercy'],
            'latha'  : ['mercy', 'city', 'general'],
            'darrius': ['city', 'mercy', 'general'],
        }
        
        program_prefs = {
            'mercy'  : ['darrius', 'joseph'],
            'city'   : ['darrius', 'arthur', 'sunny', 'latha', 'joseph'],
            'general': ['darrius', 'arthur', 'joseph', 'latha'],
        }
        
        program_slots = {
            'mercy'  : 2,
            'city'   : 2,
            'general': 2,
        }

        expected_assignment = {
            'arthur' : ['city'],
            'sunny'  : [],
            'joseph' : ['general'],
            'latha'  : ['general'],
            'darrius': ['city'],
        }

        from emt.gale_shapley import deferred_acceptance

        actual_assignment = deferred_acceptance(applicant_prefs,
                                                program_prefs,
                                                program_slots)

        m1 = self._buildIncidenceMatrix(applicant_prefs.keys(),
                                        program_prefs.keys(),
                                        expected_assignment)
        
        m2 = self._buildIncidenceMatrix(program_prefs.keys(),
                                        applicant_prefs.keys(),
                                        actual_assignment)

        assert np.array_equal(m1, np.transpose(m2))
