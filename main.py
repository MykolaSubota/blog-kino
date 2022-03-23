from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload

engine = create_engine('sqlite:///kino-blog.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(254), nullable=True)
    posts = relationship('Post', back_populates='author')

    def __repr__(self):
        return self.username


association_table_post_tag = Table('association_post_tag', Base.metadata,
                                   Column('post_id', ForeignKey('post.id'), primary_key=True),
                                   Column('tag_id', ForeignKey('tag.id'), primary_key=True))


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship('User', back_populates='posts')
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    tags = relationship("Tag", secondary=association_table_post_tag, back_populates="posts")

    def __repr__(self):
        return self.title


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    posts = relationship('Post', back_populates='category')

    def __repr__(self):
        return self.name


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    body = Column(Text(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship('Post', back_populates='comments')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User")

    def __repr__(self):
        return self.body


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    posts = relationship("Post", secondary=association_table_post_tag, back_populates="tags")


def record_creation(record):
    session = Session()
    session.add(record)
    session.commit()
    session.close()


def adding_tag_to_post():
    session = Session()

    tag_movie = session.query(Tag).filter(Tag.name == 'movie').one_or_none()
    tag_fantasy = session.query(Tag).filter(Tag.name == 'fantasy').one_or_none()
    tag_thriller = session.query(Tag).filter(Tag.name == 'thriller').one_or_none()
    posts = session.query(Post).options(joinedload(Post.category)).all()
    for post in posts:
        post.tags.append(tag_movie)
        if tag_fantasy.name in post.category.name.lower():
            post.tags.append(tag_fantasy)
        else:
            post.tags.append(tag_thriller)

    session.commit()
    session.close()


def all_posts_by_author(username: str):
    session = Session()
    yield session.query(Post).join(User).filter(User.username == username)
    session.close()


def post_commentators(title: str):
    session = Session()
    yield session.query(User).join(Comment).join(Post).filter(Post.title == title)
    session.close()


def number_of_posts_by_author(username: str):
    session = Session()
    yield session.query(Post).join(User).filter(User.username == username).count()
    session.close()


def categories_of_posts_by_author(username: str):
    session = Session()
    yield session.query(Category).join(Post).join(User).filter(User.username == username)
    session.close()


def tag_posts(name: str):
    session = Session()
    yield session.query(Post).join(Post.tags).filter(Tag.name == name)
    session.close()


def main():
    Base.metadata.create_all()
    # record_creation(User(username='James Smith', email='james.smith@gmail.com'))
    # record_creation(User(username='John Johnson', email='john.johnson@gmail.com'))
    # record_creation(Category(name='Fantasy'))
    # record_creation(Category(name='Thriller'))
    # record_creation(Post(title='November',
    #                      body='Sophie Jacobs is going through the most difficult time of her life. Depression consumes '
    #                           'her to the very bones. Her unhealthy mind begins to hear the voice of a deceased person '
    #                           'during a recent shootout from an answering machine.', author_id=1, category_id=2))
    # record_creation(Post(title='Edge of Tomorrow 2 gets a new script?',
    #                      body="It looks like Future's Edge moves like this: one step forward and two steps back. Back "
    #                           "in October, it was said that the script for the continuation of fantasy with Tom Cruise "
    #                           "was completed. Now Emily Blunt says an entirely new script is being written. This means "
    #                           "more delays.", author_id=1, category_id=1))
    # record_creation(Post(title='88 minutes', body='A forensic psychologist receives an unusual message. An unknown '
    #                                               'psychopath said that the main character has only 88 minutes to '
    #                                               'live, and he is not bluffing.', author_id=2, category_id=2))
    # record_creation(Comment(body='Great movie', post_id=3, user_id=1))
    # record_creation(Comment(body='Very interesting film', post_id=1, user_id=2))
    # record_creation(Comment(body='This is one of my favorite movies', post_id=3, user_id=2))
    # record_creation(Tag(name='movie'))
    # record_creation(Tag(name='fantasy'))
    # record_creation(Tag(name='thriller'))
    # adding_tag_to_post()


if __name__ == '__main__':
    main()
