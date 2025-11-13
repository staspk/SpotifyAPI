class Html():
    def Success(): return Html.skeleton('Success', Html.message('SUCCESS', '#4CAF50'))
    def Error():   return Html.skeleton('Error', Html.message('something went wrong', '#d4695b'))

    def message(text="", text_color='white'):
        """
        A div with centered text
        """
        html  =  '<div style="display:flex; flex-direction:column; align-items:center; '
        html += f'justify-content:center; height:100%; width:100%; color:{text_color};">'
        html += f'<h2>{text}</h2>'
        html +=  '</div>'
        return html

    def skeleton(title="", body=""):
        """
        basic html structure
        """
        html            = '<!DOCTYPE html><html><head><meta charset="utf-8">'
        if title: html += f'<title>{title}</title>'
        html           += '<style>html, body { margin:0; padding:0; height:100%; background:black; }</style>'
        if body: html  += body
        html           += '</body></html>'
        return html