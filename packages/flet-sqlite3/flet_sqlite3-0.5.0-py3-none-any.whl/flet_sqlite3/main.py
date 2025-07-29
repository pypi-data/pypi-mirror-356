import flet as ft 

def main(page: ft.Page):
    page.title = "Мастер пол"
    page.scroll = "adaptive"
    page.theme_mode = "light"
    page.theme = ft.Theme(
        font_family="Segoe UI",
        color_scheme=ft.ColorScheme(
            primary="#67BA80", 
            surface="#FFFFFF", 
            background="#F4E8D3", 
        )
    )
    page.bgcolor = "#FFFFFF"  
    page.window.maximizable=True
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    try:
        page.window.icon = "Мастер пол.ico"
    except Exception as e:
        print(e)
    current_edit_id = None
    
    # Таблица типов продуктов
    table1 = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("type")),
            ft.DataColumn(ft.Text("kaof")),
            ft.DataColumn(ft.Text("Действия")),
        ]
        ,rows=[]
    )
    
    table1_container = ft.Container(
        content=ft.Column([table1], scroll=ft.ScrollMode.AUTO),
        height=400,
        width=600,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=10,
        padding=10,
        bgcolor="#FFFFFF"
    )

    def handle_navbar(e):
        index = e.control.selected_index

        if index == 0:
            page.update()
            page.controls.clear()
            add_product_types()
            
        elif index == 1:
            ...

    def delete_product_type(e, row_id):
        try:
            db.delete_product_type(row_id)
            refresh_table1()
        except Exception as ex:
            print(f"Ошибка при удалении: {ex}")
    

    def edit_product_type(e, row_id, type_value, kaof_value):
        nonlocal current_edit_id
        current_edit_id = row_id
        edit_type_input.value = type_value
        edit_kaof_input.value = kaof_value
        page.open(edit_dlg)
    
    def handle_close(e):
        page.close(dlg)
    def handle_edit_close(e):
        page.close(edit_dlg)
  
    def open_dlg(e):
        page.open(dlg)
        
    def open_dlg_product_type(e):
        type_input.value = ""
        kaof_input.value = ""
        page.open(dlg)
        
        
    def save_record(e):
        type_value = type_input.value
        kapf = kaof_input.value
        db.add_product_type_import(type_value, kapf)
        type_input.value = ""
        kaof_input.value = ""
        page.close(dlg)
        refresh_table1()
    
    
    def save_edit_record(e):
        nonlocal current_edit_id
        if current_edit_id:
            type_value = edit_type_input.value
            kaof_value = edit_kaof_input.value
            db.update_product_type(current_edit_id, type_value, kaof_value)
            page.close(edit_dlg)
            refresh_table1()
            
    type_input = ft.TextField(label="Введите тип")
    kaof_input = ft.TextField(label="Введите коэф")
    edit_type_input = ft.TextField(label="Тип")
    edit_kaof_input = ft.TextField(label="Коэффициент")
   
   
    button_add = ft.ElevatedButton(
        "Добавить",
        on_click=open_dlg_product_type,
        bgcolor="#67BA80",
        color="white"
    )
   
    button_refresh1 = ft.ElevatedButton(
        text="Обновить",
        on_click=lambda e:refresh_table1(),
        bgcolor="#67BA80",
        color="white"
    )
    
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Добавление записи"),
        content=ft.Column(controls=[
            type_input, kaof_input], tight=True),
        actions=[
            ft.TextButton("Добавить", on_click=save_record),
            ft.TextButton("Закрыть", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    edit_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Редактирование записи"),
        content=ft.Column(controls=[
            edit_type_input, edit_kaof_input], tight=True),
        actions=[
            ft.TextButton("Сохранить", on_click=save_edit_record),
            ft.TextButton("Закрыть", on_click=handle_edit_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CATEGORY, label="Типы продуктов")
            
        ], on_change=handle_navbar
    )

    def refresh_table1():
        try:
            table1.rows.clear()
            for row in ...:
                row_id, type_value, kaof_value = row
                edit_button = ft.IconButton(
                    icon=ft.Icons.EDIT,
                    tooltip="Редактировать",
                    on_click=lambda e, id=row_id, t=type_value, k=kaof_value: edit_product_type(e, id, t, k)
                )
    
                delete_button = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Удалить",
                    on_click=lambda e, id=row_id: delete_product_type(e, id)
                )
 
                table1.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row_id), no_wrap=0)),
                            ft.DataCell(ft.Text(str(type_value), no_wrap=0)),
                            ft.DataCell(ft.Text(str(kaof_value), no_wrap=0)),
                            ft.DataCell(
                                ft.Row([edit_button, delete_button])
                            )
                        ]
                    )
                )
            page.update()
        except Exception as e:
            print(e)
    

   
    def add_product_types():
        header = ft.Container(
            content=ft.Row([
                ft.Image(src="Мастер пол.ico", width=70, height=70, fit=ft.ImageFit.CONTAIN),
                ft.Column([
                    ft.Text("Мастер пол", size=32, weight=ft.FontWeight.BOLD, color="#67BA80"),
                    ft.Text("Типы продуктов", size=18, color="#67BA80")
                ])
            ], alignment=ft.MainAxisAlignment.START),
            padding=10,
            bgcolor="#F4E8D3",
            border_radius=10,
            width=page.width
        )
        page.add(header)
        page.add(dlg, edit_dlg, table1_container, button_add, button_refresh1)
   
 # TODO: Add refresh_all function to update all tables and add main(ft.app()) call to run the application
    