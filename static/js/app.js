// TaskManager - logica del frontend (consume la API REST /api/tareas)
const API = "/api/tareas";

const $ = (sel) => document.querySelector(sel);
const lista = $("#lista-tareas");
const vacio = $("#vacio");
const form = $("#form-tarea");
const dialogo = $("#dialogo-editar");
const formEditar = $("#form-editar");

let tareas = [];

// ---------------------------------------------------------------- utilidades
function toast(mensaje, error = false) {
  const t = $("#toast");
  t.textContent = mensaje;
  t.classList.toggle("error", error);
  t.classList.add("visible");
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => t.classList.remove("visible"), 2800);
}

function escapar(texto) {
  const div = document.createElement("div");
  div.textContent = texto ?? "";
  return div.innerHTML;
}

async function peticion(url, opciones = {}) {
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  const datos = await resp.json().catch(() => ({}));
  if (!resp.ok) {
    const msg = (datos.errores && datos.errores.join(" ")) || datos.error || "Error inesperado.";
    throw new Error(msg);
  }
  return datos;
}

function marcarError(input, errorEl, mensaje) {
  input.classList.toggle("invalido", Boolean(mensaje));
  errorEl.textContent = mensaje || "";
}

// --------------------------------------------------------- RF02 Consultar
async function cargarTareas() {
  const params = new URLSearchParams();
  const estado = $("#filtro-estado").value;
  const prioridad = $("#filtro-prioridad").value;
  if (estado) params.set("estado", estado);
  if (prioridad) params.set("prioridad", prioridad);
  try {
    tareas = await peticion(`${API}?${params}`);
    pintarTareas();
    cargarResumen();
  } catch (e) {
    toast(e.message, true);
  }
}

async function cargarResumen() {
  try {
    const r = await peticion("/api/resumen");
    $("#r-total").textContent = r.Total;
    $("#r-pendiente").textContent = r["Pendiente"];
    $("#r-proceso").textContent = r["En proceso"];
    $("#r-terminada").textContent = r["Terminada"];
  } catch (_) { /* el resumen es informativo */ }
}

function pintarTareas() {
  lista.innerHTML = "";
  vacio.hidden = tareas.length > 0;
  for (const t of tareas) {
    const li = document.createElement("li");
    li.className = `tarea p-${t.prioridad} ${t.estado === "Terminada" ? "terminada" : ""}`;
    li.dataset.id = t.id;
    const opciones = window.ESTADOS.map(
      (e) => `<option value="${e}" ${e === t.estado ? "selected" : ""}>${e}</option>`
    ).join("");
    li.innerHTML = `
      <div>
        <h3>${escapar(t.nombre)}</h3>
        ${t.descripcion ? `<p>${escapar(t.descripcion)}</p>` : ""}
        <div class="meta">
          <span class="badge ${t.prioridad}">${t.prioridad}</span>
          ${t.responsable ? `<span>👤 ${escapar(t.responsable)}</span>` : ""}
          <span>#${t.id} · ${t.fecha_creacion}</span>
        </div>
      </div>
      <div class="controles">
        <select class="sel-estado" aria-label="Cambiar estado">${opciones}</select>
        <div class="botones">
          <button class="btn chico btn-editar">Editar</button>
          <button class="btn chico peligro btn-eliminar">Eliminar</button>
        </div>
      </div>`;
    lista.appendChild(li);
  }
}

// ---------------------------------------------------------- RF01 Registrar
form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const nombre = $("#nombre");
  if (!nombre.value.trim()) {
    marcarError(nombre, $("#error-nombre"), "El nombre de la tarea es obligatorio.");
    nombre.focus();
    return;
  }
  marcarError(nombre, $("#error-nombre"), "");
  const datos = {
    nombre: nombre.value,
    // si esta vacia no se envia (el backend la trata como opcional)
    descripcion: $("#descripcion").value.trim() || undefined,
    responsable: $("#responsable").value,
    prioridad: $("#prioridad").value,
    estado: $("#estado").value,
  };
  try {
    const r = await peticion(API, { method: "POST", body: JSON.stringify(datos) });
    toast(r.mensaje);
    form.reset();
    $("#prioridad").value = "Media";
    cargarTareas();
  } catch (e) {
    toast(e.message, true);
  }
});

// ------------------------------------------- RF03, RF04, RF05 (delegacion)
lista.addEventListener("click", async (ev) => {
  const li = ev.target.closest(".tarea");
  if (!li) return;
  const id = Number(li.dataset.id);

  if (ev.target.classList.contains("btn-editar")) {
    abrirEdicion(tareas.find((t) => t.id === id));
  }

  if (ev.target.classList.contains("btn-eliminar")) {
    if (!confirm("¿Eliminar esta tarea? Esta acción no se puede deshacer.")) return;
    try {
      const r = await peticion(`${API}/${id}`, { method: "DELETE" });
      toast(r.mensaje);
      cargarTareas();
    } catch (e) {
      toast(e.message, true);
    }
  }
});

lista.addEventListener("change", async (ev) => {
  if (!ev.target.classList.contains("sel-estado")) return;
  const id = Number(ev.target.closest(".tarea").dataset.id);
  try {
    const r = await peticion(`${API}/${id}/estado`, {
      method: "PATCH",
      body: JSON.stringify({ estado: ev.target.value }),
    });
    toast(r.mensaje);
    cargarTareas();
  } catch (e) {
    toast(e.message, true);
  }
});

// ------------------------------------------------------------- RF03 Editar
function abrirEdicion(t) {
  if (!t) return;
  $("#e-id").value = t.id;
  $("#e-nombre").value = t.nombre;
  $("#e-descripcion").value = t.descripcion;
  $("#e-responsable").value = t.responsable;
  $("#e-prioridad").value = t.prioridad;
  $("#e-estado").value = t.estado;
  marcarError($("#e-nombre"), $("#error-e-nombre"), "");
  dialogo.showModal();
}

$("#btn-cancelar").addEventListener("click", () => dialogo.close());

formEditar.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const nombre = $("#e-nombre");
  if (!nombre.value.trim()) {
    marcarError(nombre, $("#error-e-nombre"), "El nombre de la tarea es obligatorio.");
    return;
  }
  const id = $("#e-id").value;
  const datos = {
    nombre: nombre.value,
    descripcion: $("#e-descripcion").value,
    responsable: $("#e-responsable").value,
    prioridad: $("#e-prioridad").value,
    estado: $("#e-estado").value,
  };
  try {
    const r = await peticion(`${API}/${id}`, { method: "PUT", body: JSON.stringify(datos) });
    toast(r.mensaje);
    dialogo.close();
    cargarTareas();
  } catch (e) {
    toast(e.message, true);
  }
});

// ------------------------------------------------------------------ filtros
$("#filtro-estado").addEventListener("change", cargarTareas);
$("#filtro-prioridad").addEventListener("change", cargarTareas);

cargarTareas();
