from base64 import encodestring
from pkg_resources import resource_stream
from itertools import product

import numpy as np
from IPython.core.display import HTML

from probability import WeightedBox, RandomVariable

height, width = 120, 120
host_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
             (height, 
              width,
              encodestring(resource_stream('stats_lectures', \
                           'data/host.png').read()).decode('ascii')))

student_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s"/>' % 
                (height,
                 width,
                 encodestring(resource_stream('stats_lectures', \
                              'data/user-student.png').read()).decode('ascii')))

student_win_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s"/>' % 
                    (height,
                     width,
                     encodestring(resource_stream('stats_lectures', \
                                  'data/student_win.png').read()).decode('ascii')))

student_lose_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s"/>' % 
                     (height,
                      width,
                      encodestring(resource_stream('stats_lectures', \
                                  'data/student_lose.png').read()).decode('ascii')))

car_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s"/>' % 
            (height,
             width,
             encodestring(resource_stream('stats_lectures', \
                          'data/310px-Car_with_Driver-Silhouette.svg.png' \
                                         ).read()).decode('ascii')))

def monty_hall_table(car_pos, student_pos, host_pos, final_pos=None,
                     ndoors=3):

    def make_row(label, img, pos, ndoors):
        row = '<tr><td width="%d"><h2 align="center">%s</h2></td>' % (width, label) 
        if pos >= ndoors:
            raise ValueError('invalid position')

        for i in range(pos):
            row += '<td height="%d" width="%d"></td>' % (height, width)
        row += '<td height="%d" width="%d">%s</td>' % (height, width, img)
        for i in range(ndoors-1-pos):
            row += '<td height="%d" width="%d"></td>' % (height, width)
        row += '</tr>\n'
        return row

    if final_pos is not None:
        if car_pos == final_pos:
            final_row = make_row('Final', student_win_html, final_pos, ndoors)
        else:
            final_row = make_row('Final', student_lose_html, final_pos, ndoors)
    else:
        final_row = ''
    table = '\n'.join(['<table>',
                       make_row('Prize', car_html, car_pos, ndoors),
                       make_row('Contestant', student_html, student_pos, ndoors),
                       make_row('Host', host_html, host_pos, ndoors),
                       final_row,
                       '</table>'])
    return table

class monty_hall_noswitch(WeightedBox):

    """
    The no-switching strategy as default
    """

    def __init__(self, ndoors=3):
        self.ndoors = ndoors
        def prob(prize, student, host, final):
            if prize == student:
                return 1./(self.ndoors**2) * 1. / (self.ndoors - 1)
            else:
                return 1./(self.ndoors**2) * 1. / (self.ndoors - 2)

        _sample_space = []
        for (prize, student, host) in product(range(1,self.ndoors+1),
                                              range(1,self.ndoors+1),
                                              range(1,self.ndoors+1)): 
            if host not in [prize, student]:
                _sample_space.append((prize, student, host, student))
        WeightedBox.__init__(self, dict([(v, prob(*v)) for v in
                                         _sample_space]))

    def trial(self):
        WeightedBox.trial(self)
        self.car, self.student, self.host, self.final = np.array(self.outcome)-1
        return self.outcome

    def conditional(self, event_spec):
        mass_fn = WeightedBox.conditional(self, event_spec).mass_function
        return conditional_noswitch(mass_fn)

    @property
    def success(self):
        if not hasattr(self, "_event"):
            self._event = RandomVariable(self, lambda outcome: outcome[0] == outcome[3])
        return self._event

    def _repr_html_(self):
        if self.outcome is None:
            base = monty_hall_table(1, 
                                    1,
                                    2,
                                    None,
                                    ndoors=self.ndoors)
        else:
            base = monty_hall_table(self.car, 
                                    self.student,
                                    self.host,
                                    self.final,
                                    ndoors=self.ndoors)
        return base


class monty_hall_switch(monty_hall_noswitch):

    """
    The no-switching strategy as default
    """


    def __init__(self, ndoors=3):
        self.ndoors = ndoors
        def prob(prize, student, host, final):
            if prize == student:
                return 1./(self.ndoors**2) * 1. / ((self.ndoors - 1) * (self.ndoors - 2))
            else:
                return 1./(self.ndoors**2) * 1. / ((self.ndoors - 2) * (self.ndoors - 2))

        _sample_space = []
        for (prize, student, host) in product(range(1,self.ndoors+1),
                                              range(1,self.ndoors+1),
                                              range(1,self.ndoors+1)): 
            if host not in [prize, student]:
                possible_values = set(range(1, self.ndoors+1)).difference( \
                    [host, student])
                for final in possible_values:
                    _sample_space.append((prize, student, host, final))
        WeightedBox.__init__(self, dict([(v, prob(*v)) for v in
                                         _sample_space]))

    def conditional(self, event_spec):
        mass_fn = WeightedBox.conditional(self, event_spec).mass_function
        return conditional_switch(mass_fn)


class conditional_switch(monty_hall_switch):
    
    """
    We draw samples until initial student guess does not match the car.
    """

    def __init__(self, mass_function):
        WeightedBox.__init__(self, mass_function)

class conditional_noswitch(monty_hall_noswitch):
    
    """
    We draw samples until initial student guess does not match the car.
    """

    def __init__(self, mass_function):
        WeightedBox.__init__(self, mass_function)

no_switch = monty_hall_noswitch()
switch = monty_hall_switch()
        
examples = {'switch':switch,
            'noswitch':no_switch,
            'switch_match':switch.conditional(lambda o: o[0] == o[1]),
            'switch_nomatch':switch.conditional(lambda o: o[0] != o[1]),
            'no_switch_match':no_switch.conditional(lambda o: o[0] == o[1]),
            'no_switch_nomatch':no_switch.conditional(lambda o: o[0] != o[1])}
