class Estudiante:
    def __init__(self, nombre, apellido, matricula, carrera, identificador_unico):
        if not nombre.strip():
            raise ValueError("El nombre del estudiante no puede estar vacío.")
        if not apellido.strip():
            raise ValueError("El apellido del estudiante no puede estar vacío.")
        if not matricula.strip():
            raise ValueError("El número de matrícula no puede estar vacío.")
        if not carrera.strip():
            raise ValueError("La carrera no puede estar vacía.")
        if not identificador_unico.strip():
            raise ValueError("El identificador único no puede estar vacío.")
        
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula
        self.carrera = carrera
        self.identificador_unico = identificador_unico
        self.cursos_inscritos = []

    def __str__(self):
        cursos_nombres = ", ".join([f"'{c.nombre_curso}'" for c in self.cursos_inscritos]) if self.cursos_inscritos else "Ninguno"
        return f"Estudiante: {self.nombre} {self.apellido} (Matrícula: {self.matricula}, ID: {self.identificador_unico}) - Carrera: {self.carrera} - Cursos: {cursos_nombres}"


class Curso:
    def __init__(self, nombre_curso, codigo_curso, profesor, capacidad_maxima):
        if not nombre_curso.strip():
            raise ValueError("El nombre del curso no puede estar vacío.")
        if not codigo_curso.strip():
            raise ValueError("El código del curso no puede estar vacío.")
        if not profesor.strip():
            raise ValueError("El profesor encargado no puede estar vacío.")
        
        try:
            capacidad = int(capacidad_maxima)
            if capacidad <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("La capacidad máxima del curso debe ser un número entero mayor a 0.")

        self.nombre_curso = nombre_curso
        self.codigo_curso = codigo_curso
        self.profesor = profesor
        self.capacidad_maxima = capacidad
        self.estudiantes_inscritos = []

    def __str__(self):
        cupos_disponibles = self.capacidad_maxima - len(self.estudiantes_inscritos)
        return f"Curso: '{self.nombre_curso}' (Código: {self.codigo_curso}) - Profesor: {self.profesor} - Inscriptos: {len(self.estudiantes_inscritos)}/{self.capacidad_maxima} (Cupos libres: {cupos_disponibles})"


class Facultad:
    def __init__(self):
        self.estudiantes = []
        self.cursos = []

    def agregar_estudiante(self, estudiante):
        if not isinstance(estudiante, Estudiante):
            raise TypeError("El objeto a agregar debe ser una instancia de la clase Estudiante.")
        self.estudiantes.append(estudiante)

    def agregar_curso(self, curso):
        if not isinstance(curso, Curso):
            raise TypeError("El objeto a agregar debe ser una instancia de la clase Curso.")
        self.cursos.append(curso)

    def buscar_estudiante(self, identificador_unico):
        for estudiante in self.estudiantes:
            if estudiante.identificador_unico == identificador_unico:
                return estudiante
        raise KeyError(f"No se encontró ningún estudiante con el ID '{identificador_unico}'.")

    def buscar_curso(self, codigo_curso):
        for curso in self.cursos:
            if curso.codigo_curso == codigo_curso:
                return curso
        raise KeyError(f"No se encontró ningún curso con el código '{codigo_curso}'.")

    def inscribir_estudiante(self, identificador_unico, codigo_curso):
        try:
            estudiante = self.buscar_estudiante(identificador_unico)
            curso = self.buscar_curso(codigo_curso)

            if curso in estudiante.cursos_inscritos:
                raise ValueError(f"El estudiante {estudiante.nombre} {estudiante.apellido} ya está inscripto en el curso '{curso.nombre_curso}'.")

            if len(curso.estudiantes_inscritos) >= curso.capacidad_maxima:
                raise ValueError(f"No hay cupos disponibles para el curso '{curso.nombre_curso}' (Capacidad: {curso.capacidad_maxima}).")

            estudiante.cursos_inscritos.append(curso)
            curso.estudiantes_inscritos.append(estudiante)
            return f"Estudiante '{estudiante.nombre} {estudiante.apellido}' inscripto con éxito al curso '{curso.nombre_curso}'."
        except KeyError as e:
            return f"Error: {e.args[0]}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def dar_baja_estudiante(self, identificador_unico, codigo_curso):
        try:
            estudiante = self.buscar_estudiante(identificador_unico)
            curso = self.buscar_curso(codigo_curso)

            if curso not in estudiante.cursos_inscritos:
                raise ValueError(f"El estudiante {estudiante.nombre} {estudiante.apellido} no está inscripto en el curso '{curso.nombre_curso}'.")

            estudiante.cursos_inscritos.remove(curso)
            curso.estudiantes_inscritos.remove(estudiante)
            return f"Estudiante '{estudiante.nombre} {estudiante.apellido}' dado de baja con éxito del curso '{curso.nombre_curso}'."
        except KeyError as e:
            return f"Error: {e.args[0]}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def consultar_estado_cursos(self):
        if not self.cursos:
            print("No hay cursos registrados en la facultad.")
        else:
            print("\n--- Estado de los Cursos ---")
            for curso in self.cursos:
                print(curso)

    def consultar_estado_estudiantes(self):
        if not self.estudiantes:
            print("No hay estudiantes registrados en la facultad.")
        else:
            print("\n--- Estado de los Estudiantes ---")
            for estudiante in self.estudiantes:
                print(estudiante)


