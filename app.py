from flask import Flask, request, render_template_string
app = Flask(__name__)


# URL base de YouTube. Puedes cambiar esto según necesites.
base_youtube_url = "https://www.youtube.com/watch?v=i4t7L2oKWkQ"

def buscar_palabra_en_srt(archivo_srt, palabra):    
    resultados = []    
    with open(archivo_srt, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()

    bloques = contenido.split('\n\n')
    for bloque in bloques:
        lineas = bloque.split('\n')
        if len(lineas) >= 2:
            numero_linea = lineas[0]
            texto = ' '.join(lineas[1:])
            if palabra.lower() in texto.lower():
                resultados.append(f"{numero_linea}:{texto}")
    return resultados

@app.route('/', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        palabra = request.form['palabra']
        resultados = buscar_palabra_en_srt('subtitulos.srt', palabra)
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <body>
                <form action="/" method="post">
                    Palabra: <input type="text" name="palabra">
                    <input type="submit" value="Buscar">
                </form>
                {% for resultado in resultados %}
                   <p>
                    {% set partes = resultado.split(':') %}
                    {% if partes|length >= 3 %}
                        {{ partes[0] }}:
                        <a href="{{ base_youtube_url }}&t={{ partes[1] }}s" target="_blank">{{ partes[1] }}</a>:
                        {{ partes[2] }} - {{ ' '.join(partes[3:]) }}
                    {% else %}
                        {{ resultado }}
                    {% endif %}
                    </p>
                {% endfor %}
            </body>
            </html>
        ''', resultados=resultados, base_youtube_url=base_youtube_url)
    else:
        return '''
            <!DOCTYPE html>
            <html>
            <body>
                <form action="/" method="post">
                    Palabra: <input type="text" name="palabra">
                    <input type="submit" value="Buscar">
                </form>
            </body>
            </html>
        '''

if __name__ == '__main__':
    app.run(debug=True)




