 let productos = [];
 fetch("./static/js/productos.json")
  .then(response => response.json())
  .then(data => {
    productos = data;
    const contenedorProductos = document.querySelector("#contenedor-productos");
    const botonesCategorias = document.querySelectorAll(".boton-categoria");
    const tituloPrincipal = document.querySelector("#titulo-principal");
    let botonesAgregar = document.querySelectorAll(".producto-agregar");
    const numero = document.querySelector("#numero");

    cargarProductos(productos);
    console.log(productos);

    function cargarProductos(productosElegidos) {
      contenedorProductos.innerHTML = "";
      productosElegidos.forEach(producto => {
        const div = document.createElement("div")
        div.classList.add("producto");
        div.innerHTML = `
          <img src="${producto.imagen}" alt="${producto.nombre}" class="producto-imagen">
          <div class="producto-detalle">
            <h3 class="producto-nombre">${producto.nombre}</h3>
            <p class="producto-precio">${producto.precio}</p>
            <button class="producto-agregar" id="${producto.id}">Agregar</button>
          </div>
        `;
        contenedorProductos.append(div);
      });
      console.log(productosElegidos);
      actualizarBotonesAgregar();
    }

    botonesCategorias.forEach(boton => {
      boton.addEventListener("click", (e) => {
        botonesCategorias.forEach(boton => boton.classList.remove("active"));
        e.currentTarget.classList.add("active");
        if (e.currentTarget.id !== "todos") {
          const productosCategoria = productos.find(producto => producto.categoria.id === e.currentTarget.id);
          if (productosCategoria) {
            console.log(productosCategoria);
            tituloPrincipal.innerHTML = productosCategoria.categoria.nombre;
            const productosBoton = productos.filter(producto => producto.categoria.id === e.currentTarget.id);
            cargarProductos(productosBoton);
          } else {
            console.error('No products found for the category:', e.currentTarget.id);
          }
        } else {
          tituloPrincipal.innerText = "Todos los productos";
          cargarProductos(productos);
        }
      });
    });

    function actualizarBotonesAgregar() {
      botonesAgregar = document.querySelectorAll(".producto-agregar");
      botonesAgregar.forEach(boton => {
        boton.addEventListener("click", agregarAlCarrito);
      });
    }

    let productosEnCarrito;
    let productosEnCarritoLs = localStorage.getItem("productos-en-carrito");
    if (productosEnCarritoLs) {
      productosEnCarrito = JSON.parse(productosEnCarritoLs);
      actualizarNumero();
    } else {
      productosEnCarrito = [];
    }

    function agregarAlCarrito(e) {

        Toastify({
            text: "Producto agregado",
            duration: 3000,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "right", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
              background: "linear-gradient(to right, #4b33a8, #785ce9)",
              borderRadius: "2rem",
              textTransform: "uppercase",
              fontSize: ".75rem"
            },
            offset: {
                x: '1.5rem', // horizontal axis - can be a number or a string indicating unity. eg: '2em'
                y: '1.5rem' // vertical axis - can be a number or a string indicating unity. eg: '2em'
              },
            onClick: function(){} // Callback after click
          }).showToast();

      const idBoton = e.currentTarget.id;
      const productoAgregado = productos.find(producto => producto.id === idBoton);
      if (productosEnCarrito.some(producto => producto.id === idBoton)) {
        const index = productosEnCarrito.findIndex(producto => producto.id === idBoton);
        productosEnCarrito[index].cantidad++;
      } else {
        productoAgregado.cantidad = 1;
        productosEnCarrito.push(productoAgregado);
      }
      actualizarNumero();
      localStorage.setItem("productos-en-carrito", JSON.stringify(productosEnCarrito));
    }

    function actualizarNumero() {
      let nuevoNumero = productosEnCarrito.reduce((acc, producto) => acc + producto.cantidad, 0);
      numero.innerText = nuevoNumero;
    }
  })
  .catch(error => {
    console.error('Error al cargar los productos:', error);
  });