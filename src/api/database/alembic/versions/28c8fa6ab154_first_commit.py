"""first commit

Revision ID: 28c8fa6ab154
Revises: 
Create Date: 2024-06-15 19:39:38.582815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28c8fa6ab154'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alunos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('telefone', sa.String(length=20), nullable=False),
    sa.Column('matricula', sa.String(length=20), nullable=False),
    sa.Column('lattes', sa.String(length=255), nullable=True),
    sa.Column('orientador_id', sa.Integer(), nullable=True),
    sa.Column('curso', sa.Enum('M', 'D'), nullable=False),
    sa.Column('data_ingresso', sa.Date(), nullable=False),
    sa.Column('data_qualificacao', sa.Date(), nullable=True),
    sa.Column('data_defesa', sa.Date(), nullable=True),
    sa.Column('senha_hash', sa.String(length=255), nullable=False),
    sa.Column('new_password_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alunos_cpf'), 'alunos', ['cpf'], unique=True)
    op.create_index(op.f('ix_alunos_curso'), 'alunos', ['curso'], unique=False)
    op.create_index(op.f('ix_alunos_data_defesa'), 'alunos', ['data_defesa'], unique=False)
    op.create_index(op.f('ix_alunos_data_ingresso'), 'alunos', ['data_ingresso'], unique=False)
    op.create_index(op.f('ix_alunos_data_qualificacao'), 'alunos', ['data_qualificacao'], unique=False)
    op.create_index(op.f('ix_alunos_email'), 'alunos', ['email'], unique=True)
    op.create_index(op.f('ix_alunos_id'), 'alunos', ['id'], unique=False)
    op.create_index(op.f('ix_alunos_lattes'), 'alunos', ['lattes'], unique=False)
    op.create_index(op.f('ix_alunos_matricula'), 'alunos', ['matricula'], unique=True)
    op.create_index(op.f('ix_alunos_nome'), 'alunos', ['nome'], unique=False)
    op.create_index(op.f('ix_alunos_orientador_id'), 'alunos', ['orientador_id'], unique=False)
    op.create_index(op.f('ix_alunos_senha_hash'), 'alunos', ['senha_hash'], unique=False)
    op.create_index(op.f('ix_alunos_telefone'), 'alunos', ['telefone'], unique=True)
    op.create_table('professores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('senha_hash', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('orientador', 'coordenador'), nullable=False),
    sa.Column('new_password_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_professores_email'), 'professores', ['email'], unique=True)
    op.create_index(op.f('ix_professores_id'), 'professores', ['id'], unique=False)
    op.create_index(op.f('ix_professores_nome'), 'professores', ['nome'], unique=False)
    op.create_table('tarefas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=False),
    sa.Column('completada', sa.Integer(), nullable=False),
    sa.Column('data_prazo', sa.Date(), nullable=False),
    sa.Column('aluno_id', sa.Integer(), nullable=False),
    sa.Column('last_notified', sa.Date(), nullable=True),
    sa.Column('data_conclusao', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tarefas_base',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=False),
    sa.Column('prazo_em_meses', sa.Integer(), nullable=False),
    sa.Column('curso', sa.Enum('M', 'D'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tarefas_base_curso'), 'tarefas_base', ['curso'], unique=False)
    op.create_index(op.f('ix_tarefas_base_id'), 'tarefas_base', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tarefas_base_id'), table_name='tarefas_base')
    op.drop_index(op.f('ix_tarefas_base_curso'), table_name='tarefas_base')
    op.drop_table('tarefas_base')
    op.drop_table('tarefas')
    op.drop_index(op.f('ix_professores_nome'), table_name='professores')
    op.drop_index(op.f('ix_professores_id'), table_name='professores')
    op.drop_index(op.f('ix_professores_email'), table_name='professores')
    op.drop_table('professores')
    op.drop_index(op.f('ix_alunos_telefone'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_senha_hash'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_orientador_id'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_nome'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_matricula'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_lattes'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_id'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_email'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_data_qualificacao'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_data_ingresso'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_data_defesa'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_curso'), table_name='alunos')
    op.drop_index(op.f('ix_alunos_cpf'), table_name='alunos')
    op.drop_table('alunos')
    # ### end Alembic commands ###
