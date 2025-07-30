import subprocess
import sys
import os
import shutil
from pathlib import Path
import click
from textwrap import dedent

from tai_sql import pm

class NewSchemaCommand:

    def __init__(self, namespace: str, schema_name: str):
        self.namespace = namespace
        self.schema_name = schema_name

    @property
    def subnamespace(self) -> str:
        """Retorna el subnamespace basado en el namespace"""
        return self.namespace.replace('-', '_')
    
    def exists(self) -> bool:
        """Verifica si el esquema ya existe"""
        schemas_dir = Path(self.namespace) / 'schemas'
        return (schemas_dir / f'{self.schema_name}.py').exists()
    
    def create(self):
        """Crea el esquema con la estructura básica"""
        click.echo(f"🚀 Creando esquema '{self.schema_name}' en '{self.namespace}/schemas'...")

        if self.exists():
            click.echo(f"❌ Error: El esquema '{self.schema_name}' ya existe en '{self.namespace}/schemas'.", err=True)
            sys.exit(1)
        
        # Verificar si estamos en un proyecto existente
        project_root = Path(self.namespace)
        existing_config = None
        
        if project_root.exists():
            existing_config = pm.load_config(project_root)
        
        # Crear directorio para el esquema
        schemas_dir = Path(self.namespace) / 'schemas'
        schemas_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear modulo con el contenido exacto del ejemplo
        content = self.get_content()
        (schemas_dir / f'{self.schema_name}.py').write_text(content, encoding='utf-8')

        # Crear directorio para las vistas
        views_dir = Path(self.namespace) / 'views' / self.schema_name
        views_dir.mkdir(parents=True, exist_ok=True)

        self.view_example()
        
        # Actualizar configuración del proyecto si existe
        if existing_config:
            # Si es el primer schema o queremos cambiar el default
            if not existing_config.default_schema:
                pm.update_config(
                    project_root,
                    default_schema=f'schemas/{self.schema_name}.py'
                )
                click.echo(f"   📄 Schema '{self.schema_name}' establecido como default")
        
        click.echo(f"   ✅ '{self.schema_name}.py' creado en '{self.namespace}/schemas/'")
    
    def view_example(self) -> None:
        """Crea un archivo de ejemplo de vista SQL"""
        views_dir = Path(self.namespace) / 'views' / self.schema_name

        sql_content = dedent('''
            SELECT
                usuario.id AS user_id,
                usuario.name AS user_name,
                COUNT(post.id) AS post_count
            FROM usuario
            LEFT JOIN post ON usuario.id = post.author_id
            GROUP BY usuario.id, usuario.name
        ''').strip()
        
        (views_dir / 'user_stats.sql').write_text(sql_content, encoding='utf-8')
    
    def get_content(self) -> str:
        """Retorna el contenido exacto del archivo public.py de ejemplo"""
        return dedent(f'''
            # -*- coding: utf-8 -*-
            """
            Fuente principal para la definición de esquemas y generación de modelos CRUD.
            Usa el contenido de tai_sql para definir tablas, relaciones, vistas y generar automáticamente modelos y CRUDs.
            Usa tai_sql.generators para generar modelos y CRUDs basados en las tablas definidas.
            Ejecuta por consola tai_sql generate para generar los recursos definidos en este esquema.
            """
            from __future__ import annotations
            from tai_sql import *
            from tai_sql.generators import *


            # Configurar el datasource
            datasource(
                provider=env('MAIN_DATABASE_URL'), # Además de env, también puedes usar (para testing) connection_string y params
                schema='{self.schema_name}', # Esquema del datasource
            )

            # Configurar los generadores
            generate(
                ModelsGenerator(
                    output_dir='{self.namespace}/{self.subnamespace}' # Directorio donde se generarán los modelos
                ),
                CRUDGenerator(
                    output_dir='{self.namespace}/{self.subnamespace}', # Directorio donde se generarán los CRUDs
                    mode='sync' # Modo de generación: 'sync' para síncrono, 'async' para asíncrono, 'both' para ambos
                ),
                ERDiagramGenerator(
                    output_dir='{self.namespace}/diagrams', # Directorio donde se generarán los diagramas
                )
            )

            # Definición de tablas y relaciones

            # Ejemplo de definición de tablas y relaciones. Eliminar estos modelos y definir los tuyos propios.
            class Usuario(Table):
                __tablename__ = "usuario"
                __description__ = "Tabla que almacena información de los usuarios del sistema" # OPCIONAL
                
                id: int = column(primary_key=True, autoincrement=True)
                name: str
                pwd: str = column(encrypt=True) # Contraseña encriptada
                email: Optional[str] # Nullable
                
                posts: List[Post] # Relación one-to-many (implícita) con la tabla Post	

            class Post(Table):
                __tablename__ = "post"
                __description__ = "Tabla que almacena los posts de los usuarios" # OPCIONAL
                
                id: bigint = column(primary_key=True, autoincrement=True) # Tipo bigint para PostgreSQL
                title: str = 'Post Title' # Valor por defecto
                content: str
                timestamp: datetime = column(default=datetime.now) # Timestamp con generador de valor por defecto
                author_id: int
                
                author: Usuario = relation(fields=['author_id'], references=['id'], backref='posts') # Relación many-to-one con la tabla User
            
            # Definición de vistas

            class UserStats(View):
                __tablename__ = "user_stats"
                __query__ = query('user_stats.sql') # Esto es necesario para usar tai-sql push
                __description__ = "Vista que muestra estadísticas de usuarios y sus posts" # OPCIONAL
                
                user_id: int
                user_name: str
                post_count: int
        ''').strip()


