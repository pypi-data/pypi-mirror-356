# -*- coding: utf-8 -*-
import json
import logging
import xmltodict

from zeep import Client, xsd
from zeep.helpers import serialize_object

from bluexpress.connector import Connector, ConnectorException
from bluexpress.settings import api_settings

logger = logging.getLogger(__name__)


class BluexpressHandler:
    """
        Handler to send shipping payload to Bluexpress.
    """

    def __init__(self, issue_wsdl=api_settings.BLUEXPRESS['ISSUE_WSDL'],
                 token_id=api_settings.BLUEXPRESS['TOKEN_ID'],
                 user_cod=api_settings.BLUEXPRESS['USER_COD'],
                 account_client=api_settings.SENDER['ACCOUNT_CLIENT'],
                 base_url_rest=api_settings.BLUEXPRESS['BASE_URL_REST'],
                 person_code=api_settings.SENDER['PERSON_CODE'],
                 verify=True, **kwargs):

        self.issue_wsdl = kwargs.pop('issue_wsdl', issue_wsdl)
        self.token_id = kwargs.pop('token_id', token_id)
        self.user_cod = kwargs.pop('user_cod', user_cod)
        self.base_url_rest = kwargs.pop('base_url_rest', base_url_rest)
        self.account_client = kwargs.pop('account_client', account_client)
        self.person_code = kwargs.pop('person_code', person_code)
        self.verify = kwargs.pop('verify', verify)
        self.header = self._headers(self.token_id, self.user_cod)
        self.connector = Connector(
            self._headers_rest(self.token_id, self.user_cod, self.account_client),
            verify_ssl=self.verify
        )

    def _headers(self, token, code_user):
        header = xsd.Element(
            '{http://ws.cl.bluex.cl/}requestHeader',
            xsd.ComplexType([
                xsd.Element('idToken', xsd.String()),
                xsd.Element('codigoUsuario', xsd.String()),
            ])
        )
        return header(idToken=token, codigoUsuario=code_user)

    def _headers_rest(self, token, code_user, account_client):
        return {
            'BX-TOKEN': token,
            'BX-USERCODE': code_user,
            'BX-CLIENT_ACCOUNT': account_client
        }

    def get_shipping_label(self, tracking_number):
        try:
            response = self.connector.get(
                f'{self.base_url_rest}/bx-label/v1/{tracking_number}')
            return {
                'base64': response['data'][0]['base64'] if response['data'] else response['data']
            }

        except ConnectorException as error:
            logger.error(error)
            raise ConnectorException(error.message, error.description, error.code) from error

    def get_default_payload(self, instance):
        lista_items = [
            {
                'codigoUnidadMasa': 'KG',
                'codigoUnidadLongitud': 'CM',
                'masa': 10,
                'largo': 10,
                'ancho': 10,
                'alto': 10,
            } for _ in range(instance.lumps)
        ]

        lista_contactos = [
            {
                'codigoTipoContacto': 'D',
                'codigoTipoCanal': 2,
                'valorCanal': instance.customer.email,
                'listaMacroestados': [{'macroestado': {'codigo': 0}}]
            },
            {
                'codigoTipoContacto': 'D',
                'codigoTipoCanal': 1,
                'valorCanal': instance.customer.phone,
                'listaMacroestados': [{'macroestado': {'codigo': 0}}]
            }
        ]

        payload = {
            'cuentaCliente': self.account_client,
            'nombreEmbalador': api_settings.SENDER['NAME'],
            'codigoPaisEmbalador': api_settings.SENDER['COUNTRY_CODE'],
            'codigoRegionEmbalador': api_settings.SENDER['REGION_CODE'],
            'codigoComunaEmbalador': api_settings.SENDER['COMMUNE_CODE'],
            'codigoLocalidadOrigen': api_settings.SENDER['LOCATION_CODE'],
            'direccionCompletaEmbalador': '{} {} {} {}'.format(
                api_settings.SENDER['STREET'],
                api_settings.SENDER['NUMBER'],
                api_settings.SENDER['FLOOR'],
                api_settings.SENDER['DPTO'],
            ),
            'direccionPisoEmbalador': xsd.SkipValue,
            'direccionDeptoEmbalador': xsd.SkipValue,
            'prefijoTelefonoEmbalador': xsd.SkipValue,
            'numeroTelefonoEmbalador': api_settings.SENDER['PHONE_NUMBER'],
            'anexoTelefonoEmbalador': xsd.SkipValue,
            'nombreDestinatario': instance.customer.full_name,
            'codigoPaisDestinatario': api_settings.DESTINATARY['COUNTRY_CODE'],
            'codigoRegionDestinatario': instance.region.code,
            'codigoComunaDestinatario': instance.commune.zone_code,
            'codigoLocalidadDestino': instance.location.code,
            'direccionCompletaDestinatario': instance.address.full_address,
            'direccionPisoDestinatario': xsd.SkipValue,
            'direccionDeptoDestinatario': xsd.SkipValue,
            'prefijoTelefonoDestinatario': '',
            'numeroTelefonoDestinatario': instance.customer.phone,
            'anexoTelefonoDestinatario': xsd.SkipValue,
            'valorDeclarado': '0',
            'codigoProducto': api_settings.BLUEXPRESS['PRODUCT_CODE'],
            'codigoMoneda': api_settings.BLUEXPRESS['CURRENCY_CODE'],
            'codigoEmpresa': api_settings.BLUEXPRESS['COMPANY_CODE'],
            'codigoTipoServicio': api_settings.BLUEXPRESS['SERVICE_TYPE_CODE'],
            'codigoPersona': self.person_code,
            'codigoFamiliaProducto': api_settings.BLUEXPRESS['PRODUCT_FAMILY_CODE'],
            'observaciones': '',
            'centroCosto': xsd.SkipValue,
            'switchNotificar': 'false',
            'codigoAgencia': instance.agency_id if instance.agency_id is not None else 0,
            'listaEmisionEmbalajesCrearReq': {
                'emisionEmbalajeCrearReq': lista_items
            },
            'listaContactosCanal': {
                'contactoCanal': lista_contactos
            },
            'listaNumerosReferenciaCrearReq': {
                'numeroReferencia': instance.reference,
            },
            'listaEmisionMercanciasPeligrosas': xsd.SkipValue,
            'listaDocumentosDevolucionCrearReq': xsd.SkipValue,
            'listaCobrosContraEntregaCrearReq': xsd.SkipValue
        }

        if hasattr(instance, 'sender'):
            payload.update({
                'codigoRegionEmbalador': instance.sender.region.code,
                'codigoComunaEmbalador': instance.sender.commune.zone_code,
                'codigoLocalidadOrigen': instance.sender.location.code,
                'direccionCompletaEmbalador': instance.sender.address.full_address
            })

        logger.debug(payload)
        return payload

    def create_shipping(self, data):
        logger.debug(data)

        client = Client(self.issue_wsdl)
        client.set_ns_prefix('ws', 'http://ws.bluex.cl/')

        try:
            zeep_response = client.service.emitir(
                codigoFormatoImpresion=api_settings.BLUEXPRESS['PRINT_FORMAT_CODE'],
                ordenServicio=data,
                _soapheaders=[self.header]
            )

            response = dict(serialize_object(zeep_response))
            response.update({'tracking_number': response['nroFolio']})

            logger.debug(response)
            return response
        except Exception as error:
            logger.error(error)
            raise ConnectorException(error.message, error.description, error.code) from error

    def get_tracking(self, identifier):
        raise NotImplementedError('get_tracking is not a method implemented for BluexpressHandler')

    def get_events(self, raw_data):
        events = []

        try:
            json_data = self._parse_xml_to_json(raw_data.get('tracking_data'))
            punctures = self._get_value_by_key(json_data, 'pinchazo')

            if isinstance(punctures, list):
                events = [
                    {
                        'city': p.get('nombrePosta'),
                        'state': p.get('codigoPosta'),
                        'description': f"{p.get('codigoTipo')} - {p.get('nombreTipo')}",
                        'date': p.get('fecha'),
                    } for p in punctures if isinstance(p, dict)
                ]
            elif isinstance(punctures, dict):
                events = [{
                    'city': punctures.get('nombrePosta'),
                    'state': punctures.get('codigoPosta'),
                    'description': f"{punctures.get('codigoTipo')} - {punctures.get('nombreTipo')}",
                    'date': punctures.get('fecha'),
                }]
        except Exception as e:
            logger.error(f"Error parsing events from Bluexpress XML: {e}")

        return events

    def get_status(self, raw_data):
        status = 'Sin estado'
        is_delivered = False

        try:
            json_data = self._parse_xml_to_json(raw_data.get('tracking_data'))
            macrostates = self._get_value_by_key(json_data, 'macroestado')

            if isinstance(macrostates, list):
                status_list = [m.get('nombre') for m in macrostates if isinstance(m, dict) and m.get('nombre')]
                if status_list:
                    status = status_list[-1]
            elif isinstance(macrostates, dict):
                status = macrostates.get('nombre', 'Sin estado')

            if status == 'Entregado':
                is_delivered = True
        except Exception as e:
            logger.error(f"Error parsing status from Bluexpress XML: {e}")

        return status, is_delivered

    def _parse_xml_to_json(self, tracking_data):
        if not tracking_data:
            return {}
        try:
            parse = xmltodict.parse(tracking_data)
            return json.loads(json.dumps(parse))
        except Exception as e:
            logger.error(f"Error parsing XML to JSON: {e}")
            return {}

    def _get_value_by_key(self, json_data, search_key):
        if not isinstance(json_data, dict):
            return None

        for key, value in json_data.items():
            if key == search_key:
                return value
            elif isinstance(value, dict):
                returned_value = self._get_value_by_key(value, search_key)
                if returned_value is not None:
                    return returned_value
            elif isinstance(value, list):
                for item in value:
                    returned_value = self._get_value_by_key(item, search_key)
                    if returned_value is not None:
                        return returned_value
        return None
