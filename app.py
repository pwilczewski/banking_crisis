import gradio as gr
import pandas as pd
import os
import random
import time
import yfinance as yf

largest_banks = ['JPM','BAC','C','WFC','USB','PNC','TFC','GS','COF','BK']
failed_banks = ['SBNY','SIVB']
failed_bank_names = ['Signature Bank', 'SVB Financial Group']
bank_tickers = ['ABCB',	'ACNB',	'AFBI',	'ALRS',	'AMAL',	'AMNB',	'AMTB',	'AROW',	'ASB',	'ASRV',	'ATLO',	'AUB',	'AUBN',	'BAC',	'BANC',	'BANF',	'BANR',	'BCML',	'BCOW',	'BFC',	'BFIN',	'BFST',	'BHB',	'BKSC',	'BLFY',	'BMRC',	'BOH',	'BOKF',	'BOTJ',	'BPOP',	'BPRN',	'BRBS',	'BSRR',	'BSVN',	'BUSE',	'BWB',	'BWFG',	'BY',	'C',	'CAC',	'CADE',	'CALB',	'CARE',	'CASH',	'CATC',	'CATY',	'CBAN',	'CBFV',	'CBNK',	'CBSH',	'CBU',	'CCB',	'CCBG',	'CCNE',	'CFB',	'CFFI',	'CFG',	'CFR',	'CFSB',	'CHCO',	'CHMG',	'CIVB',	'CIZN',	'CLBK',	'CMA',	'CNOB',	'COFS',	'COLB',	'CPF',	'CSTR',	'CTBI',	'CUBI',	'CVBF',	'CVCY',	'CWBC',	'CZFS',	'CZNC',	'EBC',	'EBTC',	'ECBK',	'EFSC',	'EGBN',	'ESQ',	'ESSA',	'EVBN',	'EWBC',	'FBIZ',	'FBK',	'FBMS',	'FBNC',	'FCBC',	'FCCO',	'FCF',	'FCNCA',	'FDBC',	'FFBC',	'FFIC',	'FFIN',	'FFNW',	'FFWM',	'FGBI',	'FHB',	'FHN',	'FIBK',	'FINW',	'FISI',	'FITB',	'FLIC',	'FMBH',	'FMNB',	'FNB',	'FNCB',	'FNLC',	'FNWB',	'FRAF',	'FRBA',	'FRBK',	'FRC',	'FRME',	'FRST',	'FSBC',	'FSBW',	'FSEA',	'FSFG',	'FULT',	'FUNC',	'FUSB',	'FVCB',	'FXNC',	'GABC',	'GBCI',	'GBNY',	'GGAL',	'GLBZ',	'GNTY',	'GSBC',	'HAFC',	'HBAN',	'HBCP',	'HBNC',	'HBT',	'HFWA',	'HIFS',	'HMST',	'HNVR',	'HOMB',	'HONE',	'HOPE',	'HTBK',	'HTH',	'HTLF',	'HVBC',	'HWBK',	'HWC',	'IBCP',	'IBOC',	'IBTX',	'INBK',	'INDB',	'ISTR',	'JMSB',	'JPM',	'KEY',	'LARK',	'LBAI',	'LBC',	'LCNB',	'LKFN',	'LMST',	'LOB',	'MBCN',	'MBIN',	'MBWM',	'MCB',	'MCBC',	'MCBS',	'MGYR',	'MLVF',	'MNSB',	'MOFG',	'MPB',	'MRBK',	'MSBI',	'MSVB',	'MTB',	'MYFW',	'NBHC',	'NBN',	'NBTB',	'NFBK',	'NIC',	'NKSH',	'NSTS',	'NWBI',	'NWFL',	'NYCB',	'OBNK',	'OBT',	'ONB',	'OPBK',	'OPHC',	'OPOF',	'ORRF',	'OSBC',	'OVBC',	'OVLY',	'OZK',	'PACW',	'PB',	'PBBK',	'PBFS',	'PBHC',	'PCB',	'PEBK',	'PEBO',	'PFBC',	'PFIS',	'PGC',	'PKBK',	'PNBK',	'PNC',	'PNFP',	'PPBI',	'PRK',	'PTRS',	'PVBC',	'PWOD',	'QCRH',	'RBB',	'RBCAA',	'RBKB',	'RF',	'RNST',	'RRBI',	'RVSB',	'SASR',	'SBCF',	'SBFG',	'SBSI',	'SFBS',	'SFNC',	'SFST',	'SHBI',	'SHFS',	'SMBC',	'SMBK',	'SMMF',	'SNV',	'SPFI',	'SRCE',	'SSB',	'SSBI',	'SSBK',	'STBA',	'STEL',	'SYBT',	'TBBK',	'TCBC',	'TCBI',	'TCBK',	'TCBS',	'TCBX',	'TCFC',	'TFC',	'TFIN',	'THFF',	'TMP',	'TOWN',	'TRMK',	'TRST',	'TSBK',	'UBCP',	'UBFO',	'UBSI',	'UCBI',	'UMBF',	'UNB',	'UNTY',	'USB',	'USCB',	'UVSP',	'VABK',	'VBFC',	'VBTX',	'VLY',	'WABC',	'WAFD',	'WAL',	'WASH',	'WBS',	'WFC',	'WSBC',	'WSFS',	'WTBA',	'WTFC',	'ZION','GS','COF','BK','STT','MS','ALLY', 'AXP','NTRS','DFS']
bank_names = ['Ameris Bancorp',	'ACNB Corporation',	'Affinity Bancshares Inc.',	'Alerus Financial Corporation',	'Amalgamated Financial Corp.',	'American National Bankshares Inc.',	'Amerant Bancorp Inc.',	'Arrow Financial Corporation',	'Associated Banc-Corp',	'AmeriServ Financial Inc.',	'Ames National Corporation',	'Atlantic Union Bankshares Corporation',	'Auburn National Bancorporation Inc.',	'Bank of America Corporation',	'Banc of California Inc.',	'BancFirst Corporation',	'Banner Corporation',	'BayCom Corp',	'1895 Bancorp of Wisconsin Inc',	'Bank First Corporation',	'BankFinancial Corporation',	'Business First Bancshares Inc.',	'Bar Harbor Bankshares Inc.',	'Bank of South Carolina Corp.',	'Blue Foundry Bancorp',	'Bank of Marin Bancorp',	'Bank of Hawaii Corporation',	'BOK Financial Corporation',	'Bank of the James Financial Group Inc.',	'Popular Inc.',	'Princeton Bancorp Inc.',	'Blue Ridge Bankshares Inc.',	'Sierra Bancorp',	'Bank7 Corp.',	'First Busey Corporation',	'Bridgewater Bancshares Inc.',	'Bankwell Financial Group Inc.',	'Byline Bancorp Inc.',	'Citigroup Inc.',	'Camden National Corporation',	'Cadence Bank',	'California BanCorp',	'Carter Bankshares Inc.',	'Pathward Financial Inc.',	'Cambridge Bancorp',	'Cathay General Bancorp',	'Colony Bankcorp Inc.',	'CB Financial Services Inc.',	'Capital Bancorp Inc.',	'Commerce Bancshares Inc.',	'Community Bank System Inc.',	'Coastal Financial Corporation',	'Capital City Bank Group',	'CNB Financial Corporation',	'CrossFirst Bankshares Inc.',	'C&F Financial Corporation',	'Citizens Financial Group Inc.',	'Cullen/Frost Bankers Inc.',	'CFSB Bancorp Inc.',	'City Holding Company',	'Chemung Financial Corp',	'Civista Bancshares Inc.',	'Citizens Holding Company',	'Columbia Financial Inc.',	'Comerica Incorporated',	'ConnectOne Bancorp Inc.',	'ChoiceOne Financial Services Inc.',	'Columbia Banking System Inc.',	'Central Pacific Financial Corp',	'CapStar Financial Holdings Inc.',	'Community Trust Bancorp Inc.',	'Customers Bancorp Inc',	'CVB Financial Corporation',	'Central Valley Community Bancorp',	'Community West Bancshares',	'Citizens Financial Services Inc.',	'Citizens & Northern Corp',	'Eastern Bankshares Inc.',	'Enterprise Bancorp Inc',	'ECB Bancorp Inc.',	'Enterprise Financial Services Corporation',	'Eagle Bancorp Inc.',	'Esquire Financial Holdings Inc.',	'ESSA Bancorp Inc.',	'Evans Bancorp Inc.',	'East West Bancorp Inc.',	'First Business Financial Services Inc.',	'FB Financial Corporation',	'First Bancshares Inc.',	'First Bancorp',	'First Community Bankshares Inc.',	'First Community Corporation',	'First Commonwealth Financial Corporation',	'First Citizens BancShares Inc.',	'Fidelity D & D Bancorp Inc.',	'First Financial Bancorp.',	'Flushing Financial Corporation',	'First Financial Bankshares Inc.',	'First Financial Northwest Inc.',	'First Foundation Inc.',	'First Guaranty Bancshares Inc.',	'First Hawaiian Inc.',	'First Horizon Corporation',	'First Interstate BancSystem Inc.',	'FinWise Bancorp',	'Financial Institutions Inc.',	'Fifth Third Bancorp',	'First of Long Island Corporation (The)',	'First Mid Bancshares Inc.',	'Farmers National Banc Corp.',	'F.N.B. Corporation',	'FNCB Bancorp Inc.',	'First Bancorp Inc',	'First Northwest Bancorp',	'Franklin Financial Services Corporation',	'First Bank',	'Republic First Bancorp Inc.',	'First Republic Bank',	'First Merchants Corporation',	'Primis Financial Corp.',	'Five Star Bancorp',	'FS Bancorp Inc.',	'First Seacoast Bancorp Inc.',	'First Savings Financial Group Inc.',	'Fulton Financial Corporation',	'First United Corporation',	'First US Bancshares Inc.',	'FVCBankcorp Inc.',	'First National Corporation',	'German American Bancorp Inc.',	'Glacier Bancorp Inc.',	'Generations Bancorp NY Inc.',	'Grupo Financiero Galicia S.A.',	'Glen Burnie Bancorp',	'Guaranty Bancshares Inc.',	'Great Southern Bancorp Inc.',	'Hanmi Financial Corporation',	'Huntington Bancshares Incorporated',	'Home Bancorp Inc.',	'Horizon Bancorp Inc.',	'HBT Financial Inc.',	'Heritage Financial Corporation',	'Hingham Institution for Savings',	'HomeStreet Inc.',	'Hanover Bancorp Inc.',	'Home BancShares Inc.',	'HarborOne Bancorp Inc.',	'Hope Bancorp Inc.',	'Heritage Commerce Corp',	'Hilltop Holdings Inc.',	'Heartland Financial USA Inc.',	'HV Bancorp Inc.',	'Hawthorn Bancshares Inc.',	'Hancock Whitney Corporation',	'Independent Bank Corporation',	'International Bancshares Corporation',	'Independent Bank Group Inc',	'First Internet Bancorp',	'Independent Bank Corp.',	'Investar Holding Corporation',	'John Marshall Bancorp Inc.',	'JP Morgan Chase & Co.',	'KeyCorp',	'Landmark Bancorp Inc.',	'Lakeland Bancorp Inc.',	'Luther Burbank Corporation',	'LCNB Corporation',	'Lakeland Financial Corporation',	'Limestone Bancorp Inc.',	'Live Oak Bancshares Inc.',	'Middlefield Banc Corp.',	'Merchants Bancorp',	'Mercantile Bank Corporation',	'Metropolitan Bank Holding Corp.',	'Macatawa Bank Corporation',	'MetroCity Bankshares Inc.',	'Magyar Bancorp Inc.',	'Malvern Bancorp Inc.',	'MainStreet Bancshares Inc.',	'MidWestOne Financial Gp',	'Mid Penn Bancorp',	'Meridian Corporation',	'Midland States Bancorp Inc.',	'Mid-Southern Bancorp Inc.',	'M&T Bank Corporation',	'First Western Financial Inc.',	'National Bank Holdings Corporation',	'Northeast Bank',	'NBT Bancorp Inc.',	'Northfield Bancorp Inc.',	'Nicolet Bankshares Inc.',	'National Bankshares Inc.',	'NSTS Bancorp Inc.',	'Northwest Bancshares Inc.',	'Norwood Financial Corp.',	'York Community Bancorp Inc.',	'Origin Bancorp Inc.',	'Orange County Bancorp Inc.',	'Old National Bancorp',	'OP Bancorp',	'OptimumBank Holdings Inc.',	'Old Point Financial Corporation',	'Orrstown Financial Services Inc',	'Old Second Bancorp Inc.',	'Ohio Valley Banc Corp.',	'Oak Valley Bancorp',	'Bank OZK',	'PacWest Bancorp',	'Prosperity Bancshares Inc.',	'PB Bankshares Inc.',	'Pioneer Bancorp Inc.',	'Pathfinder Bancorp Inc.',	'PCB Bancorp',	'Peoples Bancorp of North Carolina Inc.',	'Peoples Bancorp Inc.',	'Preferred Bank',	'Peoples Financial Services Corp.',	'Peapack-Gladstone Financial Corporation',	'Parke Bancorp Inc.',	'Patriot National Bancorp Inc.',	'PNC Financial Services Group Inc.',	'Pinnacle Financial Partners Inc.',	'Pacific Premier Bancorp Inc',	'Park National Corporation',	'Partners Bancorp',	'Provident Bancorp Inc.',	'Penns Woods Bancorp Inc.',	'QCR Holdings Inc.',	'RBB Bancorp',	'Republic Bancorp Inc.',	'Rhinebeck Bancorp Inc.',	'Regions Financial Corporation',	'Renasant Corporation',	'Red River Bancshares Inc.',	'Riverview Bancorp Inc',	'Sandy Spring Bancorp Inc.',	'Seacoast Banking Corporation of Florida',	'SB Financial Group Inc.',	'Southside Bancshares Inc.',	'ServisFirst Bancshares Inc.',	'Simmons First National Corporation',	'Southern First Bancshares Inc.',	'Shore Bancshares Inc',	'SHF Holdings Inc.',	'Southern Missouri Bancorp Inc.',	'SmartFinancial Inc.',	'Summit Financial Group Inc.',	'Synovus Financial Corp.',	'South Plains Financial Inc.',	'1st Source Corporation',	'SouthState Corporation',	'Summit State Bank',	'Southern States Bancshares Inc.',	'S&T Bancorp Inc.',	'Stellar Bancorp Inc.',	'Stock Yards Bancorp Inc.',	'The Bancorp Inc',	'TC Bancshares Inc.',	'Texas Capital Bancshares Inc.',	'TriCo Bancshares',	'Texas Community Bancshares Inc.',	'Third Coast Bancshares Inc.',	'The Community Financial Corporation',	'Truist Financial Corporation',	'Triumph Financial Inc.',	'First Financial Corporation Indiana',	'Tompkins Financial Corporation',	'TowneBank',	'Trustmark Corporation',	'TrustCo Bank Corp NY',	'Timberland Bancorp Inc.',	'United Bancorp Inc.',	'United Security Bancshares',	'United Bankshares Inc.',	'United Community Banks Inc.',	'UMB Financial Corporation',	'Union Bankshares Inc.',	'Unity Bancorp Inc.',	'U.S. Bancorp',	'USCB Financial Holdings Inc.',	'Univest Financial Corporation',	'Virginia National Bankshares Corporation',	'Village Bank and Trust Financial Corp.',	'Veritex Holdings Inc.',	'Valley National Bancorp',	'Westamerica Bancorporation',	'Washington Federal Inc.',	'Western Alliance Bancorporation',	'Washington Trust Bancorp Inc.',	'Webster Financial Corporation',	'Wells Fargo & Company',	'WesBanco Inc.',	'WSFS Financial Corporation',	'West Bancorporation',	'Wintrust Financial Corporation',	'Zions Bancorporation N.A.', 'Bank of New York Mellon', 'Capital One Financial Corporation','Goldman Sachs Group Inc.','State Street Corporation','Morgan Stanley','Ally Financial Inc.','American Express Company','Northern Trust Corporation','Discover Financial Services']
name_dict = dict(zip(bank_tickers, bank_names))

