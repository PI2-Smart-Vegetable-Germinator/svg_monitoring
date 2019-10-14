from flask.cli import FlaskGroup
from project import app, db

from populate import seedMachine, seedPlanting, seedSeedlings


cli = FlaskGroup(app)

# Create command
@cli.command()
def recreatedb():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Populate Functions
@cli.command()
def seed():
    seedMachine(db)
    seedSeedlings(db)
    seedPlanting(db)


if __name__ == "__main__":
    cli()
