import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from biblioteca.multas.adapters.orm import metadata, start_mappers

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    
    try:
        start_mappers()
    except Exception:
        pass
        
    Session = sessionmaker(bind=engine)
    return Session()