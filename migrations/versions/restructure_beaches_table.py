"""restructure_beaches_table

Revision ID: restructure_beaches
Revises: previous_revision
Create Date: 2024-03-22 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'restructure_beaches'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Crear tabla temporal con la nueva estructura
    op.create_table(
        'beaches_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('image', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('services', sa.String(), nullable=True),
        sa.Column('access', sa.String(), nullable=False),
        sa.Column('featured', sa.Boolean(), default=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('locality_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.ForeignKeyConstraint(['locality_id'], ['localities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copiar datos existentes a la nueva tabla
    op.execute("""
        INSERT INTO beaches_new (
            id, name, image, description, type, services, access, 
            featured, latitude, longitude, locality_id, created_at, 
            updated_at, is_active
        )
        SELECT 
            b.id, b.name, b.image, b.description, b.type, b.services, 
            b.access, b.featured, b.latitude, b.longitude, 
            l.id as locality_id, b.created_at, b.updated_at, b.is_active
        FROM beaches b
        JOIN localities l ON LOWER(l.name) = LOWER(b.town)
    """)

    # Eliminar tabla antigua
    op.drop_table('beaches')

    # Renombrar nueva tabla
    op.rename_table('beaches_new', 'beaches')

def downgrade():
    # En caso de necesitar revertir los cambios
    op.create_table(
        'beaches_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('image', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('town', sa.String(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('services', sa.String(), nullable=True),
        sa.Column('access', sa.String(), nullable=False),
        sa.Column('featured', sa.Boolean(), default=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Copiar datos de vuelta
    op.execute("""
        INSERT INTO beaches_old (
            id, name, image, description, region, town, type, services,
            access, featured, latitude, longitude, created_at, updated_at, is_active
        )
        SELECT 
            b.id, b.name, b.image, b.description, 
            l.zone_id as region, l.name as town, b.type, b.services,
            b.access, b.featured, b.latitude, b.longitude, 
            b.created_at, b.updated_at, b.is_active
        FROM beaches b
        JOIN localities l ON l.id = b.locality_id
    """)

    # Eliminar tabla nueva
    op.drop_table('beaches')

    # Renombrar tabla antigua
    op.rename_table('beaches_old', 'beaches') 