from base64 import encodestring
from pkg_resources import resource_stream
from itertools import product

import numpy as np
from IPython.core.display import HTML

from examples import WeightedBox, RandomVariable

height, width = 120, 120
host_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
             (height, 
              width,
              encodestring(resource_stream('stats_lectures', \
                           'data/host.png').read()).decode('ascii')))

student_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
                (height,
                 width,
                 encodestring(resource_stream('stats_lectures', \
                              'data/user-student.png').read()).decode('ascii')))

student_win_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
                    (height,
                     width,
                     encodestring(resource_stream('stats_lectures', \
                                  'data/student_win.png').read()).decode('ascii')))

student_lose_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
                     (height,
                      width,
                      encodestring(resource_stream('stats_lectures', \
                                  'data/student_lose.png').read()).decode('ascii')))

car_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
            (height,
             width,
             encodestring(resource_stream('stats_lectures', \
                          'data/310px-Car_with_Driver-Silhouette.svg.png' \
                                         ).read()).decode('ascii')))

def monty_hall_table(car_pos, student_pos, host_pos, final_pos=None):

    def make_row(label, img, pos):
        row = (('<tr><td width="%d"><h2 align="center">%s</h2></td>' % (width, label)) + 
               ('<td height="%d" width="%d"></td>' % (height, width)) * pos
               + ('<td height="%d" width="%d">%s</td>' % (height, width, img))
               + ('<td height="%d" width="%d"></td>' % (height, width)) * (2-pos) + '</tr>')
        return row

    if final_pos is not None:
        if car_pos == final_pos:
            final_row = make_row('Final', student_win_html, final_pos)
        else:
            final_row = make_row('Final', student_lose_html, final_pos)
    else:
        final_row = ''
    table = '\n'.join(['<table>',
                       make_row('Prize', car_html, car_pos),
                       make_row('Contestant', student_html, student_pos),
                       make_row('Host', host_html, host_pos),
                       final_row,
                       '</table>'])
    return table

class monty_hall_example(WeightedBox):

    """
    The no-switching strategy as default
    """

    def __init__(self, rule = lambda student, host: student):
        self.rule = rule

        def prob(prize, student, host):
            if prize == student:
                return 1/18.
            else:
                return 1/9.

        self._sample_space =  \
            [(prize, student, host, 
              self.rule(student-1, host-1)+1) 
             for prize, student, host in product(range(1,4),
                                                 range(1,4),
                                                 range(1,4))
             if host not in [prize, student]]        

        probs = np.array([prob(*v[:3]) for v in self._sample_space])
        probs /= probs.sum()
        WeightedBox.__init__(self, dict([(v, p) for v, p in zip(self._sample_space, probs)]))

    def trial(self):
        WeightedBox.trial(self)
        self.car, self.student, self.host, self.final = np.array(self.outcome)-1

    def conditional(self, event_spec):
        mass_fn = WeightedBox.conditional(self, event_spec).mass_function
        return conditional_monty_hall(mass_fn)

    @property
    def event(self):
        if not hasattr(self, "_event"):
            self._event = RandomVariable(self, lambda outcome: outcome[0] == outcome[3])
        return self._event

    def _repr_html_(self):
        if self.outcome is None:
            base = monty_hall_table(1, 
                                    1,
                                    2,
                                    None)
        else:
            base = monty_hall_table(self.car, 
                                    self.student,
                                    self.host,
                                    self.final)
        return base

class conditional_monty_hall(monty_hall_example):
    
    """
    We draw samples until initial student guess does not match the car.
    """

    def __init__(self, mass_function):
        WeightedBox.__init__(self, mass_function)

no_switch = monty_hall_example()

def switch_rule(student, host):
    return list(set(range(3)).difference([student, host]))[0]
switch = monty_hall_example(rule=switch_rule)

        
examples = {'switch':switch,
            'noswitch':no_switch}
# ,
#             'switch_match':conditional_scenario(True, True),
#             'switch_nomatch':conditional_scenario(True, False),
#             'noswitch_nomatch':conditional_scenario(False, False),
#             'noswitch_match':conditional_scenario(False, True)}
