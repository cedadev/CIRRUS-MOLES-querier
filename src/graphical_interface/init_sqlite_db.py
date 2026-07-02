from sqlalchemy import create_engine, Column, String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.schema import MetaData

DATABASE_URL = "sqlite:///./graphical_interface/chainlit.db"

engine = create_engine(DATABASE_URL)
Base = declarative_base(metadata=MetaData())


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    identifier = Column(String, unique=True, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=False)
    createdAt = Column(String)


class Thread(Base):
    __tablename__ = "threads"
    id = Column(String, primary_key=True)
    createdAt = Column(String)
    name = Column(String)
    userId = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    userIdentifier = Column(String)
    tags = Column(Text)
    metadata_ = Column("metadata", JSON)


class Step(Base):
    __tablename__ = "steps"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    threadId = Column(
        String, ForeignKey("threads.id", ondelete="CASCADE"), nullable=False
    )
    parentId = Column(String)
    streaming = Column(Boolean, nullable=False)
    waitForAnswer = Column(Boolean)
    isError = Column(Boolean)
    metadata_ = Column("metadata", JSON)
    tags = Column(Text)
    input = Column(Text)
    output = Column(Text)
    createdAt = Column(String)
    command = Column(Text)
    start = Column(String)
    end = Column(String)
    generation = Column(JSON)
    showInput = Column(String)
    language = Column(String)
    indent = Column(Integer)
    defaultOpen = Column(Boolean)
    autoCollapse = Column(Boolean, default=False)


class Element(Base):
    __tablename__ = "elements"
    id = Column(String, primary_key=True)
    threadId = Column(String, ForeignKey("threads.id", ondelete="CASCADE"))
    type = Column(String)
    url = Column(Text)
    chainlitKey = Column(String)
    name = Column(String, nullable=False)
    display = Column(String)
    objectKey = Column(String)
    size = Column(String)
    page = Column(Integer)
    language = Column(String)
    forId = Column(String)
    mime = Column(String)
    props = Column(JSON)


class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(String, primary_key=True)
    forId = Column(String, nullable=False)
    threadId = Column(
        String, ForeignKey("threads.id", ondelete="CASCADE"), nullable=False
    )
    value = Column(Integer, nullable=False)
    comment = Column(Text)


Base.metadata.create_all(engine)

print("SQLite database initialised successfully.")
