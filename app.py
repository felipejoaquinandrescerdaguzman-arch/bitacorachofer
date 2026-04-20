from flask import Flask, render_template_string, jsonify
import pymysql

app = Flask(__name__)

# --- CONEXIÓN A LA BASE DE DATOS (Misma que tu App) ---
def conectar_db():
    try:
        return pymysql.connect(host="gateway01.us-east-1.prod.aws.tidbcloud.com", port=4000,
                               user="2DmVGgKQsLpUtHr.root", password="iEb7Yts2tMNf8jdS",
                               database="app_bitacoras", ssl_verify_cert=True, ssl_verify_identity=True)
    except: 
        return None

# --- EL HTML DEL CHOFER (Diseño Responsivo para Celulares y Stepper Dinámico en Tiempo Real) ---
HTML_CHOFER = """
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mis Rutas - Logistic FC</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>

<body class="bg-zinc-50 text-zinc-900 antialiased selection:bg-zinc-200">

    <div class="max-w-md mx-auto min-h-screen pb-12">
        <!-- Header / Navbar -->
        <header class="bg-white px-6 py-8 border-b border-zinc-100 sticky top-0 z-20">
            <p class="text-[10px] font-semibold text-zinc-400 uppercase tracking-widest mb-1">Logística en Tiempo Real</p>
            <h1 class="text-2xl font-bold tracking-tight text-zinc-900">Mis Rutas</h1>
        </header>

        <main class="px-6 py-8">
            {% if rutas %}
            <div class="space-y-10">
                {% for ruta in rutas %}
                
                {% set estado = ruta.estado %}
                {% if estado == 'Pendiente' %}
                    {% set btn_text = 'Iniciar Ruta' %}
                    {% set w = '0%' %}
                    {% set c = ['bg-zinc-900 ring-4 ring-zinc-50 scale-125 z-10', 'bg-zinc-200', 'bg-zinc-200', 'bg-zinc-200'] %}
                {% elif estado == 'En Camino a Origen' %}
                    {% set btn_text = 'Llegué al Origen' %}
                    {% set w = '33%' %}
                    {% set c = ['bg-zinc-400', 'bg-zinc-900 ring-4 ring-zinc-50 scale-125 z-10', 'bg-zinc-200', 'bg-zinc-200'] %}
                {% elif estado == 'Cargando' %}
                    {% set btn_text = 'Carga Lista, ir a Destino' %}
                    {% set w = '66%' %}
                    {% set c = ['bg-zinc-400', 'bg-zinc-400', 'bg-zinc-900 ring-4 ring-zinc-50 scale-125 z-10', 'bg-zinc-200'] %}
                {% elif estado == 'En Camino a Destino' %}
                    {% set btn_text = 'Finalizar Ruta' %}
                    {% set w = '100%' %}
                    {% set c = ['bg-zinc-400', 'bg-zinc-400', 'bg-zinc-400', 'bg-zinc-900 ring-4 ring-zinc-50 scale-125 z-10'] %}
                {% else %}
                    {% set btn_text = 'Estado Desconocido' %}
                    {% set w = '0%' %}
                    {% set c = ['bg-zinc-200', 'bg-zinc-200', 'bg-zinc-200', 'bg-zinc-200'] %}
                {% endif %}

                <div id="ruta-{{ ruta.id }}" class="bg-white rounded-[2rem] p-8 relative border border-zinc-200 transition-all duration-500 overflow-visible">
                    
                    <div class="flex justify-between items-center mb-10">
                        <span id="badge-{{ ruta.id }}" class="text-[10px] font-bold px-3 py-1 bg-zinc-50 text-zinc-600 rounded-full uppercase tracking-widest border border-zinc-200">
                            {{ estado }}
                        </span>
                        <span class="text-zinc-400 text-[11px] font-medium tracking-wide">{{ ruta.fecha }}</span>
                    </div>

                    <!-- STEPPER TIEMPO REAL -->
                    <div class="mb-14 px-2">
                        <div class="relative flex justify-between items-center h-2">
                            <!-- Linea base -->
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full h-px bg-zinc-200"></div>
                            </div>
                            <!-- Linea activa -->
                            <div id="line-prog-{{ ruta.id }}" class="absolute inset-y-0 left-0 flex items-center transition-all duration-700 ease-[cubic-bezier(0.2,0,0,1)]" aria-hidden="true" style="width: {{ w }};">
                                <div class="w-full h-px bg-zinc-900"></div>
                            </div>
                            
                            <!-- Nodos -->
                            <div class="relative flex justify-center bg-white px-2 items-center">
                                <div id="step-1-{{ ruta.id }}" class="w-2.5 h-2.5 rounded-full transition-all duration-700 {{ c[0] }}"></div>
                                <span class="absolute top-5 text-[9px] font-medium text-zinc-400 uppercase tracking-widest">Inicio</span>
                            </div>
                            <div class="relative flex justify-center bg-white px-2 items-center">
                                <div id="step-2-{{ ruta.id }}" class="w-2.5 h-2.5 rounded-full transition-all duration-700 {{ c[1] }}"></div>
                                <span class="absolute top-5 text-[9px] font-medium text-zinc-400 uppercase tracking-widest">Origen</span>
                            </div>
                            <div class="relative flex justify-center bg-white px-2 items-center">
                                <div id="step-3-{{ ruta.id }}" class="w-2.5 h-2.5 rounded-full transition-all duration-700 {{ c[2] }}"></div>
                                <span class="absolute top-5 text-[9px] font-medium text-zinc-400 uppercase tracking-widest">Carga</span>
                            </div>
                            <div class="relative flex justify-center bg-white px-2 items-center">
                                <div id="step-4-{{ ruta.id }}" class="w-2.5 h-2.5 rounded-full transition-all duration-700 {{ c[3] }}"></div>
                                <span class="absolute top-5 text-[9px] font-medium text-zinc-400 uppercase tracking-widest">Destino</span>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-center gap-4 mb-8">
                        <div class="w-12 h-12 bg-zinc-50 rounded-full flex items-center justify-center text-lg border border-zinc-100">
                            🧑‍✈️
                        </div>
                        <div>
                            <h2 class="text-[15px] font-semibold text-zinc-900 tracking-tight leading-none mb-1.5">{{ ruta.chofer }}</h2>
                            <p class="text-xs text-zinc-500 tracking-wide font-medium">Vehículo: {{ ruta.vehiculo }}</p>
                        </div>
                    </div>

                    <div class="flex flex-col mb-10 divide-y divide-zinc-100 border-t border-b border-zinc-100 py-1">
                        <div class="flex flex-col py-4 gap-1.5">
                            <p class="text-[10px] font-medium text-zinc-400 uppercase tracking-widest leading-none">Origen</p>
                            <p class="text-sm text-zinc-900 font-medium tracking-wide leading-tight">{{ ruta.origen }}</p>
                        </div>
                        <div class="flex flex-col py-4 gap-1.5">
                            <p class="text-[10px] font-medium text-zinc-400 uppercase tracking-widest leading-none">Destino</p>
                            <p class="text-sm text-zinc-900 font-medium tracking-wide leading-tight">{{ ruta.destino }}</p>
                        </div>
                        <div class="flex flex-col py-4 gap-1.5">
                            <p class="text-[10px] font-medium text-zinc-400 uppercase tracking-widest leading-none">Centro de Costo</p>
                            <p class="text-sm text-zinc-900 font-medium tracking-wide leading-tight">{{ ruta.cc }}</p>
                        </div>
                    </div>

                    {% if ruta.descripcion %}
                    <div class="bg-zinc-50 rounded-2xl p-5 mb-10 border border-zinc-100/50">
                        <p class="text-[10px] font-medium text-zinc-400 uppercase tracking-widest mb-2.5">Detalle</p>
                        <p class="text-sm text-zinc-700 leading-relaxed font-medium">{{ ruta.descripcion }}</p>
                    </div>
                    {% endif %}

                    <!-- BOTÓN DINÁMICO MINIMALISTA -->
                    <button id="btn-{{ ruta.id }}" type="button" onclick="avanzar({{ ruta.id }}, '{{ estado }}')"
                        class="w-full bg-zinc-900 hover:bg-black active:scale-[0.98] transition-all duration-300 text-white font-medium py-4 px-6 rounded-full flex items-center justify-center gap-2 focus:outline-none focus:ring-4 focus:ring-zinc-100">
                        <span class="tracking-wide text-sm">{{ btn_text }}</span>
                    </button>
                    
                </div>
                {% endfor %}
            </div>
            {% else %}
            <!-- EMPTY STATE MINIMALISTA -->
            <div class="flex flex-col items-center justify-center py-20 px-6 text-center h-[60vh]">
                <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mb-6 border border-zinc-200">
                    <span class="text-2xl opacity-80 text-zinc-400">✓</span>
                </div>
                <h3 class="text-xl font-semibold text-zinc-900 mb-2 tracking-tight">Todo al día</h3>
                <p class="text-zinc-500 font-medium text-sm leading-relaxed max-w-xs">No tienes rutas nuevas asignadas. Tómate un descanso y te notificaremos cuando haya algo nuevo.</p>
            </div>
            {% endif %}
        </main>
    </div>

    <!-- SCRIPT DE ACTUALIZACIÓN ASÍNCRONA (TIEMPO REAL) -->
    <script>
        const conf = {
            'Pendiente': { next: 'En Camino a Origen', btnText: 'Llegué al Origen' },
            'En Camino a Origen': { next: 'Cargando', btnText: 'Carga Lista, ir a Destino' },
            'Cargando': { next: 'En Camino a Destino', btnText: 'Finalizar Ruta' },
            'En Camino a Destino': { next: 'Realizado', btnText: 'Completado' }
        };

        const stateSteps = {
            'Pendiente': { width: '0%', colors: ['bg-zinc-900 ring-4 ring-zinc-50 scale-125 z-10', 'bg-zinc-200', 'bg-zinc-200', 'bg-zinc-200'] },
            'En Camino a Origen': { width: '33%', colors: ['bg-zinc-400', 'bg-zinc-900 ring-4 ring-zinc-50 scale-125 z-10', 'bg-zinc-200', 'bg-zinc-200'] },
            'Cargando': { width: '66%', colors: ['bg-zinc-400', 'bg-zinc-400', 'bg-zinc-900 ring-4 ring-zinc-50 scale-125 z-10', 'bg-zinc-200'] },
            'En Camino a Destino': { width: '100%', colors: ['bg-zinc-400', 'bg-zinc-400', 'bg-zinc-400', 'bg-zinc-900 ring-4 ring-zinc-50 scale-125 z-10'] }
        };

        function avanzar(idRuta, estadoActual) {
            const currentStateConfig = conf[estadoActual];
            if (!currentStateConfig || !currentStateConfig.next) return;
            const nuevoEstado = currentStateConfig.next;
            
            // Estado visual de carga (Deshabilitar botón)
            const btn = document.getElementById('btn-' + idRuta);
            btn.disabled = true;
            btn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline align-middle" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-20" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-100" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg> <span class="tracking-wide text-sm">Actualizando...</span>`;
            
            // Petición en segundo plano al servidor
            fetch(`/completar/${idRuta}/${encodeURIComponent(nuevoEstado)}`, { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                if(data.success) {
                    if (nuevoEstado === 'Realizado') {
                        // Animación muy limpia de salida
                        const card = document.getElementById('ruta-' + idRuta);
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.98)';
                        setTimeout(() => {
                            card.remove();
                            // Si ya no quedan rutas, refrescamos para ver estado vacío
                            if (document.querySelectorAll('[id^=ruta-]').length === 0) {
                                window.location.reload();
                            }
                        }, 500);
                    } else {
                        // 1. Actualizar Badge (Etiqueta superior)
                        const badge = document.getElementById('badge-' + idRuta);
                        badge.innerText = nuevoEstado.toUpperCase();
                        
                        // 2. Actualizar Stepper (Barra de progreso)
                        const s = stateSteps[nuevoEstado];
                        document.getElementById('line-prog-' + idRuta).style.width = s.width;
                        
                        // 3. Colorear los Nodos (Bolitas pequeñas)
                        for (let i = 1; i <= 4; i++) {
                            const step = document.getElementById(`step-${i}-${idRuta}`);
                            step.className = `w-2.5 h-2.5 rounded-full transition-all duration-700 ${s.colors[i-1]}`;
                        }
                        
                        // 4. Actualizar Botón y Evento (Siempre Negro)
                        const nextConf = conf[nuevoEstado];
                        btn.innerHTML = `<span class="tracking-wide text-sm">${nextConf.btnText}</span>`;
                        btn.onclick = (e) => { e.preventDefault(); avanzar(idRuta, nuevoEstado); };
                        btn.disabled = false;
                    }
                } else {
                    throw new Error("Respuesta no satisfactoria");
                }
            })
            .catch(err => {
                alert("Verifica tu conexión a internet.");
                btn.disabled = false;
                btn.innerHTML = `<span class="tracking-wide text-sm">${conf[estadoActual].btnText || 'Iniciar Ruta'}</span>`;
            });
        }
    </script>
</body>
</html>
"""

