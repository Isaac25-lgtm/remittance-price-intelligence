"""Fetch public reading copies and timing evidence once; no paywall circumvention."""
from pathlib import Path
import json
import re
import sys
import urllib.parse
from completion_fetch import fetch

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=ROOT/'research_completion/private_runtime/literature'
SOURCES={
 'imf2022.pdf':'https://www.imf.org/-/media/files/publications/wp/2022/english/wpiea2022063-print-pdf.pdf',
 'beck2011.pdf':'https://documents1.worldbank.org/curated/en/651781468133101391/pdf/WPS5072.pdf',
 'rpw2025q3.pdf':'https://remittanceprices.worldbank.org/sites/default/files/2026-04/RPW_main_report_and_annex_Q325.pdf',
 'rpw2025q1.pdf':'https://remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q125_1_0.pdf',
 'rpw2024q4.pdf':'https://remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q424_13.pdf',
 'borra2026.html':'https://www.svedbergopen.com/index.php/ijaiml/article/view/2926/1837',
 'borra2026.pdf':'https://www.svedbergopen.com/index.php/ijaiml/article/download/2926/1837/6504',
 'rpw2025q3_catalogue.pdf':'https://datacatalogfiles.worldbank.org/ddh-published/0037898/DR0095413/RPW_main_report_and_annex_Q325.pdf',
 'archive_reports.json':'https://web.archive.org/cdx/search/cdx?url=remittanceprices.worldbank.org/sites/default/files/*report*annex*&output=json&filter=statuscode:200&fl=timestamp,original,digest&collapse=urlkey&filter=mimetype:application/pdf',
 'wayback.json':'https://web.archive.org/cdx/search/cdx?url=remittanceprices.worldbank.org/sites/default/files/rpw_main_report_and_annex_q424_13.pdf&output=json&filter=statuscode:200&fl=timestamp,original,digest&collapse=digest',
 'crossref.json':'https://api.crossref.org/works?query.title=remittance%20prices%20worldwide%20service%20persistence&rows=15',
 'openalex.json':'https://api.openalex.org/works?search=remittance%20prices%20worldwide%20service%20persistence&per-page=15',
 'semantic_scholar.json':'https://api.semanticscholar.org/graph/v1/paper/search?query=remittance%20prices%20worldwide&limit=10&fields=title,year,url,abstract',
}

if __name__=='__main__':
    PRIVATE.mkdir(parents=True,exist_ok=True)
    selected=sys.argv[1:] or list(SOURCES)
    blocked_hosts=set()
    for name in selected:
        host=urllib.parse.urlsplit(SOURCES[name]).netloc
        if host in blocked_hosts:
            print('SKIPPED_HOST_BLOCKED',name); continue
        dest=PRIVATE/name
        if dest.exists():
            print('CACHED',name); continue
        result=fetch(SOURCES[name],dest)
        if result.get('http_status') in (401,403):
            blocked_hosts.add(host)
        if name.endswith('.pdf') and dest.exists() and dest.read_bytes()[:4]==b'%PDF':
            import fitz
            doc=fitz.open(dest)
            text='\n'.join(f'\n--- PDF PAGE {i+1} ---\n'+p.get_text() for i,p in enumerate(doc))
            dest.with_suffix('.txt').write_text(text,encoding='utf-8')
            dest.with_suffix('.metadata.json').write_text(json.dumps(dict(pages=len(doc),metadata=doc.metadata),indent=2),encoding='utf-8')
