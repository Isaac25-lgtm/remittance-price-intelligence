import pandas as pd
from tests.conftest import make_clean
from rpi import linkage as L

def test_ordered_corridor_cannot_match_reverse_direction():
    d=make_clean([dict(year=2024,qtr=1,source_code='AAA',destination_code='BBB',**{'cc1 total cost %':1}),dict(year=2024,qtr=2,source_code='BBB',destination_code='AAA',**{'cc1 total cost %':1})])
    a=L.link_next_quarter(L.service_table(d))
    assert not a.iloc[0].core_reobserved
    assert a.iloc[0].status=='corridor_not_surveyed_next_quarter'

def test_baskets_remain_distinct_when_both_are_linked():
    d=make_clean([dict(year=2024,qtr=q,**{'cc1 total cost %':float(q),'cc2 total cost %':float(q)/10}) for q in [1,2]])
    s=pd.concat([L.service_table(d,'cc1'),L.service_table(d,'cc2')],ignore_index=True)
    a=L.link_next_quarter(s);origin=a[a.qtr==1].set_index('basket')
    assert origin.loc['cc1','cost_next']==2
    assert origin.loc['cc2','cost_next']==.2
