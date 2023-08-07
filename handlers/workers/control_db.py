from sqlalchemy import create_engine, ext, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from models.posts import Base, Post


class DBAlchemy:
    def __init__(self):
        self.db = "my_alchemy.db"

    async def create_db(self):
        engine = create_engine(f'sqlite:///{self.db}')
        Base.metadata.create_all(engine)

    async def session(self):
        engine = create_engine(f'sqlite:///{self.db}')
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    # сохраняем данные в базу
    async def add_new_data(self, id, text, photo):
        with await self.session() as session:
            data = Post(id=id, text=text, photo=photo, publish=0)
            try:
                session.add(data)
                session.commit()
            except IntegrityError as e:
                session.rollback()  # Откатываем транзакцию

    # получаем все неопубликованные посты
    async def get_not_publish_post(self):
        with await self.session() as session:
            posts = session.query(Post).filter_by(publish=0).all()
            return posts

    async def update_publish_value(self, id):
        with await self.session() as session:
            post = session.query(Post).filter_by(id=id).first()
            if post:
                post.publish = 1
                session.commit()
            else:
                print("запись не найдена")

    async def delete_total_records(self, max_count):
        with await self.session() as session:
            total_count = session.query(Post).count()
            if total_count > max_count:
                old_posts = session.query(Post).order_by(desc(Post.created_at)).limit(50).all()
                if old_posts:
                    for post in old_posts:
                        session.delete(post)
                    session.commit()