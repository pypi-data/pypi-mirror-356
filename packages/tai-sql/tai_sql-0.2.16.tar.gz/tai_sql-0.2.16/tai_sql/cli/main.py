import sys
import click
from .commands import (
    InitCommand,
    NewSchemaCommand,
    PushCommand,
    DBCommand,
    GenerateCommand,
    Connectivity
)

from tai_sql import pm

config = pm.load_config()
default_schema_name = None
if config:
    pm.set_current_schema(config.default_schema)
    default_schema_name = config.default_schema

@click.group()
def cli():
    """CLI para tai-sql: Un framework de ORM basado en SQLAlchemy."""
    pass

@cli.command()
@click.option('--name', '-n', default='database', help='Nombre del proyecto a crear')
@click.option('--schema', '-s', default='public', help='Nombre del primer esquema a crear')
def init(name: str, schema: str):
    """Inicializa un nuevo proyecto tai-sql"""
    command = InitCommand(namespace=name, schema_name=schema)
    try:
        command.check_poetry()
        command.check_directory_is_avaliable()
        command.check_virtualenv()
        command.create_project()
        command.add_dependencies()
        command.add_folders()
        command.create_project_config()
        command.msg()
    except Exception as e:
        click.echo(f"❌ Error al inicializar el proyecto: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--schema', '-s', help='Nombre del esquema', default=default_schema_name)
@click.option('--create', '-c', is_flag=True, help='Crea la base de datos + schema si no existe')
@click.option('--force', '-f', is_flag=True, help='Forzar la generación de recursos, incluso si ya existen')
@click.option('--dry-run', '-d', is_flag=True, help='Mostrar las sentencias DDL sin ejecutarlas')
@click.option('--verbose', '-v', is_flag=True, help='Mostrar información detallada durante la ejecución')
def push(schema: str, create: bool, force: bool, dry_run: bool, verbose: bool):
    """Síncroniza el esquema con la base de datos"""

    if schema:
        pm.set_current_schema(schema)

    if not schema and not pm.db:
        click.echo(f"❌ No existe ningún esquema por defecto", err=True)
        click.echo(f"   Puedes definir uno con: tai-sql set-default-schema <nombre>", err=True)
        click.echo(f"   O usar la opción: --schema <nombre_esquema>", err=True)
        sys.exit(1)

    db_command = DBCommand()
    push = PushCommand()
    connectivity = Connectivity()
    try:
        # Validar la configuración del schema

        click.echo(f"🚀 Push schema: {schema}")

        if not connectivity.ping_host():
            click.echo(f"❌ No se encuentra el servidor {pm.db.provider.host}", err=True)
            sys.exit(1)

        if create:
            # Crear la base de datos si no existe
            db_command.create()
        else:
            if not connectivity.db_exist():
                click.echo(f"⚠️  La base de datos {pm.db.provider.database} no existe", err=True)
                click.echo("   Usa la opción --create para crearla")
                sys.exit(1)
            if not connectivity.schema_exists():
                click.echo(f"⚠️  El schema {pm.db.schema_name} no existe")
                click.echo("   Usa la opción --create para crearlo")
                sys.exit(1)
        
        # Cargar y procesar el schema
        push.load_schema()

        # Validar nombres
        push.validate_schema_names()
        
        # Generar DDL
        ddl = push.generate()
        
        # Mostrar DDL
        if ddl:
            if verbose or dry_run:
                push.ddl_manager.show()
            else:
                click.echo("   ℹ️  Modo silencioso: No se mostrarán las sentencias DDL")
        
        if dry_run:
            click.echo("🔍 Modo dry-run: No se ejecutaron cambios")
            return
        
        # Confirmar ejecución
        if not force:
            confirm = click.confirm("¿Deseas ejecutar estas sentencias en la base de datos?")
            if not confirm:
                click.echo("❌ Operación cancelada")
                return
        
        # Ejecutar DDL
        changes = push.execute()

        if changes:

            GenerateCommand.run()
        
    except Exception as e:
        import logging
        logging.exception(e)
        click.echo(f"❌ Error al procesar schema: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--schema', '-s', help='Nombre del esquema', default=default_schema_name)
@click.option('--all', is_flag=True, help='Generar para todos los esquemas disponibles')
def generate(schema: str, all: bool):
    """Genera recursos basados en los generadores configurados"""
    
    if schema:
        pm.set_current_schema(schema)

    if not schema and not pm.db:
        click.echo(f"❌ No existe ningún esquema por defecto", err=True)
        click.echo(f"   Puedes definir uno con: tai-sql set-default-schema <nombre>", err=True)
        click.echo(f"   O usar la opción: --schema <nombre_esquema>", err=True)
        sys.exit(1)

    GenerateCommand.run()


@cli.command()
@click.argument('name')
def new_schema(name: str):
    """Crea un nuevo esquema en el proyecto"""
    if not name:
        click.echo("❌ Error: Debes proporcionar un nombre para el esquema.", err=True)
        sys.exit(1)
    
    project_root = pm.find_project_root()
    if project_root is None:
        click.echo("❌ Error: No se encontró proyecto TAI-SQL", err=True)
        click.echo("   Ejecuta este comando una vez hecho tai-sql init", err=True)
        sys.exit(1)

    project = project_root.name

    try:
        command = NewSchemaCommand(namespace=project, schema_name=name)
        command.create()
    except Exception as e:
        click.echo(f"❌ Error al crear el esquema: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--schema', '-s', help='Nombre del esquema', default=default_schema_name)
@click.option('--timeout', '-t', default=5, help='Timeout en segundos para la verificación (default: 5)')
@click.option('--check-db', '-d', is_flag=True, help='También verificar si la base de datos específica existe')
@click.option('--full', '-f', is_flag=True, help='Verificación completa (incluye ping ICMP, TCP y BD)')
@click.option('--quiet', '-q', is_flag=True, help='Modo silencioso, solo mostrar resultado final')
def ping(schema: str, timeout: int, check_db: bool, full: bool, quiet: bool):
    """Verifica la conectividad con el servidor"""

    if schema:
        pm.set_current_schema(schema)

    if not schema and not pm.db:
        click.echo(f"❌ No existe ningún esquema por defecto", err=True)
        click.echo(f"   Puedes definir uno con: tai-sql set-default-schema <nombre>", err=True)
        click.echo(f"   O usar la opción: --schema <nombre_esquema>", err=True)
        sys.exit(1)
    
    # Crear instancia de Connectivity
    connectivity = Connectivity()
    
    # Mostrar información de conexión si no está en modo silencioso
    if not quiet:

        click.echo("🔧 Información de conexión:")
        click.echo(f"   Motor: {pm.db.provider.drivername}")
        click.echo(f"   Host: {pm.db.provider.host}")
        click.echo(f"   Puerto: {pm.db.provider.port}")
        click.echo(f"   Base de datos: {pm.db.provider.database}")
        click.echo(f"   Usuario: {pm.db.provider.username}")
        click.echo()
    
    success = True
    
    try:
        if full:
            # Verificación completa: ping + conectividad de BD
            if not quiet:
                click.echo("🌐 Verificación FULL")
                click.echo()
            
            if connectivity.verify(timeout):
                if not quiet:
                    click.echo()
                    click.echo("✅ Verificación de conectividad exitosa")
            else:
                if not quiet:
                    click.echo()
                    click.echo("❌ Falló la verificación de conectividad")
                success = False
        else:
            # Solo ping básico al host
            if not quiet:
                click.echo("🏓 Verificación BASIC")
                click.echo()
            
            if connectivity.ping_host(timeout):
                if not quiet:
                    click.echo()
                    click.echo("✅ Host accesible")
            else:
                if not quiet:
                    click.echo()
                    click.echo("❌ Host no accesible")
                success = False
        
        # Verificar existencia de la base de datos si se solicita
        if check_db and success:
            if not quiet:
                click.echo()
                click.echo("🗄️  Verificando existencia de la base de datos...")
            
            if connectivity.db_exist():
                if not quiet:
                    click.echo()
                    click.echo("✅ La base de datos existe")
            else:
                if not quiet:
                    click.echo()
                    click.echo("⚠️  La base de datos no existe")
                    click.echo("   💡 Sugerencia: Usa 'tai-sql push --createdb' para crearla")
                # No marcar como fallo si solo falta la BD
        
        # Resultado final
        if quiet:
            if success:
                click.echo("✅ CONECTIVIDAD OK")
            else:
                click.echo("❌ CONECTIVIDAD FALLIDA")
        else:
            click.echo()
            if success:
                click.echo("🎉 Verificación de conectividad completada exitosamente")
            else:
                click.echo("💥 Falló la verificación de conectividad")
        
        # Exit code apropiado
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        click.echo()
        click.echo("⚠️  Verificación interrumpida por el usuario")
        sys.exit(130)
    except Exception as e:
        click.echo(f"❌ Error inesperado durante la verificación: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('schema_name')
def set_default_schema(schema_name: str):
    """Establece el schema por defecto del proyecto"""
    
    try:
        # Verificar que estamos en un proyecto TAI-SQL
        project_root = pm.find_project_root()
        if not project_root:
            click.echo("❌ No se encontró proyecto TAI-SQL", err=True)
            click.echo("   Ejecuta este comando desde un directorio de proyecto", err=True)
            sys.exit(1)
        
        # Obtener configuración actual
        config = pm.get_project_config()
        if not config:
            click.echo("❌ No se pudo cargar la configuración del proyecto", err=True)
            sys.exit(1)
        
        click.echo(f"📁 Proyecto: {config.name}")
        
        # Verificar que el schema existe
        available_schemas = pm.discover_schemas()
        
        if schema_name not in available_schemas:
            click.echo(f"❌ El schema '{schema_name}' no existe en el proyecto", err=True)
            
            if available_schemas:
                click.echo()
                click.echo("📄 Schemas disponibles:")
                for schema in available_schemas:
                    marker = "✅" if schema == config.default_schema else "  "
                    click.echo(f"   {marker} {schema}")
                
                if config.default_schema:
                    click.echo()
                    click.echo(f"📌 Schema por defecto actual: {config.default_schema}")
            else:
                click.echo("   No se encontraron schemas en el proyecto")
                click.echo("   💡 Crea un schema con: tai-sql new-schema <nombre>")
            
            sys.exit(1)
        
        # Verificar si ya es el schema por defecto
        if schema_name == config.default_schema:
            click.echo(f"ℹ️  '{schema_name}' ya es el schema por defecto")
            sys.exit(0)
        
        # Establecer como schema por defecto
        click.echo(f"🔄 Estableciendo '{schema_name}' como schema por defecto...")
        
        pm.set_default_schema(schema_name)
        
        # Actualizar el schema actual en memoria
        pm.set_current_schema(schema_name)
        
        click.echo(f"✅ Schema por defecto actualizado: {schema_name}")
        
        # Mostrar información adicional
        schema_file = project_root / pm.SCHEMAS_DIR / f"{schema_name}.py"
        click.echo(f"📄 Archivo: {schema_file.relative_to(project_root)}")
        
        click.echo()
        click.echo("💡 Próximos pasos:")
        click.echo("   • Los comandos sin --schema usarán este schema automáticamente")
        click.echo("   • tai-sql generate")
        click.echo("   • tai-sql push")
        click.echo("   • tai-sql ping")
        
    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error inesperado: {e}", err=True)
        sys.exit(1)


@cli.command()
def info():
    """Muestra información del proyecto actual"""
    
    try:
        # Verificar que estamos en un proyecto TAI-SQL
        project_root = pm.find_project_root()
        if not project_root:
            click.echo("❌ No se encontró proyecto TAI-SQL", err=True)
            click.echo("   Ejecuta este comando desde un directorio de proyecto", err=True)
            sys.exit(1)
        
        # Obtener información del proyecto
        config = pm.get_project_config()
        available_schemas = pm.discover_schemas()
        current_schema = pm.db.schema_name
        
        # Mostrar información
        click.echo("📁 Información del proyecto:")
        if config:
            click.echo(f"   Nombre: {config.name}")
            click.echo(f"   Directorio: {project_root}")
            click.echo(f"   Schema por defecto: {config.default_schema or 'No configurado'}")
        else:
            click.echo("   ⚠️  No se pudo cargar la configuración")
        
        click.echo()
        click.echo("📄 Schemas disponibles:")
        
        if available_schemas:
            for schema in available_schemas:
                markers = []
                
                # Marcar schema por defecto
                if config and schema == config.default_schema:
                    markers.append("✅ default")
                
                # Marcar schema actual en memoria
                if schema == current_schema:
                    markers.append("📌 current")
                
                marker_text = f" ({', '.join(markers)})" if markers else ""
                click.echo(f"   • {schema}{marker_text}")
                
                # Mostrar si está cargado
                schema_manager = pm.get_schema_manager(schema)
                if schema_manager and schema_manager.is_loaded:
                    click.echo(f"     └─ Estado: Cargado")
        else:
            click.echo("   (No se encontraron schemas)")
            click.echo("   💡 Crea un schema con: tai-sql new-schema <nombre>")
        
        # Información adicional
        if config and config.default_schema:
            click.echo()
            click.echo("🔧 Comandos disponibles:")
            click.echo("   tai-sql generate              # Usa schema por defecto")
            click.echo("   tai-sql push                  # Usa schema por defecto")
            click.echo("   tai-sql set-default-schema <nombre>  # Cambiar default")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()