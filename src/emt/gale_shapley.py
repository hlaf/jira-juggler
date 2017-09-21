import copy
from collections import defaultdict
import heapq

def prefers(pref_list, first, second):
    return pref_list.index(first) < pref_list.index(second)

def reject(student, student_prefs, unmatched_students):
    if len(student_prefs[student]) > 0:
        unmatched_students.add(student)
 
def deferred_acceptance(student_prefs, program_prefs, program_slots=None):
    
    if program_slots is None:
        program_slots = defaultdict(lambda: 1)
    
    students = sorted(student_prefs.keys())
    unmatched_students = set(students)
    matchings = defaultdict(list)
    student_options = copy.deepcopy(student_prefs)
    while unmatched_students:
        student = unmatched_students.pop()
        #print("%s is on the market" % (student))
        program = student_options[student].pop(0)
        
        if student not in program_prefs[program]:
            # The program has not ranked the applicant
            reject(student, student_options, unmatched_students)
            continue
        
        #print("  %s (program's #%s) is checking out %s (student's #%s)" % (student, (program_prefs[program].index(student)+1), program, (student_prefs[student].index(program)+1)) )
        student_rank = program_prefs[program].index(student)
        if len(matchings[program]) < program_slots[program]: # The program is free
            heapq.heappush(matchings[program], (-student_rank, student))
            #print("    There's a spot! Now matched: %s and %s" % (student.upper(), program.upper()))
            continue
        
        # The student applies to a full program
        weakest_match = matchings[program][0][1]
        if prefers(program_prefs[program], student, weakest_match):
            # Program prefers new student
            heapq.heappop(matchings[program])
            heapq.heappush(matchings[program], (-student_rank, student))
            reject(weakest_match, student_options, unmatched_students)
        else: # The program prefers the existing match
            reject(student, student_options, unmatched_students)
            
    for k in matchings.keys():
        matchings[k] = [e[1] for e in matchings[k]]
    
    return matchings
