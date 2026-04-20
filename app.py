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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>

<body class="bg-gradient-to-br from-blue-50 via-white to-purple-50 text-slate-800 antialiased selection:bg-indigo-200 min-h-screen">

    <div class="max-w-md mx-auto min-h-screen pb-12">
        <!-- Header / Navbar -->
        <header class="pt-10 pb-6 px-6 text-center sticky top-0 z-20 bg-gradient-to-b from-white/90 to-white/0 backdrop-blur-md">
            <div class="inline-block bg-white/60 px-4 py-1.5 rounded-full border border-white/80 shadow-sm backdrop-blur-md mb-2">
                <p class="text-[11px] font-bold text-blue-700 uppercase tracking-widest bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">Logistic F.C.</p>
            </div>
            <h1 class="text-[28px] font-extrabold tracking-tight text-slate-900 leading-none drop-shadow-sm">Mis Rutas</h1>
        </header>

        <main class="px-6 py-6">
            {% if rutas %}
            <div class="space-y-10">
                {% for ruta in rutas %}
                
                {% set estado = ruta.estado %}
                {% if estado == 'Pendiente' %}
                    {% set btn_text = 'Iniciar Ruta' %}
                    {% set w = '0%' %}
                    {% set btn_class = 'bg-gradient-to-r from-amber-500 to-orange-500 shadow-orange-500/30' %}
                    {% set line_class = 'bg-orange-500' %}
                    {% set badge_class = 'bg-orange-100 text-orange-700 border border-orange-200/50 shadow-orange-100/50' %}
                    
                    {% set c1 = 'bg-orange-500 ring-4 ring-orange-100 ring-offset-2 ring-offset-white/80 scale-110' %}{% set i1 = 'opacity-0' %}
                    {% set c2 = 'bg-slate-200' %}{% set i2 = 'opacity-0' %}
                    {% set c3 = 'bg-slate-200' %}{% set i3 = 'opacity-0' %}
                    {% set c4 = 'bg-slate-200' %}{% set i4 = 'opacity-0' %}
                    
                {% elif estado == 'En Camino a Origen' %}
                    {% set btn_text = 'Llegué al Origen' %}
                    {% set w = '33%' %}
                    {% set btn_class = 'bg-gradient-to-r from-blue-500 to-indigo-500 shadow-blue-500/30' %}
                    {% set line_class = 'bg-blue-500' %}
                    {% set badge_class = 'bg-blue-100 text-blue-700 border border-blue-200/50 shadow-blue-100/50' %}
                    
                    {% set c1 = 'bg-blue-500' %}{% set i1 = 'opacity-100' %}
                    {% set c2 = 'bg-blue-500 ring-4 ring-blue-100 ring-offset-2 ring-offset-white/80 scale-110' %}{% set i2 = 'opacity-0' %}
                    {% set c3 = 'bg-slate-200' %}{% set i3 = 'opacity-0' %}
                    {% set c4 = 'bg-slate-200' %}{% set i4 = 'opacity-0' %}
                    
                {% elif estado == 'Cargando' %}
                    {% set btn_text = 'Carga Lista, ir a Destino' %}
                    {% set w = '66%' %}
                    {% set btn_class = 'bg-gradient-to-r from-indigo-400 to-purple-500 shadow-indigo-500/30' %}
                    {% set line_class = 'bg-indigo-500' %}
                    {% set badge_class = 'bg-indigo-100 text-indigo-700 border border-indigo-200/50 shadow-indigo-100/50' %}
                    
                    {% set c1 = 'bg-indigo-500' %}{% set i1 = 'opacity-100' %}
                    {% set c2 = 'bg-indigo-500' %}{% set i2 = 'opacity-100' %}
                    {% set c3 = 'bg-indigo-500 ring-4 ring-indigo-100 ring-offset-2 ring-offset-white/80 scale-110' %}{% set i3 = 'opacity-0' %}
                    {% set c4 = 'bg-slate-200' %}{% set i4 = 'opacity-0' %}
                    
                {% elif estado == 'En Camino a Destino' %}
                    {% set btn_text = 'Finalizar Ruta' %}
                    {% set w = '100%' %}
                    {% set btn_class = 'bg-gradient-to-r from-emerald-400 to-teal-500 shadow-emerald-500/30' %}
                    {% set line_class = 'bg-emerald-500' %}
                    {% set badge_class = 'bg-emerald-100 text-emerald-700 border border-emerald-200/50 shadow-emerald-100/50' %}
                    
                    {% set c1 = 'bg-emerald-500' %}{% set i1 = 'opacity-100' %}
                    {% set c2 = 'bg-emerald-500' %}{% set i2 = 'opacity-100' %}
                    {% set c3 = 'bg-emerald-500' %}{% set i3 = 'opacity-100' %}
                    {% set c4 = 'bg-emerald-500 ring-4 ring-emerald-100 ring-offset-2 ring-offset-white/80 scale-110' %}{% set i4 = 'opacity-0' %}
                {% else %}
                    {% set btn_text = 'Estado Desconocido' %}
                    {% set w = '0%' %}
                    {% set btn_class = 'bg-slate-400 text-slate-100' %}
                    {% set line_class = 'bg-slate-300' %}
                    {% set badge_class = 'bg-slate-100 text-slate-500' %}
                    {% set c1 = 'bg-slate-200' %}{% set i1 = 'opacity-0' %}{% set c2 = 'bg-slate-200' %}{% set i2 = 'opacity-0' %}
                    {% set c3 = 'bg-slate-200' %}{% set i3 = 'opacity-0' %}{% set c4 = 'bg-slate-200' %}{% set i4 = 'opacity-0' %}
                {% endif %}

                <div id="ruta-{{ ruta.id }}" class="bg-white/80 backdrop-blur-xl rounded-[2.5rem] p-8 relative border border-white shadow-xl shadow-blue-100/40 transition-all duration-500 overflow-visible">
                    
                    <div class="flex justify-between items-center mb-10">
                        <span id="badge-{{ ruta.id }}" class="text-[10px] font-extrabold px-4 py-1.5 rounded-full uppercase tracking-widest transition-colors duration-300 shadow-sm {{ badge_class }}">
                            {{ estado }}
                        </span>
                        <span class="text-slate-400 text-[11px] font-semibold tracking-wide bg-white/60 px-2 py-1 rounded-md">{{ ruta.fecha }}</span>
                    </div>

                    <!-- STEPPER COLORIDO Y DINÁMICO -->
                    <div class="mb-14 px-1 mt-4">
                        <div class="relative flex justify-between items-center h-2">
                            <!-- Linea base -->
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full h-1.5 bg-slate-100 rounded-full"></div>
                            </div>
                            <!-- Linea activa -->
                            <div id="line-prog-{{ ruta.id }}" class="absolute inset-y-0 left-0 flex items-center transition-all duration-700 ease-[cubic-bezier(0.2,0,0,1)]" aria-hidden="true" style="width: {{ w }};">
                                <div id="prog-bar-{{ ruta.id }}" class="w-full h-1.5 rounded-full transition-colors duration-500 shadow-sm {{ line_class }}"></div>
                            </div>
                            
                            <!-- Nodos -->
                            <div class="relative flex justify-center items-center z-10 bg-transparent px-1">
                                <div id="step-1-{{ ruta.id }}" class="w-7 h-7 rounded-full flex items-center justify-center transition-all duration-700 {{ c1 }}">
                                    <svg id="chk-1-{{ ruta.id }}" class="w-3.5 h-3.5 text-white transition-opacity duration-300 {{ i1 }}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                    </svg>
                                </div>
                                <span class="absolute top-9 text-[9px] font-bold text-slate-400 uppercase tracking-widest whitespace-nowrap">Inicio</span>
                            </div>
                            <div class="relative flex justify-center items-center z-10 bg-transparent px-1">
                                <div id="step-2-{{ ruta.id }}" class="w-7 h-7 rounded-full flex items-center justify-center transition-all duration-700 {{ c2 }}">
                                    <svg id="chk-2-{{ ruta.id }}" class="w-3.5 h-3.5 text-white transition-opacity duration-300 {{ i2 }}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                    </svg>
                                </div>
                                <span class="absolute top-9 text-[9px] font-bold text-slate-400 uppercase tracking-widest whitespace-nowrap">Origen</span>
                            </div>
                            <div class="relative flex justify-center items-center z-10 bg-transparent px-1">
                                <div id="step-3-{{ ruta.id }}" class="w-7 h-7 rounded-full flex items-center justify-center transition-all duration-700 {{ c3 }}">
                                    <svg id="chk-3-{{ ruta.id }}" class="w-3.5 h-3.5 text-white transition-opacity duration-300 {{ i3 }}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                    </svg>
                                </div>
                                <span class="absolute top-9 text-[9px] font-bold text-slate-400 uppercase tracking-widest whitespace-nowrap">Carga</span>
                            </div>
                            <div class="relative flex justify-center items-center z-10 bg-transparent px-1">
                                <div id="step-4-{{ ruta.id }}" class="w-7 h-7 rounded-full flex items-center justify-center transition-all duration-700 {{ c4 }}">
                                    <svg id="chk-4-{{ ruta.id }}" class="w-3.5 h-3.5 text-white transition-opacity duration-300 {{ i4 }}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                    </svg>
                                </div>
                                <span class="absolute top-9 text-[9px] font-bold text-slate-400 uppercase tracking-widest whitespace-nowrap">Destino</span>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-center gap-4 mb-8 bg-blue-50/40 p-4 rounded-full border border-blue-100/50 backdrop-blur-sm shadow-sm opacity-90 mx-1">
                        <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center text-xl shadow-sm border border-blue-100">
                            👨‍✈️
                        </div>
                        <div>
                            <h2 class="text-[15px] font-bold text-slate-900 tracking-tight leading-none mb-1">{{ ruta.chofer }}</h2>
                            <p class="text-xs font-semibold text-blue-600 tracking-wide">Vehículo: {{ ruta.vehiculo }}</p>
                        </div>
                    </div>

                    <div class="flex flex-col gap-3 mb-10 w-full">
                        <!-- Origen -->
                        <div class="flex items-center gap-4 bg-orange-50/50 p-4 rounded-3xl border border-orange-100/50 hover:bg-orange-50 transition-colors">
                            <div class="w-12 h-12 bg-orange-100/70 text-orange-600 rounded-2xl flex items-center justify-center shrink-0 shadow-sm border border-orange-200/30">
                                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                            </div>
                            <div class="flex-1">
                                 <p class="text-[10px] font-extrabold text-orange-500 uppercase tracking-widest mb-1">Origen</p>
                                 <p class="text-sm font-bold text-slate-800 leading-tight">{{ ruta.origen }}</p>
                            </div>
                        </div>
                        <!-- Destino -->
                        <div class="flex items-center gap-4 bg-emerald-50/60 p-4 rounded-3xl border border-emerald-100/50 hover:bg-emerald-50 transition-colors">
                            <div class="w-12 h-12 bg-emerald-100/70 text-emerald-600 rounded-2xl flex items-center justify-center shrink-0 shadow-sm border border-emerald-200/30">
                                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                            </div>
                            <div class="flex-1">
                                 <p class="text-[10px] font-extrabold text-emerald-500 uppercase tracking-widest mb-1">Destino</p>
                                 <p class="text-sm font-bold text-slate-800 leading-tight">{{ ruta.destino }}</p>
                            </div>
                        </div>
                        <!-- Centro de Costo -->
                        <div class="flex items-center gap-4 bg-indigo-50/60 p-4 rounded-3xl border border-indigo-100/50 hover:bg-indigo-50 transition-colors">
                            <div class="w-12 h-12 bg-indigo-100/70 text-indigo-600 rounded-2xl flex items-center justify-center shrink-0 shadow-sm border border-indigo-200/30">
                                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                                </svg>
                            </div>
                            <div class="flex-1">
                                 <p class="text-[10px] font-extrabold text-indigo-500 uppercase tracking-widest mb-1">Centro de Costo</p>
                                 <p class="text-sm font-bold text-slate-800 leading-tight">{{ ruta.cc }}</p>
                            </div>
                        </div>
                    </div>

                    {% if ruta.descripcion %}
                    <div class="bg-gradient-to-br from-indigo-50 to-blue-50/30 rounded-3xl p-6 mb-10 border border-indigo-100/60 shadow-inner">
                        <div class="flex items-center gap-2 mb-3">
                            <span class="w-6 h-6 bg-indigo-100/80 text-indigo-600 flex items-center justify-center rounded-full">
                                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            </span>
                            <p class="text-[10px] font-extrabold text-indigo-600 uppercase tracking-widest">Notas Adicionales</p>
                        </div>
                        <p class="text-sm text-slate-700 leading-relaxed font-semibold">{{ ruta.descripcion }}</p>
                    </div>
                    {% endif %}

                    <!-- BOTÓN DINÁMICO STARTUP -->
                    <button id="btn-{{ ruta.id }}" type="button" onclick="avanzar({{ ruta.id }}, '{{ estado }}')"
                        class="w-full text-white font-extrabold py-5 px-6 rounded-full flex items-center justify-center gap-2 focus:outline-none hover:shadow-xl hover:-translate-y-1 transition-all duration-300 active:scale-[0.98] shadow-lg {{ btn_class }}">
                        <span class="tracking-wide text-[15px] drop-shadow-sm uppercase">{{ btn_text }}</span>
                    </button>
                    
                </div>
                {% endfor %}
            </div>
            {% else %}
            <!-- EMPTY STATE MODERNO Y AMIGABLE -->
            <div class="flex flex-col items-center justify-center py-20 px-6 text-center h-[60vh] mt-4">
                <div class="w-24 h-24 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-full flex items-center justify-center mb-8 border-4 border-white shadow-xl shadow-emerald-200/40 relative">
                    <span class="text-4xl animate-bounce">✨</span>
                    <div class="absolute inset-0 rounded-full ring-4 ring-emerald-50 scale-110"></div>
                </div>
                <h3 class="text-[28px] font-extrabold pb-2 bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 to-teal-500 tracking-tight">Todo está listo</h3>
                <p class="text-slate-500/80 font-semibold text-[15px] leading-relaxed max-w-[280px]">No tienes rutas nuevas asignadas. Tómate un café ☕ mientras esperamos novedades.</p>
            </div>
            {% endif %}
        </main>
    </div>

    <!-- SCRIPT DE ACTUALIZACIÓN ASÍNCRONA (TIEMPO REAL) -->
    <script>
        const conf = {
            'Pendiente': { next: 'En Camino a Origen', btnText: 'Llegué al Origen', btnClass: 'bg-gradient-to-r from-blue-500 to-indigo-500 shadow-blue-500/30' },
            'En Camino a Origen': { next: 'Cargando', btnText: 'Carga Lista', btnClass: 'bg-gradient-to-r from-indigo-400 to-purple-500 shadow-indigo-500/30' },
            'Cargando': { next: 'En Camino a Destino', btnText: 'Finalizar Ruta', btnClass: 'bg-gradient-to-r from-emerald-400 to-teal-500 shadow-emerald-500/30' },
            'En Camino a Destino': { next: 'Realizado', btnText: 'Completado', btnClass: 'bg-slate-300 text-slate-500 shadow-none' }
        };

        const stateSteps = {
            'Pendiente': { 
                width: '0%', line: 'bg-orange-500', badge: 'bg-orange-100 text-orange-700 border border-orange-200/50 shadow-orange-100/50',
                colors: ['bg-orange-500 ring-4 ring-orange-100 ring-offset-2 ring-offset-white/80 scale-110', 'bg-slate-200', 'bg-slate-200', 'bg-slate-200'],
                icons: ['opacity-0', 'opacity-0', 'opacity-0', 'opacity-0']
            },
            'En Camino a Origen': { 
                width: '33%', line: 'bg-blue-500', badge: 'bg-blue-100 text-blue-700 border border-blue-200/50 shadow-blue-100/50',
                colors: ['bg-blue-500', 'bg-blue-500 ring-4 ring-blue-100 ring-offset-2 ring-offset-white/80 scale-110', 'bg-slate-200', 'bg-slate-200'],
                icons: ['opacity-100', 'opacity-0', 'opacity-0', 'opacity-0']
            },
            'Cargando': { 
                width: '66%', line: 'bg-indigo-500', badge: 'bg-indigo-100 text-indigo-700 border border-indigo-200/50 shadow-indigo-100/50',
                colors: ['bg-indigo-500', 'bg-indigo-500', 'bg-indigo-500 ring-4 ring-indigo-100 ring-offset-2 ring-offset-white/80 scale-110', 'bg-slate-200'],
                icons: ['opacity-100', 'opacity-100', 'opacity-0', 'opacity-0']
            },
            'En Camino a Destino': { 
                width: '100%', line: 'bg-emerald-500', badge: 'bg-emerald-100 text-emerald-700 border border-emerald-200/50 shadow-emerald-100/50',
                colors: ['bg-emerald-500', 'bg-emerald-500', 'bg-emerald-500', 'bg-emerald-500 ring-4 ring-emerald-100 ring-offset-2 ring-offset-white/80 scale-110'],
                icons: ['opacity-100', 'opacity-100', 'opacity-100', 'opacity-0']
            }
        };

        function avanzar(idRuta, estadoActual) {
            const currentStateConfig = conf[estadoActual];
            if (!currentStateConfig || !currentStateConfig.next) return;
            const nuevoEstado = currentStateConfig.next;
            
            // Estado visual de carga
            const btn = document.getElementById('btn-' + idRuta);
            btn.disabled = true;
            btn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-current inline align-middle" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg> <span class="tracking-wide text-[15px] drop-shadow-sm uppercase">PROCESANDO...</span>`;
            
            fetch(`/completar/${idRuta}/${encodeURIComponent(nuevoEstado)}`, { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                if(data.success) {
                    if (nuevoEstado === 'Realizado') {
                        // Salida elegante
                        const card = document.getElementById('ruta-' + idRuta);
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            card.remove();
                            if (document.querySelectorAll('[id^=ruta-]').length === 0) {
                                window.location.reload();
                            }
                        }, 500);
                    } else {
                        // 1. Badge
                        const badge = document.getElementById('badge-' + idRuta);
                        badge.innerText = nuevoEstado.toUpperCase();
                        const s = stateSteps[nuevoEstado];
                        badge.className = `text-[10px] font-extrabold px-4 py-1.5 rounded-full uppercase tracking-widest transition-colors duration-300 shadow-sm ${s.badge}`;
                        
                        // 2. Stepper
                        document.getElementById('line-prog-' + idRuta).style.width = s.width;
                        document.getElementById('prog-bar-' + idRuta).className = `w-full h-1.5 rounded-full transition-colors duration-500 shadow-sm ${s.line}`;
                        
                        // 3. Nodos e Íconos
                        for (let i = 1; i <= 4; i++) {
                            const step = document.getElementById(`step-${i}-${idRuta}`);
                            step.className = `w-7 h-7 rounded-full flex items-center justify-center transition-all duration-700 ${s.colors[i-1]}`;
                            const chk = document.getElementById(`chk-${i}-${idRuta}`);
                            chk.className = `w-3.5 h-3.5 text-white transition-opacity duration-300 ${s.icons[i-1]}`;
                        }
                        
                        // 4. Botón
                        const nextConf = conf[nuevoEstado];
                        btn.className = `w-full text-white font-extrabold py-5 px-6 rounded-full flex items-center justify-center gap-2 focus:outline-none hover:shadow-xl hover:-translate-y-1 transition-all duration-300 active:scale-[0.98] shadow-lg ${nextConf.btnClass}`;
                        btn.innerHTML = `<span class="tracking-wide text-[15px] drop-shadow-sm uppercase">${nextConf.btnText}</span>`;
                        btn.onclick = (e) => { e.preventDefault(); avanzar(idRuta, nuevoEstado); };
                        btn.disabled = false;
                    }
                } else {
                    throw new Error("Error del servidor");
                }
            })
            .catch(err => {
                alert("Error de red. Intenta nuevamente.");
                btn.disabled = false;
                btn.innerHTML = `<span class="tracking-wide text-[15px] drop-shadow-sm uppercase">${conf[estadoActual].btnText || 'Iniciar Ruta'}</span>`;
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
