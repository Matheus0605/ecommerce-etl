import streamlit as st
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
METRICS_DIR = Path('data') / 'metrics'

st.set_page_config(page_title='Data Quality Dashboard', layout='wide')

st.title('Data Quality Dashboard')

metrics_path = METRICS_DIR / 'quality_metrics.json'

if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text(encoding='utf-8'))

    st.metric('Customers - válidos', metrics.get('customers_valid'))
    st.metric('Customers - quarantine', metrics.get('customers_quarantine'))

    st.metric('Products - válidos', metrics.get('products_valid'))
    st.metric('Products - quarantine', metrics.get('products_quarantine'))

    st.metric('Orders - válidos', metrics.get('orders_valid'))
    st.metric('Orders - quarantine', metrics.get('orders_quarantine'))

    st.subheader('Resumo')
    st.json(metrics)
else:
    st.warning('Métricas não encontradas. Execute o pipeline para gerar metrics em data/metrics/quality_metrics.json')
