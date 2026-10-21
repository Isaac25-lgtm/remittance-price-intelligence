"""Versioned evidence assessment; judgements are labelled, access depth is explicit."""
import hashlib
import json
from pathlib import Path
import re
import pandas as pd

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'research_completion/phase3'

def prose_spacing(text):
    pieces=re.split(r'(`[^`]*`|\b[a-f0-9]{32,64}\b|\d{4}-\d{2}-\d{2}T[\d:.+Z-]+|\]\([^)]*\)|https?://\S+|\S*[/\\]\S*)',text)
    for i in range(0,len(pieces),2):
        s=re.sub(r'(?<=[a-z])(?=\d)',' ',pieces[i])
        s=re.sub(r'(?<=\d)(?=[a-zA-Z])',' ',s)
        s=re.sub(r'(\d{4}) Q([1-4])',r'\1Q\2',s)
        s=re.sub(r'(\d) e([-+]\d+)',r'\1e\2',s)
        s=re.sub(r',(?=[A-Za-z])',', ',s)
        s=re.sub(r',(?=\d{1,2}(?:[^\d]|$))',', ',s)
        pieces[i]=s
    return ''.join(pieces)

def md(name,text):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    if p.suffix=='.md':text=prose_spacing(text)
    p.write_text(text.strip()+'\n',encoding='utf-8')

