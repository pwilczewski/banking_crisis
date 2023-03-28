import gradio as gr
import pandas as pd
import numpy as np
from data_proc import load_equity_data, load_yield_curve_data, load_credit_spread_data
from data_proc import plot_treasury_curves, plot_credit_spreads

loser_frame, largest_frame = load_equity_data(False)
yc_frame = load_yield_curve_data(False)
spread_frame = load_credit_spread_data(False)

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
                gr.Markdown("## <center>Treasury yield curve</center>")
                gr.Plot(plot_treasury_curves(yc_frame))
            with gr.Column():
                gr.Markdown("## <center>Credit spreads</center>")
                gr.Plot(plot_credit_spreads(spread_frame))
        gr.Markdown("### <center>Data Source: FRED</center>")
    #with gr.Tab("Fed Balance Sheet"):
    #    seed = gr.Number(label="Seed", elem_id="seed", every=int, value=random.randint(0,2147483647))
    #with gr.Tab("Bank Balance Sheets"):
    #    scale = gr.Number(label="Guidance scale", elem_id='scale', value=7.5)

    #text.submit(infer, inputs=[text, style,steps, seed, scale], outputs=gallery)
    #btn.click(infer, inputs=[text, style,steps, seed, scale], outputs=gallery)
        
crisis_dashboard.launch()