from emt.utils import to_identifier, cv

class TaskJugglerFormatter(object):

    TEMPLATE = '''
task {id} "{key}: {description}" {{
{props}
{subtasks}
}}
'''

    def __init__(self, predicate=lambda x: True):
        self._written = set()
        self._predicate = predicate

    def format(self, task):
        '''
        Convert task object to the task juggler syntax

        Returns:
            str: String representation of the task in juggler syntax
        '''
        
        if task in self._written or not self._predicate(task):
            return ''
        self._written.add(task) 
        print 'Writing', task.key, task.summary 
    
        props = ''
        for prop in task.properties:
            if prop == 'effort' and len(task.children) > 0:
                continue
            
            # Handle completed tasks
            if prop == 'effort' and task.isDone():
                props += 'start ' + cv(task.start) + '\n'
                props += 'end ' + cv(task.end) + '\n'
                continue
            if task.isDone() and prop == 'allocate':
                continue
            if prop == 'allocate' and len(task.children) > 0:
                continue
            props += str(task.properties[prop])

        return self.TEMPLATE.format(id=to_identifier(task.key),
                                    key=task.key,
                                    description=task.summary.replace('\"', '\\\"'),
                                    props=props,
                                    subtasks=''.join([self.format(c) for c in task.children]))
    
    