# --- RUTA PRINCIPAL: Muestra la web al chofer ---
@app.route('/')
def inicio():
    con = conectar_db()
    rutas = []
    if con:
        cur = con.cursor()
        # Traemos todas las rutas que no estén terminadas para gestionar el ciclo completo
        cur.execute("SELECT id, fecha, chofer, vehiculo, origen, destino, centro_costos, descripcion, estado FROM bitacoras WHERE estado IN ('Pendiente', 'En Camino a Origen', 'Cargando', 'En Camino a Destino') ORDER BY id DESC")
        for row in cur.fetchall():
            rutas.append({
                "id": row[0], "fecha": row[1], "chofer": row[2],
                "vehiculo": row[3], "origen": row[4], "destino": row[5],
                "cc": row[6], "descripcion": row[7], "estado": row[8]
            })
        con.close()
    return render_template_string(HTML_CHOFER, rutas=rutas)

# --- ACCIÓN: Cambiar estado secuencial en la base de datos (AJAX) ---
@app.route('/completar/<int:id_ruta>/<string:nuevo_estado>', methods=['POST'])
def avanzar_estado(id_ruta, nuevo_estado):
    con = conectar_db()
    if con:
        cur = con.cursor()
        # Recibimos el estado dinámicamente y lo actualizamos en la nube
        cur.execute("UPDATE bitacoras SET estado=%s WHERE id=%s", (nuevo_estado, id_ruta))
        con.commit()
        con.close()
        return jsonify({"success": True, "estado": nuevo_estado})
    return jsonify({"success": False, "error": "Sin conexión a base de datos"}), 500

# --- INICIAR SERVIDOR ---
if __name__ == '__main__':
    # host='0.0.0.0' permite que se acceda desde celulares en la red
    app.run(debug=True, host='0.0.0.0', port=5000)
