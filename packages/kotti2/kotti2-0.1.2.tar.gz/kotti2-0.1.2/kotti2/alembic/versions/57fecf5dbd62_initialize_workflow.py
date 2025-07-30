"""Initialize workflow and publish all items.

Revision ID: 57fecf5dbd62
Revises: 9398ccf41c2
Create Date: 2012-08-06 17:53:55.352478

"""

# revision identifiers, used by Alembic.
revision = '57fecf5dbd62'
down_revision = '9398ccf41c2'


def upgrade():
    from kotti2 import DBSession
    from kotti2 import get_settings
    from kotti2.resources import Document
    from kotti2.workflow import get_workflow
    from kotti2.workflow import reset_workflow

    is_default = get_settings()['kotti2.use_workflow'] == 'kotti2:workflow.zcml'
    if not is_default:
        return

    reset_workflow()
    for obj in DBSession.query(Document):
        workflow = get_workflow(obj)
        workflow.transition_to_state(obj, None, 'public')


def downgrade():
    pass