def load_data(from_file=True):
    if from_file==True:
        init_prices = pd.read_csv("init_prices.csv")
        curr_prices = pd.read_csv("curr_prices.csv")
    else:
        init_prices = yf.download(bank_tickers, period="1d", start="2023-03-08", end="2023-03-09")["Adj Close"]
        curr_prices = yf.download(bank_tickers, period="1d")["Adj Close"]
        init_prices.to_csv("init_prices.csv", index=False)
        curr_prices.to_csv("curr_prices.csv", index=False)

    pct_diff = 100*(curr_prices.iloc[-1].div(init_prices.iloc[-1])-1)
    top_losers = round(pct_diff.sort_values()[0:10],1)
    loser_names = [name_dict[ticker] for ticker in top_losers.index.tolist()]
    loser_frame = pd.DataFrame(list(zip(loser_names,top_losers.index.tolist(),top_losers.values.tolist())), columns=['Bank Name', 'Ticker', 'Drawdown (%)'])
    largest_names = [name_dict[ticker] for ticker in largest_banks]
    largest_frame = pd.DataFrame(list(zip(largest_names,largest_banks,round(pct_diff[largest_banks],1).values.tolist())),columns=['Bank Name', 'Ticker', 'Drawdown (%)'])
    return [loser_frame, largest_frame.sort_values('Drawdown (%)')]

