/**
 * Función que nos permite cargar partes de html para acelerar la descarga de la web.
 */
async function cargar(pagina) {

    const navlinks = document.querySelectorAll('.menu-activo');
    navlinks.forEach(link => {
        link.classList.remove('menu-activo');
    })

    const equipo = await fetch(`/${pagina}`);

    if (equipo.ok) {
        document.getElementById("contenido").innerHTML = await equipo.text()
        document.getElementById(pagina).classList.add("menu-activo");
    }else{
        document.getElementById("contenido").innerHTML = "Error al cargar los datos";
    }

}