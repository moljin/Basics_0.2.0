from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref

from app.core.database import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # String은 제한 글자수를 지정해야 한다.
    title: Mapped[str] = mapped_column(String(100), index=True)
    img_path: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # users.id에서 users는 테이블명
    # 외래키를 사용할 때, 제약 조건에 name을 ForeignKey 안에 ForeignKey("users.id", name="fk_author_id") 이렇게 넣어라.
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", name="fk_author_id", ondelete='CASCADE'), nullable=False)
    # author_id가 nullable=True 이므로 Optional["User"]가 일관됩니다.
    author: Mapped["User"] = relationship("User", backref=backref("article_user_set",
                                                                  lazy="selectin",
                                                                  cascade="all, delete-orphan",
                                                                  passive_deletes=True), lazy="selectin")
    """ author 속성은 User 모델에서 Article 모델을 참조하기 위해 추가했다. 위와 같이 relationship으로 author(User) 속성을 생성하면,
    게시글 객체(예: article)에서 연결된 저자의 username 을 article.user.username 처럼 참조할 수 있다. 
    
    relationship의 첫 번째 파라미터는 참조할 모델명이고 두 번째 backref 파라미터는 역참조 설정이다. 역참조란 쉽게 말해 User 에서 Article을 거꾸로 참조하는 것을 의미한다. 
    한 User에는 여러 개의 Article이 생성 수 있는데 역참조는 이 User가 작성한 Article 들을 참조할 수 있게 한다. 
    예를 들어 어떤 User에 해당하는 객체가 a_user 라면 a_user.article_user_set 같은 코드로 해당 User가 작성한 Article 들을 참조할 수 있다.
    """


def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', author_id={self.author_id}, created_at={self.created_at})>"

"""
현재 템플릿 단에서 `<div class="uk-text-right">{{ article.author }}</div>` 여기에서
sqlalchemy.exc.StatementError: (sqlalchemy.exc.MissingGreenlet) greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place?
[SQL: SELECT users.id AS users_id, users.username AS users_username, users.email AS users_email, users.password AS users_password, users.created_at AS users_created_at
FROM users
WHERE users.id = %s]
[parameters: [{'pk_1': 21}]]
에러가 발생한다. 해결방법은? AI Chat

해당 에러는 템플릿에서 article.author에 접근하는 순간, SQLAlchemy가 “지연 로딩(lazy load)”을 수행하려고 하며, 
비동기 드라이버(aiomysql)를 쓰는 환경에서 Jinja2의 동기 렌더링 컨텍스트와 충돌해서 발생합니다. 
즉, 템플릿 렌더링 중에 DB I/O가 필요해져서 MissingGreenlet가 납니다.

1. (선택) 모델 관계 기본 전략을 selectin으로 설정
- 매 쿼리마다 options를 달기 어렵다면, 관계 정의에서 lazy="selectin"으로 설정해 지연 로딩 대신 배치 로딩을 기본으로 사용합니다.
class Article(Base):
    # ...
    author = relationship("User", back_populates="articles", lazy="selectin")

"""