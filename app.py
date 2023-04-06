import gradio as gr
import pandas as pd
import numpy as np
from data_proc import load_equity_data, load_yield_curve_data, load_credit_spread_data, load_fed_balance_sheet
from data_proc import plot_treasury_curves, plot_credit_spreads, plot_fed_balance_sheet

loser_frame, largest_frame = load_equity_data()
yc_frame = load_yield_curve_data()
spread_frame = load_credit_spread_data()
fed_frame = load_fed_balance_sheet()

with gr.Blocks() as crisis_dashboard:
    gr.Markdown("<font size=36><center>Banking Crisis Dashboard</center></font>")
    with gr.Tab("Bank Performance"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("## <center>Worst performing banks</center>")
                gr.DataFrame(loser_frame)
            with gr.Column():
                gr.Markdown("## <center>Largest bank performance</center>")
                gr.DataFrame(largest_frame)
        gr.Markdown("### <center>*performance since 3/8/2023</center>")
        with gr.Row():
            with gr.Column():
                gr.Markdown("## Failed banks")
                gr.DataFrame(pd.DataFrame(list(zip(['SBNY','SIVB'], ['Signature Bank', 'SVB Financial Group'])), columns=['Ticker','Bank Name']))
    with gr.Tab("Interest Rates"):
        with gr.Row():
            with gr.Column():
                # gr.Markdown("## <center>Treasury yield curve</center>")
                gr.Plot(plot_treasury_curves(yc_frame))
            with gr.Column():
                # gr.Markdown("## <center>Credit spreads</center>")
                gr.Plot(plot_credit_spreads(spread_frame))
        gr.Markdown("### <center>Data Source: FRED</center>")
    with gr.Tab("Fed Balance Sheet"):
        with gr.Row():
            with gr.Column():
                gr.Plot(plot_fed_balance_sheet(fed_frame))
            with gr.Column():
                gr.Plot(plot_fed_balance_sheet(fed_frame, 'Liabilities'))
        gr.Markdown("### <center>*change since 3/8/2023")
    #with gr.Tab("Bank Balance Sheets"):
        
crisis_dashboard.launch()