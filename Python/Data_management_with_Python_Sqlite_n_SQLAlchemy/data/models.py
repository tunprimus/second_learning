#!/usr/bin/env python3
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()


author_publisher = Table(
    "author_publisher",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("author.id")),
    Column("publisher_id", Integer, ForeignKey("publisher.publisher.id")),
)

book_publisher = Table(
    "book_publisher",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.id")),
    Column("publisher_id", Integer, ForeignKey("publisher.publisher.id")),
)


class Author(Base):
    __tablename__ = "author"
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    books = relationship("Book", backref=backref("authors"))
    publishers = relationship(
        "Publisher", secondary=author_publisher, back_populates="authors"
    )


class Book(Base):
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.author_id"))
    title = Column(String)
    publishers = relationship(
        "Publisher", secondary=book_publisher, back_populates="books"
    )


class Publisher(Base):
    __tablename__ = "publisher"
    publisher_id = Column(Integer, primary_key=True)
    name = Column(String)
    authors = relationship(
        "Author", secondary=author_publisher, back_populates="publishers"
    )
    books = relationship("Book", secondary=book_publisher, back_populates="publishers")
