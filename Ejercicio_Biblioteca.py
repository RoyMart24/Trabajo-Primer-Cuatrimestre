class Libro:
    def __init__(self, titulo, autor, isbn):
        if not titulo.strip():
            raise ValueError("El título del libro no puede estar vacío.")
        if not autor.strip():
            raise ValueError("El autor del libro no puede estar vacío.")
        if not isbn.strip():
            raise ValueError("El ISBN del libro no puede estar vacío.")
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True
        self.prestado_a = None

    def __str__(self):
        estado = "Disponible" if self.disponible else f"Prestado a {self.prestado_a.nombre} (ID: {self.prestado_a.id_miembro})"
        return f"'{self.titulo}' por {self.autor} (ISBN: {self.isbn}) - Estado: {estado}"


class Miembro:
    def __init__(self, nombre, id_miembro):
        if not nombre.strip():
            raise ValueError("El nombre del miembro no puede estar vacío.")
        if not id_miembro.strip():
            raise ValueError("El ID del miembro no puede estar vacío.")
        self.nombre = nombre
        self.id_miembro = id_miembro
        self.libros_prestados = []

    def tomar_prestado(self, libro):
        if libro.disponible:
            libro.disponible = False
            libro.prestado_a = self
            self.libros_prestados.append(libro)
            return True
        return False

    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            libro.disponible = True
            libro.prestado_a = None
            self.libros_prestados.remove(libro)
            return True
        return False

    def __str__(self):
        libros_nombres = ", ".join([f"'{l.titulo}'" for l in self.libros_prestados]) if self.libros_prestados else "Ninguno"
        return f"Miembro: {self.nombre} (ID: {self.id_miembro}) - Libros prestados: {libros_nombres}"


class Biblioteca:
    def __init__(self):
        self.libros = []
        self.miembros = []

    def agregar_libro(self, libro):
        if not isinstance(libro, Libro):
            raise TypeError("El objeto a agregar debe ser una instancia de la clase Libro.")
        self.libros.append(libro)

    def agregar_miembro(self, miembro):
        if not isinstance(miembro, Miembro):
            raise TypeError("El objeto a agregar debe ser una instancia de la clase Miembro.")
        self.miembros.append(miembro)

    def buscar_libro(self, isbn):
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        raise KeyError(f"No se encontró ningún libro con el ISBN '{isbn}'.")

    def buscar_miembro(self, id_miembro):
        for miembro in self.miembros:
            if miembro.id_miembro == id_miembro:
                return miembro
        raise KeyError(f"No se encontró ningún miembro con el ID '{id_miembro}'.")

    def prestar_libro(self, id_miembro, isbn):
        try:
            miembro = self.buscar_miembro(id_miembro)
            libro = self.buscar_libro(isbn)
            
            if not libro.disponible:
                raise ValueError(f"El libro '{libro.titulo}' ya se encuentra prestado.")
            
            miembro.tomar_prestado(libro)
            return f"Libro '{libro.titulo}' prestado con éxito a {miembro.nombre}."
        except KeyError as e:
            return f"Error: {e.args[0]}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def devolver_libro(self, id_miembro, isbn):
        try:
            miembro = self.buscar_miembro(id_miembro)
            libro = self.buscar_libro(isbn)
            
            if miembro.devolver_libro(libro):
                return f"Libro '{libro.titulo}' devuelto con éxito por {miembro.nombre}."
            else:
                raise ValueError(f"El miembro {miembro.nombre} no tiene prestado el libro '{libro.titulo}'.")
        except KeyError as e:
            return f"Error: {e.args[0]}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def consultar_estado_libros(self):
        if not self.libros:
            print("No hay libros registrados en la biblioteca.")
        else:
            print("\n--- Estado de los Libros ---")
            for libro in self.libros:
                print(libro)

    def consultar_estado_miembros(self):
        if not self.miembros:
            print("No hay miembros registrados en la biblioteca.")
        else:
            print("\n--- Estado de los Miembros ---")
            for miembro in self.miembros:
                print(miembro)


