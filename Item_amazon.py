
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException
import json
import pandas as pd
from genius import generate_html_response
import streamlit as st

def search_items(busca):

    """ Following are your credentials """
    """ Please add your access key here """
    access_key = st.secrets["accesskey"]

    """ Please add your secret key here """
    secret_key = st.secrets["secretkey"]

    """ Please add your partner tag (store/tracking id) here """
    partner_tag = st.secrets["partnertag"]

    """ PAAPI host and region to which you want to send request """
    """ For more details refer: https://webservices.amazon.com/paapi5/documentation/common-request-parameters.html#host-and-region"""
    host = "webservices.amazon.com.br"
    region = "us-east-1"

    """ API declaration """
    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    """ Request initialization"""

    pergunta=generate_html_response(busca)

    """ Specify keywords """
    keywords = pergunta

    print(f'Respota: {pergunta}\n')

    """ Specify the category in which search request is to be made """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/use-cases/organization-of-items-on-amazon/search-index.html """
    search_index = "All"

    """ Specify item count to be returned in search result """
    item_count = 5

    """ Choose resources you want from SearchItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/search-items.html#resources-parameter """
    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
        SearchItemsResource.IMAGES_PRIMARY_LARGE,
        SearchItemsResource.ITEMINFO_FEATURES,
        SearchItemsResource.ITEMINFO_CLASSIFICATIONS,
        SearchItemsResource.CUSTOMERREVIEWS_STARRATING,
        
    ]

    """ Forming request """
    try:
        search_items_request = SearchItemsRequest(
            partner_tag=partner_tag,
            partner_type=PartnerType.ASSOCIATES,
            keywords=keywords,
            search_index=search_index,
            item_count=item_count,
            resources=search_items_resource,
            condition='New',
            sort_by='Relevance'

        )
    except ValueError as exception:
        print("Error in forming SearchItemsRequest: ", exception)
        return

    try:
        """ Sending request """
        response = default_api.search_items(search_items_request)
        return response.to_dict()

    except ApiException as exception:
        print("Error calling PA-API 5.0!")
        print("Status code:", exception.status)
        print("Errors :", exception.body)
        print("Request ID:", exception.headers["x-amzn-RequestId"])

    except TypeError as exception:
        print("TypeError :", exception)

    except ValueError as exception:
        print("ValueError :", exception)

    except Exception as exception:
        print("Exception :", exception)

#data=search_items()


def generate_html_from_json(data):
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<style>
        body {
            font-family: 'Open Sans', sans-serif;
            color: #333;
            margin: 0;
            padding: 0;
        }

        .head h1, .head h2, .head p {
            font-family: Arial;
        }

        .head h1 {
            text-align: center;
            margin-top: 20px;
            font-size: 2.5em;
            color: #007BFF;
        }

        .head h2 {
            text-align: center;
            font-size: 2em;
            color: #007BFF;
        }

        .head p {
            text-align: center;
            font-size: 1.2em;
            margin: 20px 0;
        }
    .product-section {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin: 20px;
    }

    .product {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin: 10px;
        padding: 10px 20px;
        width: 300px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    .product img {
        max-width: 80%;
        height: auto;
        border-radius: 8px;
    }

    .product h3 {
        font-size: 1.5em;
        margin: 15px 0;
        color: #007BFF;
    }

    .product ul {
        list-style-type: none;
        padding: 0;
        text-align: left;
    }

    .product ul li {
        background: url('https://cdn-icons-png.flaticon.com/512/117/117255.png') no-repeat left center;
        background-size: 20px;
        padding-left: 30px;
        margin: 10px 0;
    }

    .product a {
        display: inline-block;
        margin-top: 15px;
        padding: 10px 20px;
        background-color: #007BFF;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        transition: background-color 0.3s;
    }

    .product a:hover {
        background-color: #0056b3;
    }
</style>
<body>     
      <div class="head">
      <h2>Produtos Encontrados ✨</h2>
      <p style="font-family: Arial;">Confira abaixo os produtos encontrados:</p>
    </div>
    <div class="product-section">
    """

    # Verifica se há resultados na pesquisa
    if 'search_result' in data and 'items' in data['search_result']:
        items = data['search_result']['items']
        
        # Itera sobre os itens
        for item in items:
            html += "<div class='product'>\n"
            
            # Adiciona o título do item
            if 'item_info' in item and 'title' in item['item_info']:
                title = item['item_info']['title']['display_value']
                html += f"<h3>{title}</h3>\n"
            
            # Adiciona a imagem do item
            if 'images' in item and 'primary' in item['images'] and 'large' in item['images']['primary']:
                image_url = item['images']['primary']['large']['url']
                html += f"<img src='{image_url}' alt='Imagem do Produto'><br><br>\n"
            
            # Adiciona o preço do item
            if 'offers' in item and 'listings' in item['offers'] and len(item['offers']['listings']) > 0:
                price = item['offers']['listings'][0]['price']['display_amount']
                html += f"<b>PREÇO: {price}</b><br>\n"
            
            # Adiciona o link para a página de detalhes do item
            if 'detail_page_url' in item:
                detail_url = item['detail_page_url']
                html += f"<a href='{detail_url}' target='_blank'>Clique aqui</a>\n"
            
            html += "<ul>\n"
            
            # Adiciona as características do item
            if 'item_info' in item and 'features' in item['item_info'] and item['item_info']['features']:
                features = item['item_info']['features']['display_values']
                for feature in features:
                    html += f"<li>{feature}</li>\n"
            
            html += "</ul>\n"
            html += "</div>\n"

    html += """</div>

</body>
</html>"""

    return html

#print(generate_html_from_json(data))
