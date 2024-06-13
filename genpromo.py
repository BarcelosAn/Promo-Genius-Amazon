from Item_amazon import search_items
import json
import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide",page_title="Promo Genius",page_icon="🛍")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.header("🛒 Promo Genius - IA de promoções",divider="grey",anchor=None)



perg=st.text_input('o que deseja procurar?\n')

if perg != "":
    data = search_items(perg)




def produto():
    produtos = data['search_result']['items']
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #fff;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                flex-wrap: wrap;
                gap: 20px;
                padding: 20px;
                margin: 0;
            }
            .product-card {
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                width: 320px;
                height: 720px;
                padding: 5px 20px;
                text-align: center;
                transition: transform 0.3s;
            }
            .product-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            }
            .product-card h1 {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 22px;
                color: #333;
                margin-bottom: 20px;
            }
            .product-card img {
                width: 100%;
                border-radius: 8px;
                margin-bottom: 5px;
            }
            .price {
                margin-bottom: 20px;
            }
            .current-price {
                font-size: 26px;
                font-weight: 650;
                color: #1eaf10;
                display: block;
            }
            .original-price {
                font-size: 18px;
                color: #777;
                text-decoration: line-through;
                display: block;
            }
            .discount {
                margin-top: 5px;
                font-size: 16px;
                color: #3c60ff;
                font-weight: 500;
                display: block;
            }
            .features {
                text-align: left;
                padding-left: 0;
                list-style: none;
                margin-bottom: 20px;
            }
            .features li {    
                display: -webkit-box;
                -webkit-line-clamp: 2; /* Número de linhas */
                -webkit-box-orient: vertical;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 15px;
                margin-bottom: 10px;
                position: relative;
            }
            .features li::before {
                content: '🌐';
                padding-right: 5px;
                left: 0;
                color: #007bff;
                font-size: 15px;
                line-height: 15px;
            }
            .buy-button {
                display: inline-block;
                background-color: #007bff;
                color: white;
                padding: 12px 80px;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            .buy-button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
    """

    for produto in produtos:
        titulo_produto = produto['item_info']['title']['display_value']
        url_produto = produto['detail_page_url']
        oferta_produto = produto['offers']['listings'][0]['price']['amount']
        img_produto = produto['images']['primary']['large']['url']

        if produto['offers']['listings'][0]['price']['savings']:
            desconto_produto = produto['offers']['listings'][0]['price']['savings']['amount']
            perc_produto = produto['offers']['listings'][0]['price']['savings']['percentage']
            valor_origi = oferta_produto + desconto_produto
            desconto_texto = f"Desconto: R$ {desconto_produto} ({perc_produto}%)"
            valor_origi_texto = f"R$ {valor_origi:.2f}"
        else:
            desconto_texto = ""
            valor_origi_texto = ""
        if produto['item_info']['features']:
            cat_produto = produto['item_info']['features']['display_values']
            cat_produto_html = "".join([f"<li>{cat}</li>" for cat in cat_produto[:3]])

        html_content += f"""
        <div class="product-card">
            <h1>{titulo_produto}</h1>
            <a href="{url_produto}" target="_blank">
                <img src="{img_produto}" alt="{titulo_produto}">
            </a>
            <div class="price">
                <span class="current-price">R$ {oferta_produto:.2f}</span>
                <span class="original-price">{valor_origi_texto}</span>
                <span class="discount">{desconto_texto}</span>
            </div>
            <ul class="features">
                {cat_produto_html}
            </ul>
            <a href="{url_produto}" class="buy-button" target="_blank">Comprar Agora</a>
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    # Escrever o conteúdo HTML para um arquivo
    with open('produtos.html', 'w', encoding='utf-8') as file:
        file.write(html_content)


tem_anuncio = 0
erro=0

if st.button("Buscar"):
    if perg:
        # EFEITO DE LOADING - Enquanto busca o resultado da IA
        with st.spinner("🤖 Buscando promoções..."):
            produto()
            with open('produtos.html', 'r', encoding='utf-8') as file:
                # Leia o conteúdo do arquivo
                html_content = file.read()
            components.html(html_content, height=1800, scrolling=True)

            # ARMAZENA - o historico de busca
            st.session_state["historico_busca"] = [html_content]
            tem_anuncio=1
    
    else:
        erro="🛑 Por favor, insira algo para buscar."
        st.write(erro)

if erro == 0:
    ""
    if tem_anuncio == 1:
        ""
    else:
        if "historico_busca" not in st.session_state:
                ""
                #st.session_state["historico_busca"] = ""
        else:
            components.html(st.session_state["historico_busca"][0], height=1800, scrolling=True)

#print(json.dumps(data, indent=4))
#python -m streamlit run genpromo.py