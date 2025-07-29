import subprocess
import sys
import os
import shutil
from pathlib import Path
import click
from textwrap import dedent

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
        
        # Crear directorio para el esquema
        schemas_dir = Path(self.namespace) / 'schemas'
        schemas_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear main.py con el contenido exacto del ejemplo
        content = self.get_content()
        (schemas_dir / f'{self.schema_name}.py').write_text(content, encoding='utf-8')

        # Crear directorio para las vistas
        views_dir = Path(self.namespace) / 'views' / self.schema_name
        views_dir.mkdir(parents=True, exist_ok=True)
        
        click.echo(f"   ✅ '{self.schema_name}.py' creado en '{self.namespace}/schemas/'")
    
    def get_content(self) -> str:
        """Retorna el contenido exacto del archivo main.py de ejemplo"""
        return dedent(f'''
            # -*- coding: utf-8 -*-
            """
            Fuente principal para la definición de esquemas y generación de modelos CRUD.
            Usa el contenido de tai_sql para definir tablas, relaciones, vistas y generar automáticamente modelos y CRUDs.
            Usa tai_sql.generators para generar modelos y CRUDs basados en las tablas definidas.
            Ejecuta por consola tai_sql generate para generar los recursos definidos en este esquema.
            """
            from __future__ import annotations
            from typing import List, Optional
            # from datetime import datetime, date
            from tai_sql import *
            from tai_sql.generators import *


            # Configurar el datasource
            datasource(
                provider=env('{self.schema_name.upper()}_DATABASE_URL') # Además de env, también puedes usar (para testing) connection_string y params
                # Revisa la documentación de la función datasource para más opciones
            )

            # Configurar los generadores
            generate(
                ModelsGenerator(
                    output_dir='{self.namespace}/{self.subnamespace}' # Directorio donde se generarán los modelos
                ),
                CRUDGenerator(
                    output_dir='{self.namespace}/{self.subnamespace}', # Directorio donde se generarán los CRUDs
                    models_import_path='{self.subnamespace}.{self.schema_name}.models', # Ruta de importación de los modelos generados
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
                email: Optional[str] # Nullable
                
                posts: List[Post] # Relación one-to-many (implícita) con la tabla Post	

            class Post(Table):
                __tablename__ = "post"
                __description__ = "Tabla que almacena los posts de los usuarios" # OPCIONAL
                
                id: int = column(primary_key=True, autoincrement=True)
                title: str = 'Post Title' # Valor por defecto
                content: str
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
            subprocess.run(['poetry', 'add', '--group', 'dev', 'tai-sql'],
                        cwd=self.namespace,
                        check=True, 
                        capture_output=True)
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
        
        dependencies = ['sqlalchemy', 'psycopg2-binary']
        
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

    def msg(self):
        """Muestra el mensaje de éxito y next steps"""
        click.echo()
        click.echo(f'🎉 ¡Proyecto "{self.namespace}" creado exitosamente!')
        click.echo()
        click.echo("📋 Próximos pasos:")
        click.echo("   1. Configurar MAIN_DATABASE_URL en tu entorno:")
        click.echo("      export MAIN_DATABASE_URL='postgresql://user:pass@localhost:5432/dbname'")
        click.echo("   2. Definir tus modelos en schemas/main.py")
        click.echo("   3. Crear recursos:")
        click.echo("      tai-sql generate")
        click.echo()
        click.echo("🔗 Documentación: https://github.com/triplealpha-innovation/tai-sql")
        