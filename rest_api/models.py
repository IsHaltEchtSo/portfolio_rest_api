from flask import current_app as app
from sqlalchemy import Column, ForeignKey, Integer, String, Table, \
                        create_engine, func, select
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from typing_extensions import Self

engine = create_engine(app.config['DATABASE_URI'], echo=False)
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base(bind=engine)


follower_association = Table(
    'follower_association', Base.metadata,
    Column('follower_id', ForeignKey('user.id'), primary_key=True),
    Column('followee_id', ForeignKey('user.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    follower = relationship(
        'User', backref='following', 
        secondary=follower_association,
        primaryjoin=follower_association.c.followee_id == id,
        secondaryjoin=follower_association.c.follower_id ==id
    )

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    @hybrid_property
    def follower_count(self) -> int:
        return len(self.follower)

    @follower_count.expression
    def follower_count(cls) -> int:
        return select([func.count()]) \
            .where(cls.id == follower_association.c.followee_id) \
            .scalar_subquery()

    @hybrid_property
    def following_count(self) -> int:
        return len(self.following)

    @following_count.expression
    def following_count(cls) -> int:
        return select([func.count()]) \
            .where(cls.id == follower_association.c.follower_id) \
            .scalar_subquery()

    @hybrid_method
    def has_follower(self, follower: Self) -> bool:
        for f in self.follower:
            if f.id == follower.id:
                return True
        return False

    @has_follower.expression
    def has_follower(cls, follower: Self.__class__) -> bool:
        return select([bool(1)]) \
            .where(cls.id == follower_association.c.followee_id) \
            .where(follower.id == follower_association.c.follower_id) \
            .scalar_subquery()

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.name}>"


Base.metadata.create_all()