def main():
    facultad = Facultad()

    try:
        with open("estudiantes_iniciales.txt", "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 5:
                    nombre, apellido, matricula, carrera, identificador_unico = partes
                    facultad.agregar_estudiante(Estudiante(nombre, apellido, matricula, carrera, identificador_unico))
        print("Carga inicial exitosa desde 'estudiantes_iniciales.txt'.")
    except FileNotFoundError:
        print("Aviso: No se encontró 'estudiantes_iniciales.txt' (se omitió la carga inicial).")
        # Cargo 3 estudiantes por defecto para demostrar la carga al fallar el archivo (FileNotFoundError)
        print("Cargando 3 estudiantes de demostración por defecto...")
        facultad.agregar_estudiante(Estudiante("Juan", "Pérez", "12345", "Analista de Sistemas", "E001"))
        facultad.agregar_estudiante(Estudiante("María", "Gómez", "67890", "Desarrollo de Software", "E002"))
        facultad.agregar_estudiante(Estudiante("Carlos", "López", "11223", "Desarrollo de Software", "E003"))

    while True:
        print("\n=== Sistema de Gestión de Facultad ===")
        print("1. Registrar Estudiante")
        print("2. Registrar Curso")
        print("3. Inscribir Estudiante en Curso")
        print("4. Dar de Baja Estudiante de Curso")
        print("5. Consultar Estado de Cursos")
        print("6. Consultar Estado de Estudiantes")
        print("7. Forzar TypeError (Agregar string a estudiantes)")
        print("8. Intentar cargar archivo inexistente (Prueba FileNotFoundError)")
        print("9. Salir")

        opcion = input("Seleccione una opción (1-9): ").strip()

        if opcion == "1":
            nombre = input("Ingrese el nombre del estudiante: ").strip()
            apellido = input("Ingrese el apellido del estudiante: ").strip()
            matricula = input("Ingrese el número de matrícula: ").strip()
            carrera = input("Ingrese la carrera: ").strip()
            identificador_unico = input("Ingrese el ID único del estudiante: ").strip()
            try:
                # Validar duplicados de ID único
                try:
                    facultad.buscar_estudiante(identificador_unico)
                    raise ValueError("Ya existe un estudiante con ese ID único.")
                except KeyError:
                    pass

                estudiante = Estudiante(nombre, apellido, matricula, carrera, identificador_unico)
                facultad.agregar_estudiante(estudiante)
                print(f"Estudiante '{nombre} {apellido}' registrado exitosamente.")
            except ValueError as e:
                print(f"Error de Valor (ValueError): {e}")
            except TypeError as e:
                print(f"Error de Tipo (TypeError): {e}")

        elif opcion == "2":
            nombre_curso = input("Ingrese el nombre del curso: ").strip()
            codigo_curso = input("Ingrese el código del curso: ").strip()
            profesor = input("Ingrese el profesor encargado: ").strip()
            capacidad_maxima = input("Ingrese la capacidad máxima: ").strip()
            try:
                # Validar duplicados de código de curso
                try:
                    facultad.buscar_curso(codigo_curso)
                    raise ValueError("Ya existe un curso con ese código.")
                except KeyError:
                    pass

                curso = Curso(nombre_curso, codigo_curso, profesor, capacidad_maxima)
                facultad.agregar_curso(curso)
                print(f"Curso '{nombre_curso}' registrado exitosamente.")
            except ValueError as e:
                print(f"Error de Valor (ValueError): {e}")
            except TypeError as e:
                print(f"Error de Tipo (TypeError): {e}")

        elif opcion == "3":
            identificador_unico = input("Ingrese el ID del estudiante: ").strip()
            codigo_curso = input("Ingrese el código del curso: ").strip()
            resultado = facultad.inscribir_estudiante(identificador_unico, codigo_curso)
            print(resultado)

        elif opcion == "4":
            identificador_unico = input("Ingrese el ID del estudiante: ").strip()
            codigo_curso = input("Ingrese el código del curso: ").strip()
            resultado = facultad.dar_baja_estudiante(identificador_unico, codigo_curso)
            print(resultado)

        elif opcion == "5":
            facultad.consultar_estado_cursos()

        elif opcion == "6":
            facultad.consultar_estado_estudiantes()

        elif opcion == "7":
            print("\nIntentando agregar un texto plano a la facultad (debería lanzar TypeError)...")
            try:
                facultad.agregar_estudiante("Este es un string de prueba, no un Estudiante")
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
