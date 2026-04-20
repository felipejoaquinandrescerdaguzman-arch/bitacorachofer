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
    <title>Mis Rutas - Logistic F.C.</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>

<body class="bg-slate-50 text-slate-800 antialiased selection:bg-blue-200">

    <div class="max-w-md mx-auto min-h-screen pb-8">
        <!-- Header / Navbar -->
        <header class="bg-gradient-to-r from-blue-700 to-blue-900 text-white p-5 text-center sticky top-0 shadow-[0_4px_20px_-5px_rgba(0,0,0,0.3)] rounded-b-2xl z-20 relative border-b border-blue-900/50">
            <h1 class="text-2xl font-extrabold tracking-tight">🚛 Mis Rutas</h1>
            <p class="text-sm text-blue-100 mt-1 font-medium opacity-90 tracking-wide">Logistic F.C. • En Ruta</p>
        </header>

        <main class="px-4 pt-6">
            {% if rutas %}
            <div class="space-y-6">
                {% for ruta in rutas %}
                
                {% set estado = ruta.estado %}
                {% if estado == 'Pendiente' %}
                    {% set btn_color = 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500' %}
                    {% set btn_text = 'INICIAR RUTA' %}
                    {% set w = '0%' %}{% set bd_col = 'border-blue-600' %}
                    {% set badge_col = 'bg-blue-100 text-blue-800' %}
                    {% set c = ['bg-blue-600 text-white', 'bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400'] %}
                {% elif estado == 'En Camino a Origen' %}
                    {% set btn_color = 'bg-orange-500 hover:bg-orange-600 focus:ring-orange-500' %}
                    {% set btn_text = 'LLEGUÉ AL ORIGEN' %}
                    {% set w = '33%' %}{% set bd_col = 'border-orange-500' %}
                    {% set badge_col = 'bg-orange-100 text-orange-800' %}
                    {% set c = ['bg-orange-500 text-white', 'bg-orange-500 text-white', 'bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400'] %}
                {% elif estado == 'Cargando' %}
                    {% set btn_color = 'bg-purple-600 hover:bg-purple-700 focus:ring-purple-500' %}
                    {% set btn_text = 'CARGA LISTA, IR A DESTINO' %}
                    {% set w = '66%' %}{% set bd_col = 'border-purple-600' %}
                    {% set badge_col = 'bg-purple-100 text-purple-800' %}
                    {% set c = ['bg-purple-600 text-white', 'bg-purple-600 text-white', 'bg-purple-600 text-white', 'bg-slate-200 text-slate-400'] %}
                {% elif estado == 'En Camino a Destino' %}
                    {% set btn_color = 'bg-emerald-500 hover:bg-emerald-600 focus:ring-emerald-500' %}
                    {% set btn_text = 'FINALIZAR RUTA' %}
                    {% set w = '100%' %}{% set bd_col = 'border-emerald-500' %}
                    {% set badge_col = 'bg-emerald-100 text-emerald-800' %}
                    {% set c = ['bg-emerald-500 text-white', 'bg-emerald-500 text-white', 'bg-emerald-500 text-white', 'bg-emerald-500 text-white'] %}
                {% else %}
                    {% set btn_color = 'bg-slate-500 hover:bg-slate-600 focus:ring-slate-500' %}
                    {% set btn_text = 'ESTADO DESCONOCIDO' %}
                    {% set w = '0%' %}{% set bd_col = 'border-slate-500' %}
                    {% set badge_col = 'bg-slate-100 text-slate-800' %}
                    {% set c = ['bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400'] %}
                {% endif %}

                <div id="ruta-{{ ruta.id }}" class="bg-white rounded-[1.25rem] shadow-sm hover:shadow-lg transition-all duration-300 p-5 relative border border-slate-100/80 mb-6 overflow-visible">
                    
                    <div class="flex justify-between items-center mb-6 border-b border-slate-100 pb-3.5">
                        <span id="badge-{{ ruta.id }}" class="text-[11px] font-black px-3.5 py-1.5 rounded-full uppercase tracking-widest {{ badge_col }} transition-colors duration-300 shadow-sm">
                            {{ estado }}
                        </span>
                        <span class="text-slate-400 text-xs font-semibold flex items-center gap-1.5 bg-slate-50 px-2 py-1 rounded-md">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3.5 h-3.5">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {{ ruta.fecha }}
                        </span>
                    </div>

                    <!-- STEPPER TIEMPO REAL -->
                    <div class="mx-2 mb-10 mt-2">
                        <div class="relative flex justify-between">
                            <!-- Lines -->
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t-[3px] border-slate-200/80"></div>
                            </div>
                            <div id="line-prog-{{ ruta.id }}" class="absolute inset-0 flex items-center transition-all duration-500 ease-in-out" aria-hidden="true" style="width: {{ w }};">
                                <div id="prog-bar-{{ ruta.id }}" class="w-full border-t-[3px] {{ bd_col }} transition-colors duration-500"></div>
                            </div>
                            
                            <!-- Nodes -->
                            <div class="relative flex justify-center bg-white rounded-full">
                                <div id="step-1-{{ ruta.id }}" class="w-8 h-8 rounded-full flex items-center justify-center border-[3px] border-white text-xs font-black transition-all duration-500 {{ c[0] }} shadow-sm">1</div>
                                <span class="absolute -bottom-6 text-[9px] font-extrabold text-slate-400 uppercase tracking-widest">Inicio</span>
                            </div>
                            <div class="relative flex justify-center bg-white rounded-full">
                                <div id="step-2-{{ ruta.id }}" class="w-8 h-8 rounded-full flex items-center justify-center border-[3px] border-white text-xs font-black transition-all duration-500 {{ c[1] }} shadow-sm">2</div>
                                <span class="absolute -bottom-6 text-[9px] font-extrabold text-slate-400 uppercase tracking-widest">Origen</span>
                            </div>
                            <div class="relative flex justify-center bg-white rounded-full">
                                <div id="step-3-{{ ruta.id }}" class="w-8 h-8 rounded-full flex items-center justify-center border-[3px] border-white text-xs font-black transition-all duration-500 {{ c[2] }} shadow-sm">3</div>
                                <span class="absolute -bottom-6 text-[9px] font-extrabold text-slate-400 uppercase tracking-widest">Carga</span>
                            </div>
                            <div class="relative flex justify-center bg-white rounded-full">
                                <div id="step-4-{{ ruta.id }}" class="w-8 h-8 rounded-full flex items-center justify-center border-[3px] border-white text-xs font-black transition-all duration-500 {{ c[3] }} shadow-sm">4</div>
                                <span class="absolute -bottom-6 text-[9px] font-extrabold text-slate-400 uppercase tracking-widest">Destino</span>
                            </div>
                        </div>
                    </div>

                    <div class="mb-5 bg-gradient-to-r from-slate-50 to-white p-4 rounded-xl border border-slate-100 shadow-inner">
                        <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2 mb-2">
                            <span class="text-xl">🧑‍✈️</span> {{ ruta.chofer }}
                        </h2>
                        <p class="text-sm font-semibold text-slate-600 flex items-center gap-2">
                            <span class="text-base text-slate-400 opacity-80">🚚</span> <span>{{ ruta.vehiculo }}</span>
                        </p>
                    </div>

                    <div class="space-y-4 mb-6 px-1">
                        <div class="flex items-start gap-4">
                            <div class="mt-0.5 text-blue-600 bg-blue-100/50 p-2 rounded-xl shadow-sm border border-blue-50">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                                </svg>
                            </div>
                            <div class="flex-1">
                                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Origen</p>
                                <p class="text-[15px] text-slate-800 font-bold leading-tight">{{ ruta.origen }}</p>
                            </div>
                        </div>

                        <div class="flex items-start gap-4">
                            <div class="mt-0.5 text-emerald-600 bg-emerald-100/50 p-2 rounded-xl shadow-sm border border-emerald-50">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>                                
                            </div>
                            <div class="flex-1">
                                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Destino</p>
                                <p class="text-[15px] text-slate-800 font-bold leading-tight">{{ ruta.destino }}</p>
                            </div>
                        </div>

                        <div class="flex items-start gap-4">
                            <div class="mt-0.5 text-indigo-600 bg-indigo-100/50 p-2 rounded-xl shadow-sm border border-indigo-50">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" />
                                </svg>
                            </div>
                            <div class="flex-1">
                                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Centro de Costo</p>
                                <p class="text-[15px] text-slate-800 font-bold leading-tight">{{ ruta.cc }}</p>
                            </div>
                        </div>
                    </div>

                    {% if ruta.descripcion %}
                    <div class="bg-gradient-to-br from-blue-50 to-blue-100/50 p-4 rounded-xl border border-blue-100/80 mb-6 relative overflow-hidden shadow-inner">
                        <div class="absolute top-0 right-0 p-2 opacity-10">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-16 h-16 text-blue-900">
                                <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm8.706-1.442c1.146-.573 2.437.463 2.126 1.706l-.709 2.836.042-.02a.75.75 0 01.67 1.34l-.04.022c-1.147.573-2.438-.463-2.127-1.706l.71-2.836-.042.02a.75.75 0 11-.671-1.34l.041-.022zM12 9a.75.75 0 100-1.5.75.75 0 000 1.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <div class="flex items-center gap-2 mb-2 relative z-10">
                            <p class="text-[11px] font-black text-blue-700 uppercase tracking-widest">Detalle de la ruta</p>
                        </div>
                        <p class="text-sm text-slate-700 leading-relaxed font-semibold relative z-10">{{ ruta.descripcion }}</p>
                    </div>
                    {% endif %}

                    <!-- BOTÓN DINÁMICO (Call To Action) -->
                    <button id="btn-{{ ruta.id }}" type="button" onclick="avanzar({{ ruta.id }}, '{{ estado }}')"
                        class="w-full {{ btn_color }} active:scale-95 active:shadow-inner transition-all duration-300 text-white font-black py-4 px-4 rounded-2xl shadow-[0_4px_14px_0_rgba(0,0,0,0.1)] flex items-center justify-center gap-2 focus:outline-none focus:ring-4 focus:ring-offset-2">
                        <span class="tracking-wide text-lg uppercase">{{ btn_text }}</span>
                    </button>
                    
                </div>
                {% endfor %}
            </div>
            {% else %}
            <!-- EMPTY STATE -->
            <div class="flex flex-col items-center justify-center py-16 px-4 text-center h-[60vh]">
                <div class="text-[5.5rem] mb-6 drop-shadow-xl animate-[bounce_3s_infinite]">🎉</div>
                <h3 class="text-3xl font-black text-slate-800 mb-3 tracking-tight">¡Todo al día!</h3>
                <p class="text-slate-500 font-medium text-[15px]">No tienes rutas asignadas en este momento.</p>
                <div class="mt-10 p-5 bg-white rounded-2xl shadow-sm border border-slate-100 flex items-center gap-5 w-full">
                    <span class="text-4xl bg-orange-50 p-3 rounded-2xl">☕</span>
                    <p class="text-sm text-slate-600 font-bold text-left leading-relaxed">Es un excelente momento para estacionar y tomar un descanso.</p>
                </div>
            </div>
            {% endif %}
        </main>
    </div>

    <!-- SCRIPT DE ACTUALIZACIÓN ASÍNCRONA (TIEMPO REAL) -->
    <script>
        const conf = {
            'Pendiente': { next: 'En Camino a Origen', btnText: 'LLEGUÉ AL ORIGEN', btnColor: 'bg-orange-500 hover:bg-orange-600 focus:ring-orange-500' },
            'En Camino a Origen': { next: 'Cargando', btnText: 'CARGA LISTA, IR A DESTINO', btnColor: 'bg-purple-600 hover:bg-purple-700 focus:ring-purple-500' },
            'Cargando': { next: 'En Camino a Destino', btnText: 'FINALIZAR RUTA', btnColor: 'bg-emerald-500 hover:bg-emerald-600 focus:ring-emerald-500' },
            'En Camino a Destino': { next: 'Realizado', btnText: 'COMPLETADO', btnColor: 'bg-slate-500' }
        };

        const stateSteps = {
            'Pendiente': { width: '0%', colors: ['bg-blue-600 text-white', 'bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400'], barColor: 'border-blue-600', badgeColor: 'bg-blue-100 text-blue-800' },
            'En Camino a Origen': { width: '33%', colors: ['bg-orange-500 text-white', 'bg-orange-500 text-white', 'bg-slate-200 text-slate-400', 'bg-slate-200 text-slate-400'], barColor: 'border-orange-500', badgeColor: 'bg-orange-100 text-orange-800' },
            'Cargando': { width: '66%', colors: ['bg-purple-600 text-white', 'bg-purple-600 text-white', 'bg-purple-600 text-white', 'bg-slate-200 text-slate-400'], barColor: 'border-purple-600', badgeColor: 'bg-purple-100 text-purple-800' },
            'En Camino a Destino': { width: '100%', colors: ['bg-emerald-500 text-white', 'bg-emerald-500 text-white', 'bg-emerald-500 text-white', 'bg-emerald-500 text-white'], barColor: 'border-emerald-500', badgeColor: 'bg-emerald-100 text-emerald-800' }
        };

        function avanzar(idRuta, estadoActual) {
            const currentStateConfig = conf[estadoActual];
            if (!currentStateConfig || !currentStateConfig.next) return;
            const nuevoEstado = currentStateConfig.next;
            
            // Estado visual de carga (Deshabilitar botón)
            const btn = document.getElementById('btn-' + idRuta);
            btn.disabled = true;
            btn.innerHTML = `<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline max-w-fit align-middle" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-30" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-100" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg> <span class="tracking-wide text-lg uppercase font-black">ACTUALIZANDO...</span>`;
            
            // Petición en segundo plano al servidor
            fetch(`/completar/${idRuta}/${encodeURIComponent(nuevoEstado)}`, { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                if(data.success) {
                    if (nuevoEstado === 'Realizado') {
                        // Animación elegante de salida y remoción
                        const card = document.getElementById('ruta-' + idRuta);
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.9) translateY(20px)';
                        setTimeout(() => {
                            card.remove();
                            // Si ya no quedan rutas, refrescamos para ver la pantalla vacía
                            if (document.querySelectorAll('[id^=ruta-]').length === 0) {
                                window.location.reload();
                            }
                        }, 400);
                    } else {
                        // 1. Actualizar Badge (Etiqueta superior)
                        const badge = document.getElementById('badge-' + idRuta);
                        badge.innerText = nuevoEstado.toUpperCase();
                        badge.className = `text-[11px] font-black px-3.5 py-1.5 rounded-full uppercase tracking-widest transition-colors duration-300 shadow-sm ${stateSteps[nuevoEstado].badgeColor}`;
                        
                        // 2. Actualizar Stepper (Barra de progreso)
                        const s = stateSteps[nuevoEstado];
                        document.getElementById('line-prog-' + idRuta).style.width = s.width;
                        document.getElementById('prog-bar-' + idRuta).className = `w-full border-t-[3px] transition-colors duration-500 ${s.barColor}`;
                        
                        // 3. Colorear los Nodos (Bolas)
                        for (let i = 1; i <= 4; i++) {
                            const step = document.getElementById(`step-${i}-${idRuta}`);
                            step.className = `w-8 h-8 rounded-full flex items-center justify-center border-[3px] border-white text-xs font-black transition-all duration-500 shadow-sm ${s.colors[i-1]}`;
                        }
                        
                        // 4. Actualizar Botón y Evento
                        const nextConf = conf[nuevoEstado];
                        btn.className = `w-full transition-all duration-300 active:scale-95 active:shadow-inner text-white font-black py-4 px-4 rounded-2xl shadow-[0_4px_14px_0_rgba(0,0,0,0.1)] flex items-center justify-center gap-2 focus:outline-none focus:ring-4 focus:ring-offset-2 ${nextConf.btnColor}`;
                        btn.innerHTML = `<span class="tracking-wide text-lg uppercase">${nextConf.btnText}</span>`;
                        btn.onclick = (e) => { e.preventDefault(); avanzar(idRuta, nuevoEstado); };
                        btn.disabled = false;
                    }
                } else {
                    throw new Error("Respuesta no satisfactoria del servidor");
                }
            })
            .catch(err => {
                alert("Hubo un problema de conexión. Inténtalo nuevamente.");
                btn.disabled = false;
                // Restaurar texto original al fallar
                btn.innerHTML = `<span class="tracking-wide text-lg uppercase">${conf[estadoActual].btnText || 'INICIAR RUTA'}</span>`;
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