def main():
    biblioteca = Biblioteca()
    
    # Carga inicial opcional de libros para demostrar FileNotFoundError
    try:
        with open("libros_iniciales.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 3:
                    titulo, autor, isbn = partes
                    biblioteca.agregar_libro(Libro(titulo, autor, isbn))
        print("Carga inicial exitosa desde 'libros_iniciales.txt'.")
    except FileNotFoundError:
        print("Aviso: No se encontró 'libros_iniciales.txt' (se omitió la carga inicial).")
        # Cargamos 3 libros por defecto para demostrar la carga al fallar el archivo
        print("Cargando 3 libros de demostración por defecto...")
        biblioteca.agregar_libro(Libro("El Aleph", "Jorge Luis Borges", "978-950-07-2567-5"))
        biblioteca.agregar_libro(Libro("Ficciones", "Jorge Luis Borges", "978-950-07-2568-2"))
        biblioteca.agregar_libro(Libro("Rayuela", "Julio Cortázar", "978-950-511-372-8"))

    while True:
        print("\n=== Sistema de Gestión de Biblioteca ===")
        print("1. Registrar Libro")
        print("2. Registrar Miembro")
        print("3. Prestar Libro")
        print("4. Devolver Libro")
        print("5. Consultar Estado de Libros")
        print("6. Consultar Estado de Miembros")
        print("7. Forzar TypeError (Agregar string a libros)")
        print("8. Intentar cargar archivo inexistente (Prueba FileNotFoundError)")
        print("9. Salir")
        
        opcion = input("Seleccione una opción (1-9): ").strip()
        
        if opcion == "1":
            titulo = input("Ingrese el título del libro: ").strip()
            autor = input("Ingrese el autor del libro: ").strip()
            isbn = input("Ingrese el ISBN del libro: ").strip()
            try:
                # Validar duplicados de ISBN
                try:
                    biblioteca.buscar_libro(isbn)
                    raise ValueError("Ya existe un libro con ese ISBN.")
                except KeyError:
                    pass
                
                libro = Libro(titulo, autor, isbn)
                biblioteca.agregar_libro(libro)
                print(f"Libro '{titulo}' registrado exitosamente.")
            except ValueError as e:
                print(f"Error de Valor (ValueError): {e}")
            except TypeError as e:
                print(f"Error de Tipo (TypeError): {e}")
            
        elif opcion == "2":
            nombre = input("Ingrese el nombre del miembro: ").strip()
            id_miembro = input("Ingrese el ID del miembro: ").strip()
            try:
                # Validar duplicados de ID
                try:
                    biblioteca.buscar_miembro(id_miembro)
                    raise ValueError("Ya existe un miembro con ese ID.")
                except KeyError:
                    pass
                
                miembro = Miembro(nombre, id_miembro)
                biblioteca.agregar_miembro(miembro)
                print(f"Miembro '{nombre}' registrado exitosamente.")
            except ValueError as e:
                print(f"Error de Valor (ValueError): {e}")
            except TypeError as e:
                print(f"Error de Tipo (TypeError): {e}")
            
        elif opcion == "3":
            id_miembro = input("Ingrese el ID del miembro: ").strip()
            isbn = input("Ingrese el ISBN del libro: ").strip()
            resultado = biblioteca.prestar_libro(id_miembro, isbn)
            print(resultado)
            
        elif opcion == "4":
            id_miembro = input("Ingrese el ID del miembro: ").strip()
            isbn = input("Ingrese el ISBN del libro: ").strip()
            resultado = biblioteca.devolver_libro(id_miembro, isbn)
            print(resultado)
            
        elif opcion == "5":
            biblioteca.consultar_estado_libros()
            
        elif opcion == "6":
            biblioteca.consultar_estado_miembros()
            
        elif opcion == "7":
            print("\nIntentando agregar un texto plano a la biblioteca (debería lanzar TypeError)...")
            try:
                biblioteca.agregar_libro("Este es un string de prueba, no un Libro")
            except TypeError as e:
                print(f"Excepción capturada con éxito: {e}")
                
        elif opcion == "8":
            archivo_buscado = "archivo_inexistente_123.txt"
            print(f"\nIntentando abrir '{archivo_buscado}' (debería lanzar FileNotFoundError)...")
            try:
                with open(archivo_buscado, "r") as f:
                    content = f.read()
            except FileNotFoundError as e:
                print(f"Excepción capturada con éxito: {e}")
                print(f"Detalle: El sistema no pudo encontrar el archivo especificado.")
                
        elif opcion == "9":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