loser_frame, largest_frame = load_data()

with gr.Blocks() as crisis_dashboard:
    gr.Markdown("# <center>Banking Crisis Dashboard</center>")
    with gr.Tab("Bank Performance"):
        with gr.Row() as row:
            with gr.Column():
                gr.Markdown("## <center>Worst performing banks</center>")
                gr.DataFrame(loser_frame)
            with gr.Column():
                gr.Markdown("## <center>Largest bank performance</center>")
                gr.DataFrame(largest_frame)
        with gr.Row() as row:
            with gr.Column():
                gr.Markdown("## Failed banks")
                gr.DataFrame(pd.DataFrame(list(zip(failed_banks, failed_bank_names)), columns=['Ticker','Bank Name']))
    #with gr.Tab("Interest Rates"):
    #    steps = gr.Number(label="Inference steps", elem_id="steps", every=int, value=50)
    #with gr.Tab("Fed Balance Sheet"):
    #    seed = gr.Number(label="Seed", elem_id="seed", every=int, value=random.randint(0,2147483647))
    #with gr.Tab("Bank Balance Sheets"):
    #    scale = gr.Number(label="Guidance scale", elem_id='scale', value=7.5)

    #text.submit(infer, inputs=[text, style,steps, seed, scale], outputs=gallery)
    #btn.click(infer, inputs=[text, style,steps, seed, scale], outputs=gallery)
        
crisis_dashboard.launch()