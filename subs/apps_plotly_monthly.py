
from flask import render_template, session
import pandas as pd
import plotly.express as px

def apps_plotly_monthly():
    # Carrega dados do CSV
    df = pd.read_csv('data/trabalho.csv')
    df = df.dropna(subset=['order_date', 'quantity', 'price'])
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_revenue'] = df['quantity'] * df['price']
    df['month'] = df['order_date'].dt.strftime('%B')

    # Garante ordem dos meses
    month_order = [
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ]
    monthly_revenue = (
        df.groupby('month')['total_revenue']
          .sum()
          .reindex(month_order, fill_value=0)
          .reset_index()
    )

    # Cria gráfico interativo
    fig = px.line(
        monthly_revenue,
        x='month', y='total_revenue',
        markers=True,
        title='Faturamento por Mês (Interativo)',
        labels={'month':'Mês','total_revenue':'Receita Total'}
    )
    plot_div = fig.to_html(full_html=False, div_id='monthly-plot')

    return render_template(
        'plot.html',
        plot_div=plot_div,
        ulogin=session.get('user')
    )
