import http.server
import socketserver
import http.client
import json
socketserver.TCPServer.allow_reuse_address = True


IP = "localhost"
PORT = 8000

HTML_00 = (' <!DOCTYPE html>\n'
           '<html lang="es">\n'
           '<head>\n'
           '<title>OpenFDA proyect</title>\n'
           '<head>\n'
           '    <meta charset="UTF-8">\n'
           '</head>\n'
           '<body>\n')

HTML_end = ('</ul>\n'
            '\n'
            '<a href="/">Home</a>'
            '</body>\n'
            '</html>')

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def openFDA(self, param):
        REST_conect = 'api.fda.gov'
        REST_enter = '/drug/label.json'
        headers = {'User-Agent': 'http-client'}

        if '&' in param:
            list_param = param.split('&')
            list_field = list_param[0].split('=')
            field = list_field[1]
            list_limit = list_param[1].split('=')
            limite = list_limit[1]
            if list_field[0] == 'active_ingredient':
                url = REST_enter + '?search=active_ingredient:{}'.format(field) + '&limit={}'.format(limite)
            elif list_field[0] == 'company':
                url = REST_enter + '?search=openfda.manufacturer_name:{}'.format(field) + '&limit={}'.format(limite)

        else:
            if 'limit' in param:
                list_limit = param.split('=')
                limite = list_limit[1]
                url = REST_enter + '?limit={}'.format(limite)
            else:
                limite = '10'
                lista_campo = param.split('=')
                campo = lista_campo[1]
                if lista_campo[0] == 'active_ingredient':
                    url = REST_enter + '?search=active_ingredient:{}'.format(campo) + '&limit={}'.format(limite)
                elif lista_campo[0] == 'company':
                    url = REST_enter + '?search=openfda.manufacturer_name:{}'.format(campo) + '&limit={}'.format(limite)



        print(url)
        c = http.client.HTTPSConnection(REST_conect)
        c.request("GET", url, None, headers)
        resp = c.getresponse()
        json_fda = resp.read().decode("utf-8")
        c.close()
        dict_fda = json.loads(json_fda)
        return dict_fda


    def formulario(self):
        with open('index.html','r') as f:
            formulario = f.read()
            return formulario

    def listDrugs(self, dic):
        HTML_resp = HTML_00
        HTML_resp += ('<h1>Lista Medicamentos</h1>'
                      '<h3>Nombre. ID</h3>'
                      '\n'
                      '<ul>\n')

        results = dic['results']
        for med in results:
            if med['openfda']:
                nombre = med['openfda']['substance_name'][0]
            else:
                nombre = "Desconocido"
            id = med['id']

            HTML_resp += "<li>{}. {}</li>\n".format(nombre,id)
        mensaje = HTML_resp + HTML_end
        return mensaje

    def listCompanies(self, dic):
        HTML_resp = HTML_00
        HTML_resp += ('<h1>Lista Companies</h1>'
                      '\n'
                      '<ul>\n')
        results = dic['results']
        for med in results:
            if med['openfda']:
                company = med['openfda']['manufacturer_name'][0]
            else:
                company = "Desconocido"

            HTML_resp += "<li>{}</li>\n".format(company)
        mensaje = HTML_resp + HTML_end
        return mensaje

    def SearchDrug(self, dic):
        HTML_resp = HTML_00
        HTML_resp += ('<h1>Lista Medicamentos</h1>'
                      '<h3>Nombre. ID</h3>'
                      '\n'
                      '<ul>\n')

        results = dic['results']
        for med in results:
            if med['openfda']:
                nombre = med['openfda']['substance_name'][0]
            else:
                nombre = "Desconocido"
            id = med['id']

            HTML_resp += "<li>{}. {}</li>\n".format(nombre,id)
        mensaje = HTML_resp + HTML_end
        return mensaje

    def SearchCompany(self, dic):
        HTML_resp = HTML_00
        HTML_resp += ('<h1>Lista Medicamentos de la empresa</h1>'
                      '<h3>Nombre. ID</h3>'
                      '\n'
                      '<ul>\n')

        results = dic['results']
        for med in results:
            if med['openfda']:
                nombre = med['openfda']['generic_name'][0]
            else:
                nombre = "Desconocido"
            id = med['id']

            HTML_resp += "<li>{}. {}</li>\n".format(nombre,id)
        mensaje = HTML_resp + HTML_end
        return mensaje

    def listWarnings(self, dic):
        HTML_resp = HTML_00
        HTML_resp += ('<h1>Lista Advertencias</h1>'
                      '\n'
                      '<ul>\n')
        results = dic['results']
        for med in results:
            if 'warnings' in med:
                advertencias = med["warnings"][0]
                HTML_resp += "<li>{}</li>\n".format(advertencias)
            else:
                advertencias = 'Desconocido'
                HTML_resp += "<li>{}</li>\n".format(advertencias)
        mensaje = HTML_resp + HTML_end
        return mensaje




    def do_GET(self):
        path = self.path
        if '?' in path:
            list_path = path.split('?')
            recurso = list_path[0].strip('/')
            parametros = list_path[1]
        else:
            recurso = path


        if path == '/':
            self.send_response(200)
            info = self.formulario()
        elif recurso == 'listDrugs':
            self.send_response(200)
            dic_json = self.openFDA(parametros)
            info = self.listDrugs(dic_json)
        elif recurso == 'listCompanies':
            self.send_response(200)
            dic_json = self.openFDA(parametros)
            info = self.listCompanies(dic_json)
        elif recurso.startswith('searchDrug'):
            self.send_response(200)
            dic_json = self.openFDA(parametros)
            info = self.SearchDrug(dic_json)
        elif recurso.startswith('searchCompany'):
            self.send_response(200)
            dic_json = self.openFDA(parametros)
            info = self.SearchCompany(dic_json)
        elif recurso == 'listWarnings':
            self.send_response(200)
            dic_json = self.openFDA(parametros)
            info = self.listWarnings(dic_json)
        elif recurso == '/redirect':
            self.send_response(200)
            info = self.formulario()
        elif recurso == '/secret':
            self.send_response(401)
            info = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>WWW-Authenticate</title>
  </head>
  <body>
    <h1>401 Unauthorized.</h1>
  </body>
</html>'''
        else:
            self.send_response(404)
            info = '''<!DOCTYPE html>
            <html>
            <head>
              <title>ERROR page</title>
            </head>
            <body>
            <h1>ERROR 404</h1>
            <p>La pagina que busca no esta disponible</p>
            <p>Recurso no encontrado...</p>
            '''




        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(info, "utf8"))
        print("File served!")


        return

Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass
httpd.server_close()
print("")
print("Server stopped!")