class InitCommand:

    def __init__(self, namespace: str, schema_name: str):
        self.namespace = namespace
        self.schema_name = schema_name
    
    @property
    def subnamespace(self) -> str:
        """Retorna el subnamespace basado en el namespace"""
        return self.namespace.replace('-', '_')
    
    def check_poetry(self):
        """Verifica que Poetry esté instalado y disponible"""
        try:
            subprocess.run(['poetry', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            click.echo("❌ Error: Poetry no está instalado o no está en el PATH", err=True)
            click.echo("Instala Poetry desde: https://python-poetry.org/docs/#installation")
            sys.exit(1)
    
    def check_directory_is_avaliable(self):
        """Verifica que el directorio del proyecto no exista"""
        if os.path.exists(self.namespace):
            click.echo(f"❌ Error: el directorio '{self.namespace}' ya existe", err=True)
            sys.exit(1)
    
    def check_virtualenv(self):
        """Verifica que el entorno virtual de Poetry esté activo"""
        if 'VIRTUAL_ENV' not in os.environ:
            click.echo("❌ Error: No hay entorno virutal activo", err=True)
            click.echo("   Puedes crear uno con 'pyenv virtualenv <env_name>' y asignarlo con 'pyenv local <env_name>'", err=True)
            sys.exit(1)
    
    def create_project(self):
        """Crea el proyecto base con Poetry"""
        click.echo(f"🚀 Creando '{self.namespace}'...")
        
        try:
            subprocess.run(['poetry', 'new', self.namespace], 
                        check=True, 
                        capture_output=True)
            subprocess.run(['sed', '-i', '/^python *=/d', 'pyproject.toml'], 
                        cwd=self.namespace,
                        check=True, 
                        capture_output=True)
            subprocess.run(['sed', '-i', '/\\[tool.poetry.dependencies\\]/a python = "^3.10"', 'pyproject.toml'], 
                        cwd=self.namespace,
                        check=True, 
                        capture_output=True)
            # subprocess.run(['poetry', 'add', '--group', 'dev', 'tai-sql'],
            #             cwd=self.namespace,
            #             check=True, 
            #             capture_output=True)
            subprocess.run(['poetry', 'install'],
                        cwd=self.namespace,
                        check=True, 
                        capture_output=True)
            click.echo(f"✅ poetry new '{self.namespace}': OK")
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Error: {e}", err=True)
            sys.exit(1)

    def add_dependencies(self):
        """Añade las dependencias necesarias al proyecto"""
        click.echo("📦 Añadiendo dependencias...")
        
        dependencies = ['sqlalchemy', 'psycopg2-binary', 'cryptography']
        
        for dep in dependencies:
            try:
                subprocess.run(['poetry', 'add', dep], 
                            cwd=self.namespace,
                            check=True, 
                            capture_output=True)
                click.echo(f"   ✅ {dep} añadido")
            except subprocess.CalledProcessError as e:
                click.echo(f"   ❌ Error al añadir dependencia {dep}: {e}", err=True)
                sys.exit(1)
    
    def add_folders(self) -> None:
        """Crea la estructura adicional del proyecto"""
        new_schema = NewSchemaCommand(self.namespace, self.schema_name)
        new_schema.create()
        test_dir = Path(self.namespace) / 'tests'
        if test_dir.exists():
            shutil.rmtree(test_dir)
        # Crear directorio para los diagramas
        diagrams_dir = Path(self.namespace) / 'diagrams'
        diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    def create_project_config(self) -> None:
        """Crea el archivo .taisqlproject con la configuración inicial"""
        try:
            project_root = Path(self.namespace)
            pm.create_config(
                name=self.namespace,
                project_root=project_root
            )
            
            # Establecer el schema por defecto
            pm.update_config(
                project_root,
                default_schema=self.schema_name
            )
            
        except Exception as e:
            click.echo(f"❌ Error al crear configuración del proyecto: {e}", err=True)
            sys.exit(1)

    def msg(self):
        """Muestra el mensaje de éxito y next steps con información del proyecto"""
        # ✅ Obtener información del proyecto creado
        project_root = Path(self.namespace)
        project_config = pm.load_config(project_root)
        
        click.echo()
        click.echo(f'🎉 ¡Proyecto "{self.namespace}" creado exitosamente!')
        
        # Mostrar información del proyecto
        if project_config:
            click.echo()
            click.echo("📋 Información del proyecto:")
            click.echo(f"   Nombre: {project_config.name}")
            click.echo(f"   Schema por defecto: {project_config.default_schema}")
        
        click.echo()
        click.echo("📋 Próximos pasos:")
        click.echo(f"   1. cd {self.namespace}")
        click.echo("   2. Configurar MAIN_DATABASE_URL en tu entorno:")
        click.echo("      export MAIN_DATABASE_URL='postgresql://user:pass@localhost:5432/dbname'")
        click.echo(f"   3. Definir tus modelos en schemas/{self.schema_name}.py")
        click.echo("   4. Crear recursos:")
        click.echo("      tai-sql generate    # Usa schema por defecto automáticamente")
        click.echo("      tai-sql push --createdb")
        click.echo()
        click.echo("🔧 Comandos útiles:")
        click.echo("   tai-sql project                    # Ver info del proyecto")
        click.echo("   tai-sql new-schema <nombre>        # Crear nuevo schema")
        click.echo("   tai-sql set-default-schema <path>  # Cambiar schema por defecto")
        click.echo()
        click.echo("🔗 Documentación: https://github.com/triplealpha-innovation/tai-sql")
        