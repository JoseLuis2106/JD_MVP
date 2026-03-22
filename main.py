import flet as ft
import random

def main(page: ft.Page):
    page.title = "Just Done - MVP"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.window_height = 800

    # --- DATOS ---
    trabajos = [
        {"id": 1, "cat": "Fontanería", "desc": "Grifo cocina gotea mucho", "dist": "0.8 km", "status": "Abierto", "rating": None},
        {"id": 2, "cat": "Electricidad", "desc": "Salto de diferenciales constante", "dist": "2.1 km", "status": "Abierto", "rating": None},
        {"id": 3, "cat": "Fontanería", "desc": "Instalación de lavavajillas", "dist": "1.5 km", "status": "Cerrado", "rating": None},
        {"id": 4, "cat": "Fontanería", "desc": "Sin agua caliente en lavadero", "dist": "1.7 km", "status": "Abierto", "rating": None},
        {"id": 5, "cat": "Electricidad", "desc": "Frigorífico da calambres", "dist": "1.3 km", "status": "Abierto", "rating": None},
        {"id": 5, "cat": "Electricidad", "desc": "No hay luz en la cocina", "dist": "0.9 km", "status": "Cerrado", "rating": None},
    ]
    
    pros = [
        {"nombre": "Carlos Fontanería", "cat": "Fontanería", "rating": "4.5"},
        {"nombre": "Lucía Electric", "cat": "Electricidad", "rating": "4.7"},
        {"nombre": "Fontaneros García", "cat": "Electricidad", "rating": "4.1"},
        {"nombre": "Pedro Electricista", "cat": "Fontanería", "rating": "3.7"},
    ]

    tipo_trabajo = "Electricidad"

    # --- DIÁLOGOS ---
    tf_desc = ft.TextField(label="Descripción del problema")
    dd_cat = ft.Dropdown(
        label="Categoría",
        options=[ft.dropdown.Option("Electricidad"), ft.dropdown.Option("Fontanería")],
        value="Electricidad"
    )

    def guardar_problema(e):
        if tf_desc.value:
            dist_random = round(random.uniform(0.5, 3.0), 1)
            nuevo = {
                "id": len(trabajos) + 1,
                "cat": dd_cat.value,
                "desc": tf_desc.value,
                "dist": f"{dist_random} km",
                "status": "Abierto",
                "rating": None
            }
            trabajos.insert(0, nuevo)
            dlg_publicar.open = False
            tf_desc.value = ""
            render_client()
            page.update()

    dlg_publicar = ft.AlertDialog(
        title=ft.Text("Publicar Nuevo Problema"),
        content=ft.Column([dd_cat, tf_desc], tight=True),
        actions=[ft.TextButton("Publicar", on_click=guardar_problema)]
    )

    def set_rating(t, nota):
        t["status"] = "Cerrado"
        t["rating"] = nota
        dlg_rating.open = False
        render_client()
        page.update()

    dlg_rating = ft.AlertDialog(title=ft.Text("Valorar trabajo"))

    def abrir_valoracion(t):
        # FIX 1: Usamos val=i para capturar el valor correcto de la estrella
        dlg_rating.content = ft.Row([
            ft.IconButton(
                ft.Icons.STAR, 
                on_click=lambda _, val=i: set_rating(t, val),
                icon_color="amber"
            ) for i in range(1, 6)
        ], alignment=ft.MainAxisAlignment.CENTER)
        dlg_rating.open = True
        page.update()

    main_view = ft.ListView(expand=True, spacing=8, padding=10, scroll=ft.ScrollMode.AUTO)

    # --- RENDER CLIENTE ---
    def render_client():
        main_view.controls.clear()
        main_view.controls.append(ft.Text("Soluciona tus problemas eléctricos y de fontanería.",text_align="center",size=30,weight="bold"))
        main_view.controls.append(
            ft.Container(
                content=ft.Text("➕ Publicar Problema", color="white", weight="bold"),
                bgcolor="blue", padding=15, border_radius=10, alignment=ft.Alignment.CENTER,
                on_click=lambda _: (setattr(dlg_publicar, "open", True), page.update())
            )
        )

        main_view.controls.append(ft.Text("Profesionales Destacados", size=18, weight="bold"))
        pro_row = ft.Row(scroll=ft.ScrollMode.AUTO)
        for p in pros:
            pro_row.controls.append(
                ft.Card(content=ft.Container(padding=10, content=ft.Column([
                    ft.Text(p["nombre"], weight="bold"),
                    ft.Row([ft.Icon(ft.Icons.STAR, color="amber", size=16), ft.Text(p["rating"])])
                ])))
            )
        main_view.controls.append(pro_row)
        main_view.controls.append(ft.Text("Mi Historial", size=20, weight="bold"))
        
        for t in trabajos:
            trailing_control = None
            if t["status"] == "Cerrado":
                if t["rating"]:
                    trailing_control = ft.Text(f"⭐ {t['rating']}", weight="bold")
                else:
                    trailing_control = ft.TextButton("Valorar", on_click=lambda _, t=t: abrir_valoracion(t))

            main_view.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.BOLT if t['cat']=="Electricidad" else ft.Icons.WATER_DROP, 
                            color="#00ff00" if t['status']=="Cerrado" else "#FF9C2B"
                        ),
                        title=ft.Text(t["desc"], size=16, weight="bold"),
                        subtitle=ft.Text(f"Estado: {t['status']}"),
                        trailing=trailing_control,
                    ),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                    border_radius=10
                )
            )
        page.update()

    # --- RENDER PROFESIONAL ---
    def but_ctrl(e):
        nonlocal tipo_trabajo
        tipo_trabajo = e.control.content.value
        render_pro()

    def render_pro():
        main_view.controls.clear()
        main_view.controls.append(ft.Text("Trabajos Disponibles", size=20, weight="bold"))

        main_view.controls.append(ft.MenuBar(
            controls=[
                ft.SubmenuButton(
                    content=ft.Text(f"Filtrar: {tipo_trabajo}"),
                    controls=[
                        ft.MenuItemButton(content=ft.Text("Electricidad"), on_click=but_ctrl),
                        ft.MenuItemButton(content=ft.Text("Fontanería"), on_click=but_ctrl),
                    ],
                ),
            ],
        ))

        for t in trabajos:
            if (t['status']=="Abierto" or t['status']=="En curso") and t["cat"]==tipo_trabajo:
                
                def toggle_trabajo(e, job=t):
                    job["status"] = "En curso" if e.control.value else "Abierto"
                    page.snack_bar = ft.SnackBar(ft.Text(f"Trabajo {job['status']}"))
                    page.snack_bar.open = True
                    page.update()

                main_view.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.BOLT if t['cat']=="Electricidad" else ft.Icons.WATER_DROP, color="#cccccc"),
                            title=ft.Text(t["desc"], size=16, weight="bold"),
                            subtitle=ft.Text(f"{t['dist']} · {t['cat']}"),
                            # FIX 2: El Switch ahora lee el estado del objeto 't' para marcarse o no
                            trailing=ft.Switch(
                                label="Aceptar", 
                                value=True if t["status"] == "En curso" else False,
                                on_change=toggle_trabajo
                            )
                        ),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                        border_radius=10
                    )
                )
        page.update()

    # --- NAVEGACIÓN ---
    page.overlay.extend([dlg_publicar, dlg_rating])
    tab_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.ElevatedButton("Cliente", icon=ft.Icons.PERSON, on_click=lambda _: render_client(), width=180),
            ft.ElevatedButton("Profesional", icon=ft.Icons.ENGINEERING, on_click=lambda _: render_pro(), width=180),
        ],
    )

    page.add(tab_buttons, ft.Divider(height=10), main_view)
    render_client()

if __name__ == "__main__":
    ft.run(main)