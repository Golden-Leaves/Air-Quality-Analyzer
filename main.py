import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey
import requests
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///air.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id = mapped_column(ForeignKey("users.id"))
    author = relationship("User", back_populates="blog_post")

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_directory,".env")
    load_dotenv(env_path)
    api_key = os.getenv("API_KEY")
    print(api_key)
    params = {"key"}
    response = requests.get("https://example.com")
if __name__ == "__main__":
    main()