def main():
    old=pd.read_csv(ROOT/'research_completion/literature/closest_work_matrix.csv').fillna('')
    old['phase3_review']='Phase2 evidence retained; access depth not upgraded merely from metadata.'
    old.loc[old.citation_id=='beck2022','access_depth']='FULL_TEXT_LOCAL; methods, tables and appendix definitions'
    old.loc[old.citation_id=='beck2022','phase3_review']='Local 37-page PDF recovered, SHA256 11bf3907bb9c303d2b4e8ee7d0c0e57f0fcbe366ef710f924b7e672bad722cc9; pp8,11-14,29-34. Firm-level models already established. No stable longitudinal bundle-ID definition or E1/E2 threshold-transition endpoint established in reviewed methods.'
    old.loc[old.citation_id=='lim2026','phase3_review']='Author-maintained https://singapore.to/research/ssrn-6830281/ checked; only SSRN source link, not full text. SSRN HTTP403. Manuscript date26May2026 versus posted1June2026. Exact service identity and missingness overlap remain unverified.'
    additions=[
        dict(citation_id='nakamura2008',author='Nakamura, Emi; Steinsson, Jon',date='2008',title='Five Facts about Prices: A Reevaluation of Menu Cost Models',doi='10.1162/qjec.2008.123.4.1415',url='https://eml.berkeley.edu/~enakamura/papers/fivefacts.pdf',type='published QJE; author-posted full text',dataset_period_sample='US BLS consumer1988-2005 and producer1998-2005 microdata',unit='item/outlet price quotes',outcome_analysis='price changes, sales, substitutions, durations',access_depth='FULL_TEXT_RELEVANT_METHODS',independent_overlap_critique='Identity, temporary nonobservation and product substitution alter measured price persistence: established conceptual prior art. Not an RPW3% transition estimate.',evidence_locator_limitations='SecII-III; pp1421-1438; not independently replicated',phase3_review='Read author-posted PDF; local reading copy hash in access ledger.'),
        dict(citation_id='nakamura2012',author='Nakamura, Emi; Steinsson, Jon',date='2009 working paper;2012 journal',title='Lost in Transit: Product Replacement Bias and Pricing to Market',doi='10.1257/aer.102.7.3277',url='https://www.nber.org/papers/w15359',type='AER2012; NBER15359 working-paper full text separately read',dataset_period_sample='US import/export product microdata1994-2004; aggregate1982-2007',unit='sampled product-firm price spell',outcome_analysis='replacement bias in matched-model price indexes and exchange-rate pass-through',access_depth='FULL_TEXT_WORKING_PAPER_METHODS; published version abstract',independent_overlap_critique='Closest conceptual head-to-head: matched-item persistence can omit replacement-related changes. R01 has no quality/volume or replacement truth and cannot estimate their structural correction.',evidence_locator_limitations='WP sections1-4, product sampling and replacement model; not identical threshold estimand',phase3_review='Lawful local NBER PDF obtained with ordinary request; web-reader PDF access had403. Distinguish transport endpoint outcomes, no bypass or authenticated access.'),
        dict(citation_id='horowitz1998',author='Horowitz, Joel L; Manski, Charles F',date='1998',title='Censoring of outcomes and regressors due to survey nonresponse: Identification and estimation using weights and imputations',doi='10.1016/S0304-4076(97)00077-8',url='https://www.sciencedirect.com/science/article/pii/S0304407697000778',type='Journal of Econometrics84(1):37-58',dataset_period_sample='methodological missing-data framework',unit='partially observed outcomes/regressors',outcome_analysis='identification bounds under nonresponse',access_depth='PUBLISHER_ABSTRACT',independent_overlap_critique='Worst/best bounds and limits of untestable missingness assumptions are established methods, not new R01 theory.',evidence_locator_limitations='Publisher-indexed abstract; full text not read',phase3_review='No theorem attribution beyond inspected abstract.'),
        dict(citation_id='bersch2021',author='Bersch, Julia; Clevy, Jean Francois; Muhammad, Naseem; Perez Ruiz, Esther; Yakhshilikov, Yorbol',date='2021',title='Fintech Potential for Remittance Transfers: A Central America Perspective',doi='',url='https://www.imf.org/-/media/files/publications/wp/2021/english/wpiea2021175-print-pdf.pdf',type='IMF Working Paper21/175',dataset_period_sample='Central America/LAC remittance industry evidence',unit='firm/route pricing',outcome_analysis='fee drivers, competitor fee elasticity, fintech inclusion',access_depth='FULL_TEXT_INTRO; INDEXED_METHOD_CAVEATS',independent_overlap_critique='Competitor-price sensitivity already studied. Authors specifically note time-varying firm data would be needed to test responses to entrants/price changes. Not demonstrated to contain R01 exact-quarter E1/E2.',evidence_locator_limitations='SecV and AnnexIV identified; full annex could not be re-opened after timeout and eLibrary403; NOT a completed full-annex audit',phase3_review='Retain limited access depth; no novelty exclusion based on unread annex.'),
    ]
    works=pd.concat([old,pd.DataFrame(additions)],ignore_index=True).fillna('')
    works.loc[works.citation_id=='bersch2021',['access_depth','dataset_period_sample','phase3_review','evidence_locator_limitations']]=[
      'FULL_TEXT_METHODS_SEC_V_ANNEX_IV','own collection from operators December2019;31 US-origin routes; RPW regional context',
      'Local52-page PDF recovered, SHA25611b05dbce51493bac61050128292ca1cc3a753a37387d2a9a42f6b9f8e0ad0da. AnnexIV pricing equations and tables inspected; not a longitudinal RPW quote linkage study.',
      'pp18-19,46-52; three operators, two amounts and transfer modes; authors explicitly list lack of time-varying data as a limitation']
    for col in ['quote_service_identity','transition_outcome','denominators','attrition_handling','missingness_identification','publication_clock','validation_design','baseline_models','uncertainty','actionability','substantive_delta']:
        works[col]='NOT_ESTABLISHED_IN_REVIEWED_SOURCE; see access depth'
    specifics={
      'beck2022':['firm/corridor/year; bundle identifier not specified','fee levels, not exact-quarter cheap-to-cheap','unbalanced and balanced corridor samples; covariate complete cases','balanced203-corridor trend; varying regression samples','no E2 bounds established','lags for country/corridor factors; contemporaneous firm factors','explanatory cross-section/pooled/fixed effects','regressions; no comparable E1 forecasting scores','corridor-clustered firm regression SE; robust corridor regression SE','associations, explicitly not causal','service-level work occupied; exact-key threshold and attrition application remains candidate'],
      'borra2026':['provider/channel within corridor/quarter, not validated persistent bundles','digital-versus-agent price levels','5902 distinct service quotes across overlapping samples','survey expansion and provider-composition sensitivities','no E2 bounds established in reviewed full text','survey quarter; no as-of forecasting claim','provider/corridor/quarter fixed effects','six channel definitions and fee/FX comparisons','reported clustered regressions; not a paired E1 predictive benchmark','provider effects distinguish digital composition from channel saving','cannot claim service-level price analysis, decomposition or expansion sensitivity as new'],
      'rpw54':['qualifying surveyed services within corridor','cross-sectional averages and SmaRT','qualifying corridor/service sets;20corridors without qualifying service','current coverage; no matched-service transition estimand','not a missing-successor bound','issue label versus publication/creation/capture differ','official descriptive monitoring','global/weighted/MTO/SmaRT indicators','not a validated E1 confidence interval','corridor affordable choices and access qualification','our continuity does not correct or invalidate the official metric'],
      'plainrelease':['corridor, at least two providers per compared period','latest two available corridor observations; may skip quarters','365 compared corridors in displayed release','requires coverage both periods; no zero fabricated','not service-successor identification','dynamic request-time compilation; no historical full-feature vintages','descriptive release comparison','corridor costs/coverage','no dependence-based E1 inference','coverage and corridor trend reference','same source longitudinal monitoring is occupied; exact bundle target differs'],
      'lim2026':['provider-corridor-quarter per abstract; exact key unread','digital cost/inclusion gradient per abstract','188700 and377 corridors per abstract','UNVERIFIED_FULLTEXT','UNVERIFIED_FULLTEXT','UNVERIFIED_FULLTEXT','fixed effects per abstract; details unread','UNVERIFIED_FULLTEXT','UNVERIFIED_FULLTEXT','abstract inclusion-gradient claim only','major unresolved source overlap; author catalogue has no alternate full text'],
      'nakamura2012':['BLS product-firm sampled price spells','replacement bias and price adjustment','attempted product-month observations and trade weights','product turnover is central','structural replacement model; not R01 unknown-outcome allocation','not an operational forecast clock','empirical/model correction of trade price indexes','conventional matched-item measures','model and sample assumptions; not RPW bootstrap','interpretation of official price-index pass-through','general selection lesson established; domain/threshold application alone may be incremental'],
    }
    columns=['quote_service_identity','transition_outcome','denominators','attrition_handling','missingness_identification','publication_clock','validation_design','baseline_models','uncertainty','actionability','substantive_delta']
    for citation,values in specifics.items():works.loc[works.citation_id==citation,columns]=values
    works.to_csv(OUT/'literature/closest_work_matrix_v3.csv',index=False)
    access=[]
    for _,r in works.iterrows():access.append(dict(citation_id=r.citation_id,url=r.url,access_date='2026-10-21',access_depth=r.access_depth,locator=r.evidence_locator_limitations,status='UNRESOLVED_FULLTEXT' if r.citation_id=='lim2026' else 'DEPTH_EXPLICIT_NOT_ALL_FULLTEXT'))
    for p in (OUT/'private_runtime/sources').glob('*.pdf'):
        with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
        access.append(dict(citation_id=p.stem,url='see source_acquisition.csv or imf_access.json',access_date='2026-10-21',access_depth='PRIVATE_READING_COPY',sha256=h,bytes=p.stat().st_size))
    pd.DataFrame(access).to_csv(OUT/'literature/fulltext_access_ledger.csv',index=False)
    queries=[
      ('web','"The Digital Discount in Cross-Border Remittances" Lim 6830281','SSRN abstract; author catalogue found'),
      ('web','"6830281" Lim remittances full text','no separate accessible full text found'),
      ('author','https://singapore.to/research/ssrn-6830281/','bibliography only; SSRN sole work link'),
      ('RePEc targeted web','site.ideas.repec.org "Digital Discount" remittances','no lawful alternate full text located'),
      ('web','"Boon Chuan Lim" remittances research','author catalogue and SSRN author record'),
      ('web','"remittance" "price persistence" World Bank quotes panel','no exact E1/E2 report established in reviewed hits'),
      ('web','"remittance" "quote" "attrition" study','bounded negative search; not proof of absence'),
      ('web','"remittance" "cheap" "persistence" World Bank paper','bounded negative search; not proof of absence'),
      ('web','"remittance" "threshold" "transition" prices worldwide','no exact same-estimand source established'),
      ('conceptual','Nakamura Steinsson product substitutions missing price quotes','Five Facts and Lost in Transit; existing replacement-bias methods'),
      ('conceptual','Horowitz Manski 1998 censoring outcomes missing data nonparametric bounds','publisher abstract verified; no novel R01 bounding theory'),
      ('IMF cited-work followup','"Bersch" "2021" remittance prices competitors','IMF21/175; annex access incomplete'),
      ('official','site.remittanceprices.worldbank.org "2025Q4" OR "Q4 2025" OR "2026Q1" OR "Q1 2026"','no verified new row vintage'),
      ('official','site.remittanceprices.worldbank.org "2026Q2" OR "2026Q3" OR "Q2 2026" OR "Q3 2026"','no verified new row vintage'),
      ('official','site.datacatalog.worldbank.org "Remittance Prices Worldwide" "2026" dataset','catalogue ends2025; source checksum unchanged'),
      ('journal','site.iospress.com Statistical Journal IAOS scope official statistics','current society page confirms use/production of official statistics scope; publisher now Sage'),
    ]
    pd.DataFrame([dict(date='2026-10-21',portal=a,query=b,result=c) for a,b,c in queries]).to_csv(OUT/'literature/search_log_v3.csv',index=False)
    bibliography=(ROOT/'research_completion/literature/references.bib').read_text(encoding='utf-8')
    bibliography+='\n@article{nakamura2008, author={Nakamura, Emi and Steinsson, Jon}, title={Five Facts about Prices: A Reevaluation of Menu Cost Models}, year={2008}, journal={Quarterly Journal of Economics}, volume={123}, number={4}, pages={1415--1464}, doi={10.1162/qjec.2008.123.4.1415}, url={https://eml.berkeley.edu/~enakamura/papers/fivefacts.pdf}}\n'
    bibliography+='\n@article{nakamura2012, author={Nakamura, Emi and Steinsson, Jon}, title={Lost in Transit: Product Replacement Bias and Pricing to Market}, year={2012}, journal={American Economic Review}, volume={102}, number={7}, pages={3277--3316}, doi={10.1257/aer.102.7.3277}, note={NBER working paper15359 full methods read; journal version not read in full}, url={https://www.nber.org/papers/w15359}}\n'
    bibliography+='\n@article{horowitz1998, author={Horowitz, Joel L. and Manski, Charles F.}, title={Censoring of outcomes and regressors due to survey nonresponse: Identification and estimation using weights and imputations}, year={1998}, journal={Journal of Econometrics}, volume={84}, number={1}, pages={37--58}, doi={10.1016/S0304-4076(97)00077-8}, note={Publisher abstract reviewed}}\n'
    bibliography+='\n@techreport{bersch2021, author={Bersch, Julia and Clevy, Jean Francois and Muhammad, Naseem and Perez Ruiz, Esther and Yakhshilikov, Yorbol}, title={Fintech Potential for Remittance Transfers: A Central America Perspective}, year={2021}, institution={International Monetary Fund}, number={21/175}, url={https://www.imf.org/-/media/files/publications/wp/2021/english/wpiea2021175-print-pdf.pdf}, note={SectionV and AnnexIV methods/tables reviewed; own December2019 operator collection}}\n'
    md('literature/references.bib',bibliography)
    classifications=[
      ('Service-level RPW analysis, channel comparison and fee/FX decomposition','ALREADY_ESTABLISHED','Beck2022;Borra2026;Lim abstract','Different geography/model does not supply novelty.'),
      ('Matched-price selection and substitution matter for persistence','ALREADY_ESTABLISHED','Nakamura2008;Nakamura2012','Different market, but the general conceptual lesson already exists.'),
      ('Worst/best missing-outcome bounds','ALREADY_ESTABLISHED','HorowitzManski1998; standard binary-outcome arithmetic','No new identification method is claimed.'),
      ('RPW exact-adjacent-quarter3% continuity and core/strict unknown-bound contrast','POTENTIALLY_SUBSTANTIAL','independent Phase3 measurement; closest-work matrix','Large interpretive difference; novelty and economic-product validity not externally resolved.'),
      ('Four threshold/basket identity scenarios and equal-group measurement','NEW_BUT_INCREMENTAL','Phase3 independent aggregates','Useful robustness; additional cells do not by themselves establish a substantial paper.'),
      ('Superior deployable AI recheck allocation','UNRESOLVED','Phase2 adverse inference/timing/capacity evidence','Operational branch unsupported. Not salvaged by nominal small p-values or dashboard.'),
    ]
    pd.DataFrame(classifications,columns=['candidate_contribution','classification','evidence','falsifier_or_limit']).to_csv(OUT/'literature/contribution_classification.csv',index=False)
    md('literature/NOVELTY_DECISION.md','''# Novelty decision: CONDITIONAL_HOLD

The strongest surviving title is **Affordable surveyed remittance quotes: identity-sensitive continuity and unknown-successor bounds**. This is a retrospective measurement application, not a new bounding method, first service-level RPW study or prospective AI system. No contribution is SUBSTANTIAL_CONFIRMED.

The exact numerical application appears distinct from the inspected closest methods. Core and strict conditional estimates are nearly identical, while their source-population bounds differ materially. This changes whether an analyst can defend a four-in-five same-record persistence statement. It does not establish the true direction of selection bias: the conditional estimate lies inside both identification sets. The independent Phase3 tables reproduce, rather than newly discover, the main Phase2 contrast. The added period/group/basket contrasts improve interpretation and verification.

Beck, Janfils and Kpodar already use firm-level RPW variation; their pp13-14 and Table9 specify explanatory regressions with contemporaneous product attributes and corridor-clustered errors. Their Appendix defines covariates, not a verified same-bundle continuity panel. Borra and Saritha already use provider fixed effects, service quotes, decomposition and survey-expansion checks. Official SmaRT concerns qualifying corridor choices; PlainRemit compares successive available corridor observations, which may skip quarters. None is a head-to-head predictive benchmark on E1.

The closest conceptual competitor, Nakamura and Steinsson's **Lost in Transit**, shows why identical-item price comparisons can miss replacement-related adjustment. R01 cannot claim that lesson or their structural correction: it has no verified replacement/quality or quantity data. Standard nonresponse bounds also predate this study. Thus a domain application and a new model scoreboard alone would be incremental.

Lim2026 is still ABSTRACT-ONLY/UNVERIFIED OVERLAP. A precise-title/identifier, RePEc-targeted, SSRN-author and author-catalogue search found the author-maintained entry, but it links only to denied SSRN. Its bibliography confirms a preprint, not peer review; it does not clear methods, supplements or overlap. Bersch2021's firm-price annex was recovered locally: it uses the authors' December2019 operator collection and explicitly lacks time-varying firm data. That access blocker is resolved; its endpoint is different. Search logs record the remaining limits; absence of a hit is not proof of originality.

**Concrete answer:** important recorded-key persistence and a large identity/unknown-successor contrast are demonstrated; not-previously-quantified and substantial scientific advance are not demonstrated. Prior corridor monitoring answers a different question and is not shown wrong. A monitoring analyst should report continuity with its conditioning/denominator, not translate a SmaRT or E3 value into a same-service guarantee.

Continue only a bounded external validation/overlap review. A full text reporting the same E1/E2/core-strict contrast, or human evidence that links cannot represent comparable offers, would falsify the proposed paper. If literature and identity checks establish only the already-known matched-panel selection lesson without a consequential new domain result, archive as NO_GO for an original research article. No acceptance probability is supplied.
''')
    print(dict(works=len(works),contributions=len(classifications),verdict='CONDITIONAL_HOLD'))

if __name__=='__main__':main()
