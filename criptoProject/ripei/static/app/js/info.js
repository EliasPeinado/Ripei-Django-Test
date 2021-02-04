const CriptoAPI = async() => {
    const api = 'http://127.0.0.1:8000/'
    const response = await fetch(api + 'api/crito/');
    const myJson = await response.json();

    const div_s = document.createElement("div");
    div_s.className = "productos";
    document.getElementById('contenido').appendChild(div_s)

    const div_p = document.createElement("div");
    div_p.className = "producto";
    div_s.appendChild(div_p)


    const fragment = document.createDocumentFragment()


    for (i of myJson) {

        const div_cont = document.createElement('div');
        div_cont.innerHTML = '<br><br><hr></hr><br>'
        fragment.appendChild(div_cont);

        const img = document.createElement('IMG');
        img.src = i['imagen'];
        div_cont.appendChild(img);

        const div_det = document.createElement('div');
        div_det.className = 'detalle';
        div_det.innerHTML = `<h2>${i['name']}</h2> <br>\
        <p>Descripcion : ${i['descripcion']} </p>\
        <h3>Su valor es de: ${i['valor']}</h3><br><br>`
        div_cont.appendChild(div_det);
    }

    div_p.appendChild(fragment)
}