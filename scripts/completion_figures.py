"""Publication figures from locked public aggregates. PNG 300dpi and editable SVG."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image,ImageOps,ImageDraw

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'research_completion';FIG=OUT/'figures'
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.grid':True,'grid.alpha':.18,'svg.fonttype':'none'})
COLORS=['#2563a6','#dc6b30','#1b8b67','#7b61a8','#c74961','#8a8074','#468a96','#c39c2e']
inventory=[]

def load(name):return pd.read_csv(OUT/name)
def save(fig,name,title,source,note):
    fig.suptitle(title,x=.02,ha='left',fontsize=13,fontweight='bold')
    fig.text(.02,.018,note,fontsize=7,color='#444444',va='bottom',wrap=True)
    fig.tight_layout(rect=(.01,.09,.99,.94));FIG.mkdir(exist_ok=True)
    for ext in ['png','svg']:
        p=FIG/f'{name}.{ext}';fig.savefig(p,dpi=300,facecolor='white')
        if ext=='svg':p.write_text('\n'.join(line.rstrip() for line in p.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig);inventory.append(dict(figure=name,title=title,source=source,note=note,status='GENERATED'))

def main():
    f=load('data/inclusion_exclusion_flow.csv');wide=f.pivot(index='qidx',columns='state',values='count').fillna(0)
    fig,ax=plt.subplots(figsize=(11,4.8));bottom=np.zeros(len(wide));x=np.arange(len(wide))
    for j,c in enumerate(wide):ax.bar(x,wide[c],bottom=bottom,label=c.replace('_',' '),color=COLORS[j%len(COLORS)]);bottom+=wide[c].to_numpy()
    labels=f.drop_duplicates('qidx').set_index('qidx').loc[wide.index,'origin_quarter']
    ax.set_xticks(x[::4],labels.iloc[::4]);ax.set_ylabel('Initially cheap quote records');ax.legend(fontsize=7,ncol=2,loc='upper left')
    save(fig,'figure_01_quote_flow','1. Exact-quarter quote flow and observation uncertainty','data/inclusion_exclusion_flow.csv',f'All {int(f["count"].sum()):,} initially cheap origin quotes, including right censoring. Missing service is not market exit. Source: World Bank RPW.')
    p=load('data/cohort_by_wave.csv');x=p.qidx-p.qidx.min()
    fig,axs=plt.subplots(2,1,figsize=(10,6),sharex=True)
    axs[0].bar(x,p.n_quotes,color=COLORS[0]);axs[0].set_ylabel('Surveyed quote records')
    axs[1].plot(x,p.n_corridors,label='corridors');axs[1].plot(x,p.n_providers,label='normalised providers');axs[1].set_ylabel('Distinct labels');axs[1].legend()
    axs[1].set_xticks(x.iloc[::4],p.quarter.iloc[::4])
    missing=2025*4+1-p.qidx.min()
    for ax in axs:ax.axvline(missing,color=COLORS[1],linestyle='--',label='2025Q2 absent')
    save(fig,'figure_02_coverage','2. Survey coverage and composition across 37 observed waves','data/cohort_by_wave.csv','Post-2016 sheet; 2025Q2 absent, not zero coverage measured. Provider counts describe survey labels, not market concentration or transaction shares.')
    b=load('tables/table_03_persistence_bounds.csv');x=b.qidx-b.qidx.min()
    fig,ax=plt.subplots(figsize=(10,4.5));ax.fill_between(x,b.lower_bound,b.upper_bound,color=COLORS[0],alpha=.18,label='E2 extreme bounds')
    ax.plot(x,b.conditional_p_stay_core,color=COLORS[0],label='E1 conditional stay')
    ax.fill_between(x,b.ci95_lo,b.ci95_hi,color=COLORS[2],alpha=.35,label='E1 corridor bootstrap 95%')
    ax.set(ylim=(0,1.03),ylabel='Probability of cost staying at or below 3%');ax.set_xticks(x.iloc[::4],b.origin_quarter.iloc[::4]);ax.legend(fontsize=8)
    save(fig,'figure_03_bounds','3. Conditional continuity and partially identified population bounds','tables/table_03_persistence_bounds.csv','Origin-quarter cohorts; exact next-calendar-quarter outcome. Bounds allocate unknown successors to all fail/all stay. E1 intervals: 300 corridor draws per wave; no release-time claim.')
    t=load('tables/supplementary_cost_transitions.csv');m=load('tables/supplementary_threshold_margin.csv')
    t=t.iloc[np.argsort([float(v.split(',')[0].lstrip('([')) for v in t.delta_band])]
    m=m.iloc[np.argsort([float(v.split(',')[0].lstrip('([')) for v in m.margin_band])]
    fig,axs=plt.subplots(1,2,figsize=(11,4.7));axs[0].barh(t.delta_band,t.n,color=COLORS[0]);axs[0].set_xlabel('Valid matched quote pairs');axs[0].set_title('Next cost minus origin cost (pp)')
    axs[1].barh(m.margin_band,m.stay_rate,color=COLORS[2]);axs[1].set(xlim=(0,1),xlabel='Conditional stay probability');axs[1].set_title('Distance below 3% at origin (pp)')
    save(fig,'figure_04_cost_transitions','4. Cost movement and threshold proximity','tables/supplementary_cost_transitions.csv; supplementary_threshold_margin.csv','USD200, initially cheap, valid reobserved pairs only; cost-band endpoints in percentage points. Threshold crossing can be sensitive to rounding.')
    c=load('models/absolute_brier_ci.csv');mc=load('models/model_comparison.csv')
    fig,axs=plt.subplots(1,2,figsize=(13,6.8))
    for ax,analysis in zip(axs,['legacy','phase2']):
        d=c[(c.analysis==analysis)&(c.resampling=='corridor')].sort_values('brier')
        yy=np.arange(len(d));ax.errorbar(d.brier,yy,xerr=[d.brier-d.ci95_lo,d.ci95_hi-d.brier],fmt='o',color=COLORS[0],capsize=2)
        ax.set_yticks(yy,d.model,fontsize=7);ax.invert_yaxis();ax.set_xlabel('Brier; lower is better');ax.set_title('Legacy full training' if analysis=='legacy' else 'Phase2 temporal selection/calibration')
    save(fig,'figure_05_models','5. Conventional and ML probability comparisons','models/absolute_brier_ci.csv',f'Retrospective previously inspected test records. 95% corridor-bootstrap intervals, 1,000 draws. Phase2 reserves six chronological quarters for tuning/calibration/selection; training differs from legacy.')
    r=load('models/calibration.csv');fig,ax=plt.subplots(figsize=(7,5))
    selected=['B2_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest','S_selected']
    for j,n in enumerate(selected):
        d=r[r.model==n];ax.plot(d.mean_pred,d.obs_rate,'-o',label=n,color=COLORS[j],markersize=3);ax.scatter(d.mean_pred,d.obs_rate,s=d.n/120,alpha=.4,color=COLORS[j])
    ax.plot([0,1],[0,1],'--',color='gray');ax.set(xlim=(0,1),ylim=(0,1),xlabel='Predicted stay probability',ylabel='Observed stay fraction');ax.legend(fontsize=7,loc='upper left')
    save(fig,'figure_06_calibration','6. Reliability on retrospective outer test records','models/calibration.csv','Decile bins; marker area reflects sample size. S_selected uses calibrators fitted on earlier, separate quarters. These curves describe test performance, not calibration training.')
    c=load('models/decision_capacity.csv');fig,axs=plt.subplots(1,2,figsize=(11,4.7))
    names=['R_highest_cost_rule','B2_history','B4_recent_history','L2_spline_logistic','M1_hist_gbm','M2_random_forest','S_selected']
    for j,n in enumerate(names):
        d=c[(c.analysis=='phase2')&(c.rule==n)].sort_values('capacity')
        axs[0].plot(d.capacity*100,d.recall,'-o',label=n,color=COLORS[j],markersize=3)
        axs[1].plot(d.capacity*100,d.false_alerts,'-o',label=n,color=COLORS[j],markersize=3)
    axs[0].set(ylabel='Observed failures captured (fraction)',xlabel='Review capacity within quarter (%)');axs[1].set(ylabel='Reviews of quotes that stay cheap',xlabel='Review capacity within quarter (%)');axs[0].legend(fontsize=6)
    save(fig,'figure_07_review_capacity','7. Conditional matched-sample analyst review benchmark','models/decision_capacity.csv','Queue membership conditions on future reobservation; not operational. See figure14 for all-origin budgets and unknown outcomes. No intervention benefit measured.')
    s=load('models/subgroups.csv');s=s[(s.analysis=='phase2')&(s.model=='S_selected')&s.group.isin(['SSA','EAC','Uganda'])]
    fig,axs=plt.subplots(1,2,figsize=(9,4.2));axs[0].barh(s.group,s.failures,color=[COLORS[0] if v else '#aaaaaa' for v in s.supported]);axs[0].axvline(100,color='gray',linestyle='--');axs[0].set_xlabel('Observed threshold failures; gate=100')
    d=s[s.supported];axs[1].barh(d.group,d.brier,color=COLORS[2]);axs[1].set_xlabel('Selected-policy Brier (supported groups)')
    save(fig,'figure_08_subgroup_support','8. African subgroup support and limitations','models/subgroups.csv','Global models applied to retrospective subgroup records; no Uganda-specific score when fewer than100 failures. Subgroup comparison is not external validation.')
    s=load('models/sensitivity_grid.csv');fig,ax=plt.subplots(figsize=(10,7));y=np.arange(len(s));ax.hlines(y,s.lower_bound,s.upper_bound,color=COLORS[0],alpha=.5,lw=4);ax.scatter(s.conditional_p_stay_core,y,color=COLORS[1],s=25,label='Conditional E1')
    ax.set_yticks(y,s.scenario,fontsize=8);ax.set(xlim=(0,1),xlabel='Stay probability; line = E2 bounds');ax.invert_yaxis();ax.legend(fontsize=8)
    save(fig,'figure_09_identity_selection','9. Identity, threshold, basket and attrition sensitivities','models/sensitivity_grid.csv','Each scenario names its own population/threshold. Reduced metadata can create false merges; no new links are promoted. All comparisons are exploratory.')
    d=pd.concat([load('models/paired_dependence.csv'),load('models/joint_dependence_sensitivity.csv')]);d=d[((d.analysis=='legacy')&(d.model_a=='M2_random_forest')&(d.model_b=='L2_spline_logistic'))|((d.analysis=='phase2')&(d.model_a=='S_selected')&(d.model_b=='L2_spline_logistic'))]
    fig,ax=plt.subplots(figsize=(13,6));yy=np.arange(len(d));ax.errorbar(d.brier_diff,yy,xerr=[d.brier_diff-d.ci95_lo,d.ci95_hi-d.brier_diff],fmt='o',capsize=3,color=COLORS[0]);ax.axvline(0,color='gray',linestyle='--');ax.set_yticks(yy,d.analysis.map({'legacy':'Legacy RF','phase2':'Selected policy'})+' / '+d.resampling,fontsize=8);ax.set_xlabel('Paired Brier difference versus spline; negative favours candidate')
    save(fig,'figure_10_dependence','10. Dependence-aware uncertainty sensitivity','models/paired_dependence.csv; models/joint_dependence_sensitivity.csv','Nominal 95% intervals, 1,000 draws; 13 waves. Joint method is post hoc exploratory, stress coverage 0.86. Selected-policy interval crosses zero; no universal coverage claim.')
    d=load('models/permutation_importance.csv');g=d.groupby(['model','feature_group']).mean_brier_increase.mean().unstack('model');fig,ax=plt.subplots(figsize=(10,5));g.plot.barh(ax=ax,color=COLORS[:len(g.columns)]);ax.set_xlabel('Mean increase in test Brier after grouped permutation');ax.set_ylabel('');ax.legend(fontsize=7)
    save(fig,'figure_11_associations','11. Associative feature-group diagnostics across 2024 quarters','models/permutation_importance.csv','Three permutations per feature group per quarter; selected calibrators fixed. Correlated features and off-manifold combinations limit interpretation; no causal effects.')
    gates=load('assessment/publication_gates.csv');counts=gates.status.value_counts();fig,ax=plt.subplots(figsize=(8,4));ax.bar(counts.index,counts.values,color=[COLORS[2] if x=='PASS' else COLORS[1] if x=='FAIL' else '#888888' for x in counts.index]);ax.set(ylabel='Scientific gates',ylim=(0,12));ax.set_title('Conditional research report; no operational model')
    save(fig,'figure_12_supported_scope','12. Evidence gates determine the supported study scope','assessment/publication_gates.csv','Counts are an evidence inventory, not a publication probability or readiness percentage. See the gate ledger for the distinct consequences of each unresolved gate.')
    c=load('models/absolute_brier_ci.csv');c=c[(c.resampling=='corridor')&c.model.isin(['B2_history','L1_ridge_logistic','L2_spline_logistic','M1_hist_gbm','M2_random_forest'])];g=c.pivot(index='model',columns='analysis',values='brier');fig,ax=plt.subplots(figsize=(9,4.5));g.plot.barh(ax=ax,color=[COLORS[0],COLORS[1]]);ax.set_xlabel('Brier; lower is better');ax.set_ylabel('')
    save(fig,'figure_13_legacy_phase2','13. Legacy versus phase2 (20 October 2026)','models/absolute_brier_ci.csv','Same retrospective outer years; phase2 reserves chronological tuning/calibration/selection data, so this is not a pure algorithm substitution or untouched replication.')
    a=load('models/all_origin_capacity_bounds.csv');fig,ax=plt.subplots(figsize=(10,5))
    for j,(name,d) in enumerate(a.groupby('rule',sort=False)):
        d=d.sort_values('capacity');ax.plot(d.capacity*100,d.recall_of_known_failures,'-o',color=COLORS[j],label=name,markersize=3)
        ax.fill_between(d.capacity*100,d.all_failure_recall_lower,d.all_failure_recall_upper,color=COLORS[j],alpha=.13)
    ax.set(xlabel='Review capacity within quarter (%)',ylabel='Failure recall',ylim=(0,1));ax.legend(fontsize=7,loc='upper left')
    save(fig,'figure_14_all_origin_capacity','14. All-origin review budgets preserve unknown outcomes','models/all_origin_capacity_bounds.csv','24,556 eligible origins; 4,889 unknown outcomes. Lines: recall of known failures; bands: extreme all-failure recall bounds, not CIs. E1-score extrapolation scenario.')
    y=load('models/performance_by_year.csv');names=['B0_always_stay','B1_prevalence','B2_history','B3_cost_logistic','L1_ridge_logistic','L2_spline_logistic','M1_hist_gbm','M2_random_forest','S_selected']
    fig,axs=plt.subplots(2,2,figsize=(12,8),sharex=True)
    for row,analysis in enumerate(['legacy','phase2']):
        for j,name in enumerate(names):
            d=y[(y.analysis==analysis)&(y.model==name)].sort_values('target_year')
            if d.empty:continue
            for col,metric in enumerate(['brier','log_loss']):axs[row,col].plot(d.target_year,d[metric],marker='o',label=name,color=COLORS[j%len(COLORS)],markersize=3,linestyle='--' if j==8 else '-')
        axs[row,0].set_ylabel(analysis+' Brier');axs[row,1].set_ylabel(analysis+' log loss');axs[row,0].legend(fontsize=6,ncol=2)
    for ax in axs.flat:ax.set_xticks(sorted(y.target_year.unique()))
    save(fig,'figure_15_yearly_models','15. Annual probability scores preserve negative and changing results','models/performance_by_year.csv','All original families; selected policy only in phase2. B0 log loss is large by construction. 2025 includes Q1 only. All years previously inspected, no independent confirmation.')
    s=load('models/transfer_sensitivity_metrics.csv');s=s[(s.scope=='pooled')&(s.scenario=='lag_1')]
    base=load('models/absolute_brier_ci.csv');base=base[(base.analysis=='legacy')&(base.resampling=='corridor')&base.model.isin(s.model)]
    g=pd.concat([base[['model','brier']].assign(history_scenario='lag 0'),s[['model','brier']].assign(history_scenario='lag 1')]).pivot(index='model',columns='history_scenario',values='brier')
    fig,ax=plt.subplots(figsize=(9,4.5));g.plot.barh(ax=ax,color=COLORS[:2]);ax.set(xlabel='Brier',ylabel='')
    save(fig,'figure_16_history_timing','16. History lag sensitivity is not public release validation','models/absolute_brier_ci.csv; models/transfer_sensitivity_metrics.csv','Fixed full-training references on matched retrospective records. Current origin quotes are used in both; lag 1 changes historical features only. Verified positive public lead time: not established.')
    pd.DataFrame(inventory).to_csv(FIG/'figure_inventory.csv',index=False)
    sheets=[]
    for r in inventory:
        im=Image.open(FIG/(r['figure']+'.png')).convert('RGB');im.thumbnail((600,370))
        tile=Image.new('RGB',(620,410),'white');tile.paste(im,((620-im.width)//2,20));ImageDraw.Draw(tile).text((10,390),r['figure'],fill='black');sheets.append(tile)
    contact=Image.new('RGB',(620*3,410*int(np.ceil(len(sheets)/3))),'#dddddd')
    for i,im in enumerate(sheets):contact.paste(im,((i%3)*620,(i//3)*410))
    contact.save(OUT/'private_runtime/figure_contact_sheet.png')
    print('Generated',len(inventory),'scientific figures, each PNG300dpi + SVG')

if __name__=='__main__':main()
