"""New measurement-focused figures from actual safe aggregate CSVs, 300dpi plus SVG."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from literature import md

OUT=Path(__file__).resolve().parents[1]
BLUE='#1d5c82';ORANGE='#b46618';GREY='#5c6771'

def save(fig,name):
    fig.savefig(OUT/'figures'/f'{name}.png',dpi=300,bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/'figures'/f'{name}.svg',bbox_inches='tight',facecolor='white')
    plt.close(fig)

def main():
    (OUT/'figures').mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','svg.fonttype':'none'})
    d=pd.read_csv(OUT/'identity/LINKAGE_SCENARIO_RESULTS.csv').set_index('scenario')
    fig,ax=plt.subplots(figsize=(8,4.8))
    labels=[]
    for i,(basket,threshold) in enumerate([('cc1',3),('cc1',5),('cc2',3),('cc2',5)]):
        for offset,rule,col in [(-.12,'core',BLUE),(.12,'strict',ORANGE)]:
            r=d.loc[f'{basket}_{threshold}pct_{rule}'];y=i+offset
            ax.plot([r.lower,r.upper],[y,y],lw=5,color=col,alpha=.5,label=rule.capitalize()+' bounds' if i==0 else None)
            ax.scatter(r.conditional,y,s=35,c=col,zorder=3,label=rule.capitalize()+' conditional' if i==0 else None)
        labels.append(f'${200 if basket=="cc1" else 500}; {threshold}% threshold\nn={int(r.n_eligible):,} origins')
    ax.set(yticks=range(4),yticklabels=labels,xlim=(0,1),xlabel='Recorded continuity proportion',title='Similar matched-record points, wider strict bounds')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1));ax.invert_yaxis();ax.legend(loc='lower left',ncol=2,fontsize=8)
    fig.subplots_adjust(bottom=.25)
    fig.text(.12,.02,'Bars: unknown-outcome identification bounds under each rule, not confidence intervals.\nPoints: continuity conditional on valid matches. Separate basket/threshold cohorts.',fontsize=8)
    save(fig,'figure_01_identity_bounds')
    w=pd.read_csv(OUT/'tables/paired_wave_identity.csv');x=w.qidx/4
    fig,axes=plt.subplots(2,1,figsize=(9,6.5),sharex=True)
    full=pd.read_csv(OUT/'tables/wave_measurement.csv')
    for ax,rule,col in zip(axes,['core','strict'],[BLUE,ORANGE]):
        r=full[full.scenario==f'cc1_3pct_{rule}']
        xx=r.qidx/4
        ax.fill_between(xx,r.lower,r.upper,color=col,alpha=.22,label='All-origin bounds')
        ax.plot(xx,r.conditional,color=col,marker='o',ms=3,label='Valid-pair conditional')
        ax.set(ylim=(0,1.02),ylabel='Continuity proportion',title=rule.capitalize()+' identity: USD200, 3%')
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1));ax.legend(loc='lower left',fontsize=8)
    axes[-1].set(xlabel='Origin year (quarterly positions); no bridge across absent 2025Q2')
    fig.tight_layout();save(fig,'figure_02_wave_series')
    fig,ax=plt.subplots(figsize=(8.5,4))
    ax.plot(x,(w.width_strict-w.width_core)*100,color=BLUE,marker='o',ms=4)
    ax.axvline((2022*4+2)/4,color=GREY,ls='--',lw=1,label='2022Q3 sensitivity boundary')
    ax.axhline(0,color=GREY,lw=.8);ax.set(xlabel='Origin year',ylabel='Additional unknown share (percentage points)',title='Identity-related widening varies over calendar waves')
    ax.legend(fontsize=8);fig.tight_layout();save(fig,'figure_03_width_by_wave')
    flow=pd.read_csv(OUT/'tables/unknown_flow.csv');flow=flow[~flow.state.isin(['stay','fail'])].sort_values('count')
    fig,ax=plt.subplots(figsize=(8.5,4.2))
    ax.barh(flow.state.str.replace('_',' '),flow['count'],color=BLUE)
    for i,n in enumerate(flow['count']):ax.text(n+45,i,f'{n:,}',va='center',fontsize=9)
    ax.set(xlabel='Eligible origin records with unknown successors',xlim=(0,max(flow['count'])*1.18),title='Core identity: 8,914 unknown successors, different mechanisms')
    fig.tight_layout();save(fig,'figure_04_unknown_states')
    s=pd.read_csv(OUT/'tables/measurement_sensitivities.csv');fig,ax=plt.subplots(figsize=(8,4.5))
    for offset,rule,col in [(-.15,'core',BLUE),(.15,'strict',ORANGE)]:
        rr=s[(s.scenario==f'cc1_3pct_{rule}')&(s.stratum_field=='weighting')]
        vals=[d.loc[f'cc1_3pct_{rule}','conditional'],rr.iloc[0].conditional,rr.iloc[1].conditional]
        ax.bar(np.arange(3)+offset,vals,width=.3,color=col,label=rule.capitalize())
        for j,v in enumerate(vals):ax.text(j+offset,v+.013,f'{100*v:.1f}%',ha='center',fontsize=9)
    ax.set(xticks=range(3),xticklabels=['Quote-record weighted','Equal corridor','Equal provider label'],ylim=(0,1),ylabel='Mean conditional continuity',title='Weighting changes the scientific target')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1));ax.legend(loc='lower left')
    fig.text(.12,-.025,'Equal-group conditional means omit groups with no valid pair.\nNot survey-weighted or transaction-weighted population estimates.',fontsize=8)
    save(fig,'figure_05_weighting')
    md('manuscript/figure_legends.md','''# Figure legends

1. **Identity bounds.** Actual E1 points and E2 finite-panel identification bounds for each USD200/USD500 basket and3%/5% threshold. Core/strict share origins within each basket/threshold, not across different products. Bars are not confidence intervals. Source: identity/LINKAGE_SCENARIO_RESULTS.csv.
2. **Every eligible-origin wave.** Primary-basket core/strict conditional continuity and all-origin bounds across36 origin waves. One origin has no valid successor pairs; the point is missing there, not zero. There are37 observed source waves and35 valid-pair origin waves. Missing2025Q2 is never bridged; final2025Q3 is right-censored. Source: tables/wave_measurement.csv.
3. **Paired width.** Strict-minus-core unknown fraction for the same origins, in percentage points. All widths are nonnegative mechanically because strict restricts core matches; magnitude and temporal heterogeneity are the substantive observations. Dashed2022Q3 boundary is a fixed sensitivity split, not a causal event estimate. Source: tables/paired_wave_identity.csv.
4. **Unknown mechanisms.** Source-record counts separate ambiguity, unresurveyed corridor, absent key in surveyed corridor and invalid target cost. Missing is not exit or unaffordability. Total8,914 excludes2,083 last-wave right-censored affordable origins. Source: tables/unknown_flow.csv.
5. **Weighting.** Record-weighted versus equally weighted corridor/provider-label conditional means under each identity rule. Equal-group means exclude zero-valid groups; these are different estimands and have sparse-group uncertainty, not identified market averages. Source: tables/measurement_sensitivities.csv and independent_unit_support.csv.

All five new figures are supplied as editable SVG and300dpi PNG with editable source CSVs. The prior Phase2 figure/model package is preserved rather than redrawn. No simulated values appear in these figures.
''')
    print(dict(figures=5,formats=['SVG','PNG300dpi']))

if __name__=='__main__':main()
