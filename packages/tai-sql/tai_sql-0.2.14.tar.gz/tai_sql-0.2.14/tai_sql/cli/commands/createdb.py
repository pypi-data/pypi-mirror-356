import os
import click
from sqlalchemy import text, create_engine, URL
from sqlalchemy.exc import OperationalError, ProgrammingError

from tai_sql import pm
from .utils import Connectivity

class DBCommand:
    """
    Command to create a new database.
    """

    connectivity: Connectivity = Connectivity()
    
    def create(self) -> bool:
        """
        Crea la base de datos especificada en la configuración.
        
        Returns:
            bool: True si la base de datos se creó exitosamente o ya existía, False en caso contrario
        """
        try:

            # Verificar conectividad antes de intentar crear
            if not self.connectivity.verify():
                click.echo("❌ No se puede establecer conectividad. No es posible crear la base de datos.")
                return False
            
            # Verificar si ya existe
            if self.connectivity.db_exist():
                click.echo("ℹ️  La base de datos ya existe")
                return True
            
            click.echo(f"🚀 Creando base de datos: {pm.db.provider.database}")
            
            if pm.db.provider.drivername == "sqlite":
                # SQLite - crear archivo de base de datos vacío
                db_file = pm.db.provider.database
        
                # Crear directorios padre si no existen
                os.makedirs(os.path.dirname(db_file) if os.path.dirname(db_file) else '.', exist_ok=True)

                with pm.db.engine.connect() as conn:
                    pass  # La conexión crea el archivo
                
                click.echo(f"✅ Base de datos SQLite creada: {db_file}")
                return True
            
            engine = create_engine(
                URL.create(
                    drivername=pm.db.provider.drivername,
                    username=pm.db.provider.username,
                    password=pm.db.provider.password,
                    host=pm.db.provider.host,
                    port=pm.db.provider.port
                )
            )
            
            with engine.connect() as conn:
                if pm.db.provider.drivername == 'postgresql':
                    # PostgreSQL requires autocommit mode for CREATE DATABASE
                    conn = conn.execution_options(autocommit=True)
                    conn.execute(text("COMMIT"))
                    conn.execute(text(f'CREATE DATABASE "{pm.db.provider.database}"'))
                elif pm.db.provider.drivername == 'mysql':
                    # MySQL can use regular transaction mode
                    conn = conn.execution_options(autocommit=True)
                    conn.execute(text(f'CREATE DATABASE "{pm.db.provider.database}"'))
                    
                else:
                    click.echo(f"❌ Tipo de base de datos no soportado: {pm.db.provider.drivername}", err=True)
                    return False
            
            click.echo(f"✅ Base de datos {pm.db.provider.database} creada exitosamente")
            
            # Verificar que se creó correctamente
            return self.connectivity.db_exist()
            
        except (OperationalError, ProgrammingError) as e:
            click.echo(f"❌ Error al crear la base de datos: {e}", err=True)
            return False
        except Exception as e:
            click.echo(f"❌ Error inesperado: {e}", err=True)
            return False
        