from datetime import date, datetime
from sqlalchemy import DATETIME, Date, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine("sqlite:///database.db")


Base = declarative_base()

class Posts(Base):
    __tablename__ = 'posts'
    
    id 				= Column(Integer, primary_key=True, autoincrement=True)
    idWp 			= Column(Integer, nullable=True)
    urlPost 		= Column(String(255), nullable=True)
    title 			= Column(String(255), nullable=True)
    description 	= Column(String(255), nullable=True)
    thumbLink 		= Column(String(255), nullable=True)
    author 			= Column(String(60), nullable=True)
    publishDate 	= Column(Date, nullable=True)
    categories 		= Column(String(255), nullable=True)
    categoriesWp 	= Column(String(255), nullable=True)
    numberComments 	= Column(Integer, nullable=True)
    comments 		= Column(Text, nullable=True)
    numberViews 	= Column(Integer, nullable=True)

Base.metadata.create_all(engine)


if __name__ == '__main__':
    
    from sqlalchemy.orm import sessionmaker
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    postTest = Posts()
    postTest2 = Posts()

    postTest.author = 'bagla'
    postTest2.author = 'bagla2'

    session.add(postTest)
    session.add(postTest2)

    session.commit()

    posts = session.query(Posts).all()
    for post in posts:
        print(post.author)